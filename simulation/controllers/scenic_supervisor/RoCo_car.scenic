
import math

model scenic.simulators.webots.model

workspace = Workspace(RectangularRegion(0 @ 0, 0, 3, 3))

class Car(WebotsObject):
    width: 0.1
    length: 0.1
    webotsName: 'paperbot'
    battery[dynamic]: (1000, 1000, 0)

    @property
    def consumedEnergy(self):
        return self.battery[1] - self.battery[0]

class Target(WebotsObject):
    width: 0.01
    length: 0.01
    webotsType: 'Target'
