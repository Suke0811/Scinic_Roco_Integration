from collections import defaultdict
import glob
import os.path
import sys

from controller import Supervisor
import simplejson   # preserves field names of namedtuples, unlike json
import scenic
import scenic.simulators.webots
from scenic.core.serialization import scenicToJSON
import verifai

import scenic.core.errors
scenic.core.errors.showInternalBacktrace = True

print('Starting new batch of simulations.')

# set up supervisor
supervisor = Supervisor()
topLevelNodes = supervisor.getRoot().getField('children')

# find designs to test
designs = glob.glob('../../../results/designs/*.wbo')
designData = {}
for design in designs:
    root, ext = os.path.splitext(design)
    jsonPath = root + '.json'
    with open(jsonPath, 'r') as f:
        data = simplejson.load(f)
    params = {'Children': data['Children']}
    designData[design] = dict(parameters=params, testResults={})

print(f'Found {len(designs)} designs to test.')

# load scenario
scenario = scenic.scenarioFromFile('test.scenic')
simulationsPerDesign = scenario.params['simulationsPerDesign']
timestep = 10
simulationTimeLimit = (1000 / timestep) * scenario.params['simulationTimeLimit']
segments = scenario.params['segments']
ss = verifai.samplers.ScenicSampler(scenario)

# generate set of environments to test against
envs = []
for i in range(simulationsPerDesign):
    env, _ = scenario.generate()
    envs.append(env)

scenes = defaultdict(dict)
serializedScenes = defaultdict(dict)
for i, env in enumerate(envs):
    fixedObjects = range(2, len(scenario.objects))
    scenario.conditionOn(scene=env, objects=fixedObjects)
    for j, segment in enumerate(segments):
        scenario.conditionOn(params={'segment': segment})
        scene, _ = scenario.generate()
        point = ss.pointForScene(scene)
        scenes[i][j] = scene
        serializedScenes[i][j] = point

print(f'Generated {len(scenes)} environments to test against.')

# set up simulator and run tests
simulator = scenic.simulators.webots.WebotsSimulator(supervisor)
supervisor.simulationSetMode(supervisor.SIMULATION_MODE_FAST)

for design, data in designData.items():
    print(f'Testing design {design}')
    results = data['testResults']

    # Create new node for the robot
    topLevelNodes.importMFNode(-1, design)
    robot = topLevelNodes.getMFNode(-1)
    torqueField = robot.getField('customData')

    # Run all tests
    for i, subscenes in scenes.items():
        results[i] = {}
        for j, scene in subscenes.items():
            # Run a single test
            simulation = simulator.simulate(scene, verbosity=2)

            # Collect results of the test
            results[i][j] = simulation.records if simulation else None

    # Remove the robot node for subsequent tests
    topLevelNodes.removeMF(-1)

#supervisor.simulationSetMode(supervisor.SIMULATION_MODE_PAUSE)

print('All tests complete.')

# Write results to file
outpath = '../../../results/results.json'
data = dict(tests=serializedScenes, designs=designData)
with open(outpath, 'w') as f:
    simplejson.dump(data, f, default=scenicToJSON)#, indent='\t')

print(f'Results written to {outpath}')

#sys.stdout.flush()
supervisor.step(1)  # seems to be necessary to prevent the last messages getting lost

supervisor.simulationQuit(0)

