
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

class Hill(WebotsObject):
    width: 1
    length: 1
    height: 0.2
    webotsType: 'Hill'
    allowCollisions: True
    positionOffset: (self.width/2, -self.length/2)

    def startDynamicSimulation(self):
        super().startDynamicSimulation()
        self.setGeometry()

    def setGeometry(self, N=10):
        shape = self.webotsObject.getField('children').getMFNode(0)
        grid = shape.getField('geometry').getSFNode()
        grid.getField('xDimension').setSFInt32(N)
        grid.getField('zDimension').setSFInt32(N)
        grid.getField('xSpacing').setSFFloat(self.width/(N-1))
        grid.getField('zSpacing').setSFFloat(self.length/(N-1))
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
        stddev = N/3.5
        for x in range(N):
            xd = (x - mean) / stddev
            for z in range(N):
                zd = (z - mean) / stddev
                if x == 0 or x == N-1 or z == 0 or z == N-1:
                    y = 0
                else:
                    y = self.height * math.exp(-((xd * xd) + (zd * zd))) ** 0.5
                heights.setMFFloat(index, y)
                index += 1
