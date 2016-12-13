import adsk.core, adsk.fusion, traceback

from .Fusion360CommandBase import Fusion360CommandBase
from .svg_doc import Scene, Line, Text, Circle

def get_canvas_size(sketch):

    min_point = sketch.modelToSketchSpace(sketch.boundingBox.minPoint)
    max_point = sketch.modelToSketchSpace(sketch.boundingBox.maxPoint)

    # min_point = sketch.boundingBox.minPoint
    # max_point = sketch.boundingBox.maxPoint

    canvas_x = max_point.x - min_point.x
    canvas_y = max_point.y - min_point.y

    delta_x = 0.0 - min_point.x
    delta_y = 0.0 - min_point.y

    # app = adsk.core.Application.get()
    # ui = app.userInterface
    #
    # ui.messageBox("X = " + str(max_point.x) + "  y = " + str(max_point.y))
    # ui.messageBox("X = " + str(min_point.x) + "  y = " + str(min_point.y))
    # ui.messageBox("X = " + str(delta_x) + "  y = " + str(delta_y))

    return delta_x, delta_y, canvas_x, canvas_y


def process_sketch(sketch):

    delta_x, delta_y, canvas_x, canvas_y = get_canvas_size(sketch)

    sketch_curves = sketch.sketchCurves
    sketch_lines = sketch_curves.sketchLines
    sketch_circles = sketch_curves.sketchCircles

    #TODO Add some space around canvas
    scene = Scene(sketch.name, canvas_y, canvas_x)

    for line in sketch_lines:

        scene.add(Line((line.startSketchPoint.geometry.x+delta_x,
                        line.startSketchPoint.geometry.y+delta_y),
                       (line.endSketchPoint.geometry.x+delta_x,
                        line.endSketchPoint.geometry.y+delta_y)))

    for circle in sketch_circles:

        scene.add(Circle((circle.centerSketchPoint.geometry.x+delta_x,
                          circle.centerSketchPoint.geometry.y+delta_y),
                         circle.radius,
                         (0, 0, 255)))
    scene.write_svg()


# The following will define a command in a tool bar panel
class svgExporter(Fusion360CommandBase):
    
    # Runs when Fusion command would generate a preview after all inputs are valid or changed
    def onPreview(self, command, inputs):
        pass
    
    # Runs when the command is destroyed.  Sometimes useful for cleanup after the fact
    def onDestroy(self, command, inputs, reason_):    
        pass
    
    # Runs when when any input in the command dialog is changed
    def onInputChanged(self, command, inputs, changedInput):
        pass
    
    # Runs when the user presses ok button
    def onExecute(self, command, inputs):
        sketch = inputs.itemById('selectionInput').selection(0).entity
        process_sketch(sketch)

    # Runs when user selects your command from Fusion UI, Build UI here
    def onCreate(self, command, inputs):
        
        # Create a few inputs in the UI
        selection_input = inputs.addSelectionInput('selectionInput', 'Select Sketch: ', 'Select one')
        selection_input.addSelectionFilter('Sketches')