import adsk.core
import adsk.fusion
import os
import traceback

# Global list to keep all event handlers in scope.
handlers = []

def run(context):
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Get the add-in directory path
        addInPath = os.path.dirname(os.path.realpath(__file__))
        iconPath = os.path.join(addInPath, 'resources')
        
        # Create the command definition (resources folder will be used automatically)
        cmdDef = ui.commandDefinitions.addButtonDefinition(
            'toggleAnalysisVisibilityCmd',
            'Toggle Analysis',
            'Toggle visibility of the Analysis browser folder',
            iconPath
        )
        
        # Add command created event handler
        onCommandCreated = ToggleAnalysisCommandCreatedHandler()
        cmdDef.commandCreated.add(onCommandCreated)
        handlers.append(onCommandCreated)
        
        # Add the command to the Navigation toolbar
        navToolbar = ui.toolbars.itemById('NavToolbar')
        if navToolbar:
            control = navToolbar.controls.addCommand(cmdDef)
            control.isVisible = True
        
        # Optional: Show success message (comment out for production)
        # ui.messageBox('Toggle Analysis Visibility add-in loaded successfully!\n\nLook for the icon in the Inspect panel.')
        
    except:
        if ui:
            ui.messageBox('Failed to load Toggle Analysis add-in:\n{}'.format(traceback.format_exc()))

class ToggleAnalysisCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
        
    def notify(self, args):
        try:
            cmd = args.command
            onExecute = ToggleAnalysisCommandExecuteHandler()
            cmd.execute.add(onExecute)
            handlers.append(onExecute)
        except:
            pass

class ToggleAnalysisCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
        
    def notify(self, args):
        try:
            app = adsk.core.Application.get()
            design = app.activeProduct
            
            if not design:
                app.userInterface.messageBox('No active design found.')
                return
            
            # Toggle the Analysis folder visibility
            analyses = design.analyses
            analyses.isLightBulbOn = not analyses.isLightBulbOn
            
            # Optional: Show brief status (uncomment if desired)
            # status = "visible" if analyses.isLightBulbOn else "hidden"
            # app.userInterface.messageBox(f'Analysis folder is now {status}', 'Toggle Analysis')
            
        except Exception as e:
            app.userInterface.messageBox(f'Error toggling analysis visibility: {str(e)}')

def stop(context):
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Clean up the command definition
        cmdDef = ui.commandDefinitions.itemById('toggleAnalysisVisibilityCmd')
        if cmdDef:
            cmdDef.deleteMe()
            
        # Clean up handlers
        global handlers
        handlers = []
        
    except:
        pass