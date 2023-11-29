"""Module for servants implementations."""

from typing import List

import Ice

import IceDrive

import json

class Directory(IceDrive.Directory):
    """Implementation of the IceDrive.Directory interface."""
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.children = {}
        self.files = {}

    '''def saveToJson(self, filename):
        data = {
            "name": self.name,
            "children": {},
            "files": self.files
        }

        for child_name, child_directory in self.children.items():
            data["children"][child_name] = child_directory.saveToJson(child_name)

        with open(filename, "w") as json_file:
            json.dump(data, json_file)

        return filename

    def loadFromJson(self, filename):
        with open(filename, "r") as json_file:
            data = json.load(json_file)

        self.name = data["name"]
        self.files = data["files"]

        for child_name, child_data in data["children"].items():
            child_directory = Directory(child_name, parent=self)
            child_directory.loadFromJson(child_data)
            self.children[child_name] = child_directory

        return self '''

    def getParent(self, current: Ice.Current = None) -> IceDrive.DirectoryPrx:
        """Return the proxy to the parent directory, if it exists. None in other case."""
        if self.parent:
            return IceDrive.DirectoryPrx.uncheckedCast(self.parent)
        else:
            return None
        
    def getChilds(self, current: Ice.Current = None) -> List[str]:
        """Return a list of names of the directories contained in the directory."""
        return list(self.childs.keys())
    
    def getChild(self, name: str, current: Ice.Current = None) -> IceDrive.DirectoryPrx:
        """Return the proxy to one specific directory inside the current one."""
        if name in self.children:
            return IceDrive.DirectoryPrx.uncheckedCast(self.children[name])
        else:
            return None

    def createChild(self, name: str, current: Ice.Current = None) -> IceDrive.DirectoryPrx:
        """Create a new child directory and returns its proxy."""

    def removeChild(self, name: str, current: Ice.Current = None) -> None:
        """Remove the child directory with the given name if exists."""

    def getFiles(self, current: Ice.Current = None) -> List[str]:
        """Return a list of the files linked inside the current directory."""

    def getBlobId(self, filename: str, current: Ice.Current = None) -> str:
        """Return the "blob id" for a given file name inside the directory."""

    def linkFile(
        self, filename: str, blob_id: str, current: Ice.Current = None) -> None:
        """Link a file to a given blob_id."""

    def unlinkFile(self, filename: str, current: Ice.Current = None) -> None:
        """Unlink (remove) a filename from the current directory."""


class DirectoryService(IceDrive.DirectoryService):
    """Implementation of the IceDrive.Directory interface."""

    def getRoot(self, user: str, current: Ice.Current = None) -> IceDrive.DirectoryPrx:
        """Return the proxy for the root directory of the given user."""
