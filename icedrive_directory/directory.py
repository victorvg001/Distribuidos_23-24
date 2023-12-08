"""Module for servants implementations."""

from typing import List

import Ice

import IceDrive

import json


class Directory(IceDrive.Directory):
    """Implementation of the IceDrive.Directory interface."""

    def __init__(self, user):
        self.user = user
        self.name = "root"
        self.childrens = []
        self.files = {}

    def getParent(self, current: Ice.Current = None) -> IceDrive.DirectoryPrx:
        """Return the proxy to the parent directory, if it exists. None in other case."""
        #comprobamos que tiene padre, si no lo tiene lanzamos la excepción
        if self.name != "root":
            parent = Directory(self.user)

            with open("directorios.json", "r") as file:
                d = json.load(file)

            #Acortamos la ruta
            nombreVector = self.name.split("/")
            nombreVector.pop()
            parent.name = "/".join(nombreVector)

            #Leemos y enviamos el proxi
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
        #Devolvemos la lista de hijos
        return list(self.childrens)

    def getChild(self, name: str, current: Ice.Current = None) -> IceDrive.DirectoryPrx:
        """Return the proxy to one specific directory inside the current one."""
        #comprobamos si el hijo que se quiere existe en la lista de hijos, si no, lanzamos la excepción
        if name in self.children:
            with open("directorios.json", "r") as file:
                d = json.load(file)
            
            #creamos un objeto y le damos el nuevo nombre de la ruta
            child = Directory(self.user)
            child.name = self.name + "/" + name

            #Leemos y enviamos el proxi
            for i in d[self.user]:
                if i["name"] == child.name:
                    child.childrens = i["childrens"]
                    child.files = i["files"]

            proxy = current.adapter.addWithUUID(child)
            return IceDrive.DirectoryPrx.uncheckedCast(proxy)
        else:
            raise IceDrive.ChildNotExists(name, self.name)

    def createChild(
        self, name: str, current: Ice.Current = None
    ) -> IceDrive.DirectoryPrx:
        """Create a new child directory and returns its proxy."""
        #Comprobamos que no exista ya un directorio con ese nombre, si ya existe lanzamos la excepción
        if name not in self.childrens:
            
            #cargamos el json
            with open("directorios.json", "r") as file:
                d = json.load(file)
            
            #registramos el hijo en el directorio actual
            for i in d[self.user]:
                if i["name"] == self.name:
                    self.childrens.append(name)
            
            #creamos y damos nombre al nuevo directorio
            newChild = Directory(self.user)
            newChild.name = self.name + "/" + name

            #escribimos el json
            with open("directorios.json", "w") as file:
                json.dump(d, file)
            
            #enviamos el proxi del nuevo hijo
            proxy = current.adapter.addWithUUID(newChild)
            return IceDrive.DirectoryPrx.uncheckedCast(proxy)
        else:
            raise IceDrive.ChildAlreadyExists(name, self.name)

    def removeChild(self, name: str, current: Ice.Current = None) -> None:
        """Remove the child directory with the given name if exists."""
        #cargamos el json
        with open("directorios.json", "r") as file:
            d = json.load(file)
        
        #Borramos recursivamente los directorios
        path = self.name + "/" + name
        if path.split("/")[len(self.name.split("/"))] in self.childrens:
            for i in d[self.user]:
                if i["name"] == path:
                    newpath = path.split("/") 
                    for j in i["childrens"]:
                        self.removeChild("/".join(newpath[len(self.name.split("/")):]) + "/" + j)
                    #quitar files
                    for k in d[self.user]:
                            if k["name"] == "/".join(newpath[:-1]):
                                k["childrens"].remove(newpath[-1])
                                #quitar files
                    d[self.user].remove(i)

            #Guardamos el json modificado
            with open("directorios.json", "w") as file:
                json.dump(d, file)

            return None
        else:
            raise IceDrive.ChildNotExists(name, self.name)

    def getFiles(self, current: Ice.Current = None) -> List[str]:
        """Return a list of the files linked inside the current directory."""
        return list(self.files.keys())
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

        #comprobamos si ya tiene directorios y lo cargamos, si no tiene lo creamos
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
