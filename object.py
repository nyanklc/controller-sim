# TODO:
# i should probably use numpy or something here
import math

SHAPES = {
    "triangle":0,
    "rectangle":1,
    "circle":2
}

# defines a physical object.
# should call update whenever the object's state changes.
class Object:
    def __init__(self, shape_type:str, color:tuple, radius:float, x:float=0, y:float=0, yaw:float=0):
        # print(f"object init: shape_type={shape_type}, radius={radius}, x={x}, y={y}, yaw={yaw}")
        self.x = x
        self.y = y
        self.yaw = yaw if yaw!=0 else 0
        self.radius = radius
        self.polygon = definePolygon(SHAPES[shape_type], radius)
        self.footprint = transformPolygon(self.polygon, self.x, self.y, self.yaw)
        self.color = color
        
    def update(self, dx=0, dy=0, dyaw=0):
        self.footprint = transformPolygon(self.footprint, dx, dy, dyaw, (self.x, self.y))
        self.x += dx
        self.y += dy
        self.yaw += dyaw

def definePolygon(shape_type:int, radius:float):
    polygon_points:list = []
    if shape_type == 0: # triangle
        angle = 2 * math.pi / 3
        x = 0
        y = radius
        polygon_points.append([x, y])
        createPolygon(polygon_points, x, y, 2, angle)
    elif shape_type == 1: # rectangle
        angle = math.pi / 2
        x = 0
        y = radius
        polygon_points.append([x, y])
        createPolygon(polygon_points, x, y, 3, angle)
        # rotate by 45 degrees to have a square, not a diamond
        rotatePolygon(polygon_points, math.pi / 4)
    elif shape_type == 2: # circle (10 corners)
        angle = math.pi / 5
        x = 0
        y = radius
        polygon_points.append([x, y])
        createPolygon(polygon_points, x, y, 3, angle)
    else:
        raise Exception("invalid shape_type argument")
    return polygon_points

def createPolygon(polygon_points, x, y, rotation_count, angle):
    temp : float
    for i in range(rotation_count):
        temp = x
        x = x * math.cos(angle) - y * math.sin(angle)
        y = temp * math.sin(angle) + y * math.cos(angle)
        polygon_points.append([x, y])

def transformPolygon(polygon, x, y, yaw, rotation_axis:tuple=None):
    rotatePolygon(polygon, yaw, rotation_axis)
    translatePolygon(polygon, x, y)
    return polygon

def rotatePolygon(polygon, angle, rotation_axis:tuple=None):
    if rotation_axis is not None:
        # translate to origin
        for point in polygon:
            point[0] -= rotation_axis[0]
            point[1] -= rotation_axis[1]
    # rotate
    for i in range(len(polygon)):
        temp = polygon[i][0]
        polygon[i][0] = polygon[i][0] * math.cos(angle) - polygon[i][1] * math.sin(angle)
        polygon[i][1] = temp * math.sin(angle) + polygon[i][1] * math.cos(angle)
    if rotation_axis is not None:
        # translate back
        for point in polygon:
            point[0] += rotation_axis[0]
            point[1] += rotation_axis[1]

def translatePolygon(polygon, x, y):
    for i in range(len(polygon)):
        polygon[i][0] += x
        polygon[i][1] += y
