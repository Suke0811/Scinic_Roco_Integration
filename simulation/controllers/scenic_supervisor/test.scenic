from RoCo_car import *

param simulationsPerDesign = 2
param simulationTimeLimit = 40

param segments = ((0@0.8, 0@-0.9), (0@-0.9, 0.5@0.8))
param segment = Uniform(*globalParameters.segments)

startPos, endPos = globalParameters.segment[0], globalParameters.segment[1]

ego = Car at startPos, facing toward endPos,
  with elevation 0.15,
  with controller 'paperbot_controller',
  with customData str(endPos)

target = Target at endPos

hill1 = Hill at Range(-0.25, 0.25) @ 0,
  with width Range(1,2),
  with length 1,
  with height Range(0.02, 0.1)

hill2 = Hill in workspace, with width 0.4, with length 0.4, with height 0.2

Ground with width 2.5, with length 2.5,
  with elevation 0.05, with gridSize 30,
  with terrain [hill1, hill2]

terminate when (distance to target) <= 0.25
terminate after globalParameters.simulationTimeLimit seconds

record final (distance to target) as distanceToTarget
record final ego.consumedEnergy as consumedEnergy
record final simulation().currentRealTime as elapsedTime

#record (distance to target) as distance
#record ego.position as position
