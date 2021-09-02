from rocolib.library import getComponent



length = 200
width = 130
height = 60

# a = getComponent("Paperbot", length=length, width=width, height=height)
# dim = {"length": length, "width": width, "height": height}
# a.makeOutput("designs/paperbot", thickness=5, tree=False, display=False, Webots=True, Dimensions=dim)

for length in range(80, 200, 50):
    for width in range(60, 200, 50):
        for height in range(20, 80, 50):
            dim = {"length": length, "width": width, "height": height}
            a = getComponent("Paperbot", length=length, width=width, height=height)
            a.makeOutput("designs/%(length)d_%(width)d_%(height)d/" %locals(), thickness=5, tree=False, display=False, Webots=True, Dimensions=dim)



