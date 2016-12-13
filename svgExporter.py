# Importing sample Fusion Command
# Could import multiple Command definitions here
from .svgExporterCommand import svgExporter

commands = []
command_defs = []

# Define parameters for 1st command
cmd = {
    'commandName': 'SVG Export',
    'commandDescription': 'Demo Command 1 Description',
    'commandResources': './resources',
    'cmdId': 'cmdID_Demo_1',
    'workspace': 'FusionSolidEnvironment',
    'toolbarPanelID': 'SolidScriptsAddinsPanel',
    'class': svgExporter
}
command_defs.append(cmd)

# Set to True to display various useful messages when debugging your app
debug = False


# Don't change anything below here:
for cmd_def in command_defs:
    command = cmd_def['class'](cmd_def, debug)
    commands.append(command)


def run(context):
    for command in commands:
        command.onRun()


def stop(context):
    for command in commands:
        command.onStop()