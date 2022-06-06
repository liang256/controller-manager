from maya import cmds
import os
import json
import pprint

USERAPPDIR = cmds.internalVar(userAppDir=True)
DIRECTORY = os.path.join(USERAPPDIR, 'controllerLibrary')

def createDirectory(directory=DIRECTORY):
    """
    Creates the given directory if it doean't exist already
    Args:
        directory (str): The directory to create
    """
    if not os.path.exists(directory):
        os.mkdir(directory)

class ControllerLibrary(dict):
    """
    This is a class to find, sav and load controllers. It sotres its' data in a dictionary.
    """

    def save(self, name, directory=DIRECTORY, screenshot=True,  **info):
        """
        Saves out a controller to a location on disk
        Args:
            name (str): the name to save the controller
            directory (str): The directory to save the controller to. Defaults to user directory
            screenshot (bool): Whether to save a screenshot or not
            **info: Any arbitrary info that needs to be saved with the controller

        Returns:
            str: The path to the files that was saved out
        """

        createDirectory(directory)
        path = os.path.join(directory, '%s.ma' % name)
        infoFile = os.path.join(directory, '%s.json' % name)

        info['name']=name
        info['path']=path

        cmds.file(rename=path)

        if cmds.ls(selection=True):
            cmds.file(force=True, type='mayaAscii', exportSelected=True)
        else:
            cmds.file(save=True, type='mayaAscii', force=True)

        if screenshot:
            info['screenshot'] = self.saveScreenshot(name, directory=directory)

        with open(infoFile, 'w') as f:
            json.dump(info, f, indent=4)

        self[name] = info

    def find(self, directory=DIRECTORY):
        """
        Finds cotrollers on disk
        Args:
            directory: The directory to search in

        """
        self.clear()
        if not os.path.exists(directory):
            return

        files = os.listdir(directory)
        mayaFiles = [f for f in files if f.endswith('.ma')]

        for ma in mayaFiles:
            name, ext = os.path.splitext(ma)
            path = os.path.join(directory, ma)

            infoFile = '%s.json' % name

            if infoFile in files:
                infoFile = os.path.join(directory, infoFile)

                with open(infoFile, 'r') as f:
                    info = json.load(f)
            else:
                info = {}

            screenshot = '%s.jpg' % name
            if screenshot in files:
                info['screenshot']=os.path.join(directory, screenshot)

            info['name']=name
            info['path']=path

            self[name] = info


    def load(self, name):
        """
        Loads a given controller
        Args:
            name: the name of the controller to load
        """
        path = self[name]['path']
        cmds.file(path, i=True, usingNamespaces=False)

    def saveScreenshot(self, name, directory=DIRECTORY):
        path = os.path.join(directory, '%s.jpg' % name)

        cmds.viewFit()
        cmds.setAttr('defaultRenderGlobals.imageFormat', 8)

        cmds.playblast(completeFilename=path, forceOverwrite=True, format='image', width=200, height=200, showOrnaments=False, startTime=1, endTime=1, viewer=False)

        return path
