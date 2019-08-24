from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from panda3d.core import lookAt
from panda3d.core import GeomVertexFormat, GeomVertexData
from panda3d.core import Geom, GeomTriangles, GeomVertexWriter
from panda3d.core import Texture, GeomNode
from panda3d.core import PerspectiveLens
from panda3d.core import CardMaker
from panda3d.core import Light, Spotlight, DirectionalLight
from panda3d.core import TextNode
from panda3d.core import LVector3
import sys
import os
from numba import jit
import gc



def checker(data, x, y, z, preLoad, x_max, y_max, z_max):
    if data[x][y][z] == False:
        return
    global centralCoor
    yellow = 0
    blue = ((x - centralCoor[0]) ** 2 + (y - centralCoor[1]) ** 2 + (z - centralCoor[2]) ** 2) ** 0.5 / ((x_max / 2) ** 2 + (y_max / 2) ** 2 + (z_max / 2) ** 2) ** 0.5
    red = 1 - blue
    try:
        if data[x - 1][y][z] == False:
            color = (red * 0.3, blue * 0.3, yellow * 0.3, 1)
            preLoad.append((x + 0, y + 0, z + 0, x + 0, y + 1, z + 1, color))
    except:
        color = (red * 0.3, blue * 0.3, yellow * 0.3, 1)
        preLoad.append((x + 0, y + 0, z + 0, x + 0, y + 1, z + 1, color))
    try:
        if data[x][y - 1][z] == False:
            color = (red * 0.7, blue * 0.7, yellow * 0.7, 1)
            preLoad.append((x + 0, y + 0, z + 0, x + 1, y + 0, z + 1, color))
    except:
        color = (red * 0.7, blue * 0.7, yellow * 0.7, 1)
        preLoad.append((x + 0, y + 0, z + 0, x + 1, y + 0, z + 1, color))
    try:
        if data[x][y][z + 1] == False:
            color = (red, blue, yellow, 1)
            preLoad.append((x + 0, y + 0, z + 1, x + 1, y + 1, z + 1, color))
    except:
        color = (red, blue, yellow, 1)
        preLoad.append((x + 0, y + 0, z + 1, x + 1, y + 1, z + 1, color))
    '''
    try:
        if data[x + 1][y][z] == False:
            preLoad.append((x + 1, y + 0, z + 0, x + 1, y + 1, z + 1))
    except:
        preLoad.append((x + 1, y + 0, z + 0, x + 1, y + 1, z + 1))
    try:
        if data[x][y + 1][z] == False:
            preLoad.append((x + 0, y + 1, z + 0, x + 1, y + 1, z + 1))
    except:
        preLoad.append((x + 0, y + 1, z + 0, x + 1, y + 1, z + 1))
    try:
        if data[x][y][z - 1] == False:
            preLoad.append((x + 0, y + 0, z + 0, x + 1, y + 1, z + 0))
    except:
        preLoad.append((x + 0, y + 0, z + 0, x + 1, y + 1, z + 0))
    '''

def preLoading(data):
    x_max = 0
    y_max = 0
    z_max = 0
    print("start loading model...")
    preLoad = []
    for x in range(data.dims[0]):
        for y in range(data.dims[1]):
            for z in range(data.dims[2]):
                if data.data[x][y][z] == True:
                    if x_max < x: x_max = x
                    if y_max < y: y_max = y
                    if z_max < z: z_max = z
    print(x_max, y_max, z_max)
    global centralCoor
    centralCoor = (int(x_max / 2), int(y_max / 2), int(z_max / 2))
    for x in range(int(x_max / 2)):
        for y in range(int(y_max / 2)):
            for z in range(z_max):
                data.data[x][y][z] = False
    for x in range(data.dims[0]):
        for y in range(data.dims[1]):
            for z in range(data.dims[2]):
                checker(data.data, x, y, z, preLoad, x_max, y_max, z_max)
    print(len(preLoad))
    del(data)
    gc.collect()
    return (preLoad, x_max, y_max, z_max)

data = [[[]]]
# You can't normalize inline so this is a helper function
def normalized(*args):
    myVec = LVector3(*args)
    myVec.normalize()
    return myVec

# helper function to make a square given the Lower-Left-Hand and
# Upper-Right-Hand corners

def makeSquare(x1, y1, z1, x2, y2, z2, colorInfo):
    format = GeomVertexFormat.getV3n3cpt2()
    vdata = GeomVertexData('square', format, Geom.UHDynamic)

    vertex = GeomVertexWriter(vdata, 'vertex')
    normal = GeomVertexWriter(vdata, 'normal')
    color = GeomVertexWriter(vdata, 'color')
    texcoord = GeomVertexWriter(vdata, 'texcoord')

    # make sure we draw the sqaure in the right plane
    if x1 != x2:
        vertex.addData3(x1, y1, z1)
        vertex.addData3(x2, y1, z1)
        vertex.addData3(x2, y2, z2)
        vertex.addData3(x1, y2, z2)

        normal.addData3(normalized(2 * x1 - 1, 2 * y1 - 1, 2 * z1 - 1))
        normal.addData3(normalized(2 * x2 - 1, 2 * y1 - 1, 2 * z1 - 1))
        normal.addData3(normalized(2 * x2 - 1, 2 * y2 - 1, 2 * z2 - 1))
        normal.addData3(normalized(2 * x1 - 1, 2 * y2 - 1, 2 * z2 - 1))

    else:
        vertex.addData3(x1, y1, z1)
        vertex.addData3(x2, y2, z1)
        vertex.addData3(x2, y2, z2)
        vertex.addData3(x1, y1, z2)

        normal.addData3(normalized(2 * x1 - 1, 2 * y1 - 1, 2 * z1 - 1))
        normal.addData3(normalized(2 * x2 - 1, 2 * y2 - 1, 2 * z1 - 1))
        normal.addData3(normalized(2 * x2 - 1, 2 * y2 - 1, 2 * z2 - 1))
        normal.addData3(normalized(2 * x1 - 1, 2 * y1 - 1, 2 * z2 - 1))

    # adding different colors to the vertex for visibility
    color.addData4f(colorInfo[0], colorInfo[1], colorInfo[2], colorInfo[3])
    color.addData4f(colorInfo[0], colorInfo[1], colorInfo[2], colorInfo[3])
    color.addData4f(colorInfo[0], colorInfo[1], colorInfo[2], colorInfo[3])
    color.addData4f(colorInfo[0], colorInfo[1], colorInfo[2], colorInfo[3])

    texcoord.addData2f(0.0, 1.0)
    texcoord.addData2f(0.0, 0.0)
    texcoord.addData2f(1.0, 0.0)
    texcoord.addData2f(1.0, 1.0)
    # Quads aren't directly supported by the Geom interface
    # you might be interested in the CardMaker class if you are
    # interested in rectangle though
    tris = GeomTriangles(Geom.UHDynamic)
    tris.addVertices(0, 1, 3)
    tris.addVertices(1, 2, 3)

    square = Geom(vdata)
    square.addPrimitive(tris)
    return square


#cube.hprInterval(1.5, (360, 360, 360)).loop()



class viewer(DirectObject):

    def __init__(self, data):
        preLoad = preLoading(data)
        
        self.base = ShowBase()
        self.base.disableMouse()
        self.base.camera.setPos(0, -100, 0)
        self.base.setBackgroundColor(1,1,1)
        
        self.max_x = preLoad[1]
        self.max_y = preLoad[2]
        self.max_z = preLoad[3]
        preLoad = preLoad[0]
        
        # Note: it isn't particularly efficient to make every face as a separate Geom.
        # instead, it would be better to create one Geom holding all of the faces.
        snode = GeomNode('square')
        for element in preLoad:
            snode.addGeom(makeSquare(element[0], element[1], element[2], element[3], element[4], element[5], element[6]))
        print('done')
        '''
        square0 = makeSquare(-1, -1, -1, 1, -1, 1, colorInfo)
        square1 = makeSquare(-1, 1, -1, 1, 1, 1, colorInfo)
        square2 = makeSquare(-1, 1, 1, 1, -1, 1, colorInfo)
        square3 = makeSquare(-1, 1, -1, 1, -1, -1, colorInfo)
        square4 = makeSquare(-1, -1, -1, -1, 1, 1, colorInfo)
        square5 = makeSquare(1, -1, -1, 1, 1, 1, colorInfo)
        snode = GeomNode('square')
        snode.addGeom(square0)
        snode.addGeom(square1)
        snode.addGeom(square2)
        snode.addGeom(square3)
        snode.addGeom(square4)
        snode.addGeom(square5)
        '''

        self.cube = render.attachNewNode(snode)
        # OpenGl by default only draws "front faces" (polygons whose vertices are
        # specified CCW).
        self.cube.setTwoSided(True)



        #self.accept("1", self.toggleLightsSide)
        self.accept("w", self.keyW)
        self.accept("s", self.keyS)
        self.accept("a", self.keyA)
        self.accept("d", self.keyD)
        self.accept("arrow_left", self.arrow_left)
        self.accept("arrow_right", self.arrow_right)
        self.accept("arrow_up", self.arrow_up)
        self.accept("arrow_down", self.arrow_down)
        self.accept("wheel_up", self.wheel_up)
        self.accept("wheel_down", self.wheel_down)

        self.LightsOn = False
        
        '''
        slight = Spotlight('slight')
        slight.setColor((1, 1, 1, 1))
        lens = PerspectiveLens()
        slight.setLens(lens)
        self.slnp = render.attachNewNode(slight)
        dlight = DirectionalLight('dlight')
        dlight.setShadowCaster(True, 32, 32)
        dlnp = render.attachNewNode(dlight)
        self.dlnp = render.attachNewNode(dlight)
        '''
        self.base.run()
        
    def wheel_up(self):
        y = self.base.camera.getY()
        print("camera position y: ", y)
        self.base.camera.setY(y - 5)
    def wheel_down(self):
        y = self.base.camera.getY()
        print("camera position y: ", y)
        self.base.camera.setY(y + 5)

    def arrow_up(self):
        p = self.base.camera.getP()
        print("camera position Pitch: ", p)
        self.base.camera.setP(p + 5)
        
    def arrow_down(self):
        p = self.base.camera.getP()
        print("camera position Pitch: ", p)
        self.base.camera.setP(p - 5)
        
    def arrow_left(self):
        h = self.base.camera.getH()
        print("camera position Yaw: ", h)
        self.base.camera.setH(h - 5)
        
    def arrow_right(self):
        h = self.base.camera.getH()
        print("camera position Yaw: ", h)
        self.base.camera.setH(h + 5)
        
    def keyW(self):
        z = self.base.camera.getZ()
        print("camera position z: ", z)
        self.base.camera.setZ(z - 5)
        
    def keyS(self):
        z = self.base.camera.getZ()
        print("camera position z: ", z)
        self.base.camera.setZ(z + 5)
        
    def keyA(self):
        x = self.base.camera.getX()
        print("camera position x: ", x)
        self.base.camera.setX(x - 5)
        
    def keyD(self):
        x = self.base.camera.getX()
        print("camera position x: ", x)
        self.base.camera.setX(x + 5)

    '''
    def toggleLightsSide(self):
        self.LightsOn = not self.LightsOn

        if self.LightsOn:
            render.setLight(self.dlnp)
            self.dlnp.setPos(self.max_x, self.max_y, self.max_z)
            self.dlnp.lookAt(self.cube)
        else:
            render.setLightOff(self.dlnp)
    '''

            
'''
t = MyTapper()

'''