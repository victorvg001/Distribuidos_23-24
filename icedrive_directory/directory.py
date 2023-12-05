"""Module for servants implementations."""

from typing import List

import Ice

import IceDrive

import json


class Directory(IceDrive.Directory):
    """Implementation of the IceDrive.Directory interface."""

    def __init__(self, name):
        self.user = name
        self.name = "root"
        self.childrens = {}
        self.files = {}

    def getParent(self, current: Ice.Current = None) -> IceDrive.DirectoryPrx:
        """Return the proxy to the parent directory, if it exists. None in other case."""
        if self.parent != "None":
            parent = Directory(self.user)

            with open("directorios.json", "r") as file:
                d = json.load(file)

            nombreVector = self.name.split("/")
            nombreVector.pop()
            parent.name = "/".join(nombreVector)

            for i in d[self.user]:
                if i["name"] == parent.name:
                    parent.childrens = i["childrens"]
                    parent.files = i["files"]

            proxy = current.adapter.addWithUUID(parent)
            return IceDrive.DirectoryPrx.uncheckedCast(proxy)
        else:
            raise IceDrive.RootHasNoParent()

    def getChilds(self, current: Ice.Current = None) -> List[str]:
        """Return a list of names of the directories contained in the directory."""
        return list(self.childs.keys())

    def getChild(self, name: str, current: Ice.Current = None) -> IceDrive.DirectoryPrx:
        """Return the proxy to one specific directory inside the current one."""
        if name in self.children:
            return IceDrive.DirectoryPrx.uncheckedCast(self.children[name])
        else:
            return None

    def createChild(
        self, name: str, current: Ice.Current = None
    ) -> IceDrive.DirectoryPrx:
        """Create a new child directory and returns its proxy."""

    def removeChild(self, name: str, current: Ice.Current = None) -> None:
        """Remove the child directory with the given name if exists."""

    def getFiles(self, current: Ice.Current = None) -> List[str]:
        """Return a list of the files linked inside the current directory."""

    def getBlobId(self, filename: str, current: Ice.Current = None) -> str:
        """Return the "blob id" for a given file name inside the directory."""

    def linkFile(
        self, filename: str, blob_id: str, current: Ice.Current = None
    ) -> None:
        """Link a file to a given blob_id."""

    def unlinkFile(self, filename: str, current: Ice.Current = None) -> None:
        """Unlink (remove) a filename from the current directory."""


class DirectoryService(IceDrive.DirectoryService):
    """Implementation of the IceDrive.Directory interface."""

    def getRoot(self, user: str, current: Ice.Current = None) -> IceDrive.DirectoryPrx:
        """Return the proxy for the root directory of the given user."""
        with open("directorios.json", "r") as file:
            d = json.load(file)

        if d[user]:
            root = Directory(user)
            root.name = d[user][0]["name"]
            root.childrens = d[user][0]["childrens"]
            root.files = d[user][0]["files"]

            proxy = current.adapter.addWithUUID(root)
            return IceDrive.DirectoryPrx.uncheckedCast(proxy)
        else:
            root = Directory(user)
            root.name = "root"
            d[user] = []
            d[user].append(
                {"name": "root", "childrens": [], "files": []}
            )
            with open("directorios.json", "w") as file:
                json.dump(d, file)

            proxy = current.adapter.addWithUUID(root)
            return IceDrive.DirectoryPrx.uncheckedCast(proxy)
