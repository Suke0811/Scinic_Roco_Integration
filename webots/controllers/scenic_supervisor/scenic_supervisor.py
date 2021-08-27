"""
Set object positions
"""

from controller import Supervisor
import time
import random
import importlib
import math

import scenic

availableObjects = {
    'Car': 1,
    'Target': 1,
    'Hill': 1,
}

print('Scenic supervisor running')

# get scene objects
supervisor = Supervisor()
objects = {}

for obj_name, count in availableObjects.items():
    for i in range(count):
        name = f'{obj_name}_{i}'
        webotsName = name if count > 1 else obj_name
        webotsObj = supervisor.getFromDef(webotsName)
        if webotsObj is None:
            raise RuntimeError('no object called %s' % webotsName)
        objects[name] = webotsObj

def setHillGeometry(hill, width, length, height, N=20):
    shape = hill.getField('children').getMFNode(0)
    grid = shape.getField('geometry').getSFNode()
    grid.getField('xDimension').setSFInt32(N)
    grid.getField('zDimension').setSFInt32(N)
    grid.getField('xSpacing').setSFFloat(width/(N-1))
    grid.getField('zSpacing').setSFFloat(length/(N-1))
    heights = grid.getField('height')
    count = heights.getCount()
    size = N*N
    if count > size:
        for i in range(count - size):
            heights.removeMF(-1)
    elif count < size:
        for i in range(size - count):
            heights.insertMFFloat(-1, 0)
    index = 0
    mean = (N-1)/2
    stddev = N/4
    for x in range(N):
        xd = (x - mean) / stddev
        for z in range(N):
            zd = (z - mean) / stddev
            y = height * math.exp(-((xd * xd) + (zd * zd)))
            heights.setMFFloat(index, y)
            index += 1

# load scenario
scenario = scenic.scenarioFromFile('test.scenic')

def sampleScene():
    # generate new scene
    scene, _ = scenario.generate()

    supervisor.simulationResetPhysics()

    nextIDs = { kind: 0 for kind in availableObjects }
    for obj in scene.objects:
        # find corresponding Webots object
        kind = obj.webotsType
        if kind not in nextIDs:
            raise RuntimeError('unknown type of object %s' % kind)
        name = kind + '_' + str(nextIDs[kind])
        if name not in objects:
            raise RuntimeError('not enough objects of type %s' % kind)
        nextIDs[kind] += 1
        webotsObj = objects[name]

        # update position and orientation
        pos = webotsObj.getField('translation').getSFVec3f()
        if kind == 'Hill':
            offset = scenic.core.vectors.Vector(-obj.width/2, -obj.length/2)
            setHillGeometry(webotsObj, obj.width, obj.length, obj.height)
        else:
            offset = scenic.core.vectors.Vector(0, 0)
        newPos = obj.position + offset
        pos[0] = newPos[0]
        pos[2] = newPos[1]
        rot = [0, 1, 0, obj.heading]
        webotsObj.getField('translation').setSFVec3f(pos)
        webotsObj.getField('rotation').setSFRotation(rot)

    # hide unused objects
    for kind, nextID in nextIDs.items():
        while nextID < availableObjects[kind]:
            name = kind + '_' + str(nextID)
            obj = objects[name]
            pos = obj.getField('translation').getSFVec3f()
            pos[0] = 100
            obj.getField('translation').setSFVec3f(pos)
            nextID += 1

sampleScene()

MAX_TIME = 60
start_time = time.time()

while True:

    supervisor.step(1)

    if time.time() - start_time > MAX_TIME:
        sampleScene()
        start_time = time.time()
