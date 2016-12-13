__author__ = 'rainsbp'

# Modified from: http://code.activestate.com/recipes/325823-draw-svg-images-in-python/

from os.path import expanduser
import os


# Creates directory and returns file name for settings file
def get_file_name():

    # Get Home directory
    home = expanduser("~")
    home += '/svg_exporter/'

    # Create if doesn't exist
    if not os.path.exists(home):
        os.makedirs(home)

    # Create file name in this path
    # xmlFileName = home  + 'settings.xml'
    return home





class Scene:
    def __init__(self, name="svg", height=400, width=400):
        self.name = name
        self.items = []
        self.height = height
        self.width = width
        return

    def add(self, item):
        self.items.append(item)

    def str_array(self):
        var = ["<?xml version=\"1.0\"?>\n",
               "<svg height=\"%d\" width=\"%d\" xmlns=\"http://www.w3.org/2000/svg\">\n" % (self.height, self.width),
               "<g transform= \"translate(0,%d) scale(1,-1)\" \n" % self.height,
               "style=\"fill-opacity:1.0; stroke:black; stroke-width:1;\">\n"]
        for item in self.items:
            var += item.str_array()

        var += [" </g>\n</svg>\n"]

        return var

    def write_svg(self):
        svg_filename = get_file_name()
        svg_filename += self.name + ".svg"

        svg_file = open(svg_filename, 'w')
        svg_file.writelines(self.str_array())
        svg_file.close()
        return


class Line:
    def __init__(self, start, end):
        self.start = start  # xy tuple
        self.end = end      # xy tuple
        return

    def str_array(self):
        return ["  <line x1=\"%d\" y1=\"%d\" x2=\"%d\" y2=\"%d\" />\n" %\
                (self.start[0], self.start[1], self.end[0], self.end[1])]


class Circle:
    def __init__(self, center, radius, color):
        self.center = center  # xy tuple
        self.radius = radius  # xy tuple
        self.color = color    # rgb tuple in range(0,256)
        return

    def str_array(self):
        return ["  <circle cx=\"%d\" cy=\"%d\" r=\"%d\"\n" %\
                (self.center[0],self.center[1],self.radius),
                "    style=\"fill:%s;\"  />\n" % colorstr(self.color)]


class Rectangle:
    def __init__(self, origin, height, width, color):
        self.origin = origin
        self.height = height
        self.width = width
        self.color = color
        return

    def str_array(self):
        return ["  <rect x=\"%d\" y=\"%d\" height=\"%d\"\n" %\
                (self.origin[0], self.origin[1], self.height),
                "    width=\"%d\" style=\"fill:%s;\" />\n" %\
                (self.width, colorstr(self.color))]


class Text:
    def __init__(self, origin, text, size=24):
        self.origin = origin
        self.text = text
        self.size = size
        return

    def str_array(self):
        return ["  <text x=\"%d\" y=\"%d\" font-size=\"%d\">\n" %\
                (self.origin[0],self.origin[1],self.size),
                "   %s\n" % self.text,
                "  </text>\n"]


def colorstr(rgb):
    return "#%x%x%x" % (rgb[0]/16, rgb[1]/16, rgb[2]/16)


def test():
    scene = Scene('test')
    scene.add(Rectangle((100,100),200,200,(0,255,255)))
    scene.add(Line((200,200),(200,300)))
    scene.add(Line((200,200),(300,200)))
    scene.add(Line((200,200),(100,200)))
    scene.add(Line((200,200),(200,100)))
    scene.add(Circle((200,200),30,(0,0,255)))
    scene.add(Circle((200,300),30,(0,255,0)))
    scene.add(Circle((300,200),30,(255,0,0)))
    scene.add(Circle((100,200),30,(255,255,0)))
    scene.add(Circle((200,100),30,(255,0,255)))
    scene.add(Text((50,50),"Testing SVG"))
    scene.write_svg()
    return
