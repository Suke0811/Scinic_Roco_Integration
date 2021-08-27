from RoCo_car import *

param simulationsPerDesign = 4
param simulationTimeLimit = 40

ego = Car at 0 @ 0.8,
  with elevation 0.15
#  with controller 'Wheel_Controller'

target = Target at 0 @ -0.9

# Hill at Range(-0.25, 0.25) @ 0,
#   with width Range(1,2),
#   with length 1,
#   with height Range(0.02, 0.1)

terminate when (distance to target) <= 0.25
terminate after globalParameters.simulationTimeLimit seconds

record final (distance to target) as distanceToTarget
record final ego.consumedEnergy as consumedEnergy
record final simulation().currentRealTime as elapsedTime

#record (distance to target) as distance
#record ego.position as position
