"""Module for servants implementations."""

from typing import List

import Ice

import IceDrive

import json

from .discovery import Discovery

class Directory(IceDrive.Directory):
    """Implementation of the IceDrive.Directory interface."""

    def __init__(self, user, discovery : Discovery, userAlive: IceDrive.UserPrx):
        self.user = user
        self.discovery = discovery
        self.userAlive = userAlive
        self.name = "root"
        self.childrens = []
        self.files = {}

    def getPath(self, current: Ice.Current = None) -> str:
        """Return the path for the directory within the user space."""

    def getParent(self, current: Ice.Current = None) -> IceDrive.DirectoryPrx:
        """Return the proxy to the parent directory, if it exists. None in other case."""
        if self.userAlive.isAlive() is True:
            #comprobamos que tiene padre, si no lo tiene lanzamos la excepción
            if self.name != "root":
                parent = Directory(self.user, self.discovery)

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
        else:
            print("El usuario '{user}' ya no esta disponible.")

    def getChilds(self, current: Ice.Current = None) -> List[str]:
        """Return a list of names of the directories contained in the directory."""
        if self.userAlive.isAlive() is True:
            #Devolvemos la lista de hijos
            return list(self.childrens)
        else:
            print("El usuario '{user}' ya no esta disponible.")

    def getChild(self, name: str, current: Ice.Current = None) -> IceDrive.DirectoryPrx:
        """Return the proxy to one specific directory inside the current one."""
        if self.userAlive.isAlive() is True:
            #comprobamos si el hijo que se quiere existe en la lista de hijos, si no, lanzamos la excepción
            if name in self.childrens:
                with open("directorios.json", "r") as file:
                    d = json.load(file)
                
                #creamos un objeto y le damos el nuevo nombre de la ruta
                child = Directory(self.user, self.discovery)
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
        else:
            print("El usuario '{user}' ya no esta disponible.")

    def createChild(
        self, name: str, current: Ice.Current = None
    ) -> IceDrive.DirectoryPrx:
        """Create a new child directory and returns its proxy."""
        if self.userAlive.isAlive() is True:
            #Comprobamos que no exista ya un directorio con ese nombre, si ya existe lanzamos la excepción
            if name not in self.childrens:
                
                #cargamos el json
                with open("directorios.json", "r") as file:
                    d = json.load(file)
                
                #registramos el hijo en el directorio actual
                for i in d[self.user]:
                    if i["name"] == self.name:
                        i["childrens"].append(name)

                #añadimos el nuevo directorio
                d[self.user].append(
                    {"name": (self.name + "/" + name), "childrens": [], "files": {}}
                )
                
                #creamos y damos nombre al nuevo directorio
                newChild = Directory(self.user, self.discovery)
                newChild.name = self.name + "/" + name

                #escribimos el json
                with open("directorios.json", "w") as file:
                    json.dump(d, file, indent=4)
                
                #enviamos el proxi del nuevo hijo
                proxy = current.adapter.addWithUUID(newChild)
                return IceDrive.DirectoryPrx.uncheckedCast(proxy)
            else:
                raise IceDrive.ChildAlreadyExists(name, self.name)
        else:
            print("El usuario '{user}' ya no esta disponible.")

    def removeChild(self, name: str, current: Ice.Current = None) -> None:
        """Remove the child directory with the given name if exists."""
        if self.userAlive.isAlive() is True:
            #cargamos el json
            with open("directorios.json", "r") as file:
                d = json.load(file)
        
            #comprobamos si el directorio existe en la lista de hijos del directorio actual, si no, lanzamos la excepción
            if name in self.childrens:
                for i in d[self.user]:
                    if i["name"] == self.name:
                        #creamos un objeto Directory para llamar recurrentemente al metodo removeChild
                        dir = Directory(self.user, self.discovery)
                        dir.name = self.name + "/" + name
                        i["childrens"].remove(name)
                        self.childrens.remove(name)
                        with open("directorios.json", "w") as file:
                            json.dump(d, file, indent=4)
                        for j in d[dir.user]:
                            if j["name"] == dir.name:
                                dir.childrens = j["childrens"]
                                dir.files = j["files"]
                                #borramos a los hijos
                                print(j)
                                for k in j["childrens"]:
                                    dir.removeChild(k)

                                with open("directorios.json", "r") as file:
                                    d = json.load(file)

                                #borramos con unLink los ficheros de losdirectorios que se van a borrar
                                for F in list(j["files"].keys()):
                                    dir.unlinkFile(F)
                                d[self.user].remove(j)

                #Guardamos el json modificado
                with open("directorios.json", "w") as file:
                    json.dump(d, file, indent=4)

                #si todo va bien devolvemos None
                return None
            else:
                raise IceDrive.ChildNotExists(name, self.name)
        else:
            print("El usuario '{user}' ya no esta disponible.")

    def getFiles(self, current: Ice.Current = None) -> List[str]:
        """Return a list of the files linked inside the current directory."""
        if self.userAlive.isAlive() is True:
            #devuelve una lista con las claves(nombres) de los ficheros
            return list(self.files.keys())
        else:
            print("El usuario '{user}' ya no esta disponible.")
    
    def getBlobId(self, filename: str, current: Ice.Current = None) -> str:
        """Return the "blob id" for a given file name inside the directory."""
        if self.userAlive.isAlive() is True:
            #comprobamos si existe el fichero en el directorio actual, en caso contrario lanzamos la excepción
            if filename in self.files.keys():
                return self.files[filename]
            else:
                raise IceDrive.FileNotFound(filename)
        else:
            print("El usuario '{user}' ya no esta disponible.")

    def linkFile(
        self, filename: str, blob_id: str, current: Ice.Current = None
    ) -> None:
        """Link a file to a given blob_id."""
        if self.userAlive.isAlive() is True:
            #Comprobamos que no existe ya un fichero con el mismo nommbre, si no, lanzamos la excepción
            if filename not in self.files.keys():
                BlobPrx = self.discovery.get_BlobService()
                if BlobPrx.link(blob_id) is None:
                    #cargamos el json
                    with open("directorios.json", "r") as file:
                        d = json.load(file)

                    #guardamos los cambios en el directorio local y en el json
                    self.files[filename] = blob_id
                    for i in d[self.user]:
                        if i["name"] == self.name:
                            i["files"][filename] = blob_id
                    
                    #guardamos los cambios en el json
                    with open("directorios.json", "w") as file:
                        json.dump(d, file, indent=4)

                    #si todo va bien devolvemos None
                    return None
                else: 
                    raise IceDrive.TemporaryUnavailable("BlobService")
            else:
                raise IceDrive.FileAlreadyExists(filename)
        else:
            print("El usuario '{user}' ya no esta disponible.")
        

    def unlinkFile(self, filename: str, current: Ice.Current = None) -> None:
        """Unlink (remove) a filename from the current directory."""
        if self.userAlive.isAlive() is True:
                #comprobamos que existe el fichero a borrar en el direcrtorio actual
            if filename in self.files.keys():
                #cargamos el json
                with open("directorios.json", "r") as file:
                    d = json.load(file)
                for i in d[self.user]:
                    if i["name"] == self.name:
                        blob_id = i["files"][filename]
                BlobPrx = self.discovery.get_BlobService()
                if BlobPrx.link(blob_id) is None:
                    #borramos los cambios en el directorio local y en el json
                    del self.files[filename]
                    for i in d[self.user]:
                        if i["name"] == self.name:
                            del i["files"][filename]
                    
                    #guardamos los cambios en el json
                    with open("directorios.json", "w") as file:
                        json.dump(d, file, indent=4)

                    #si todo va bien devolvemos None
                    return None
                else: 
                    raise IceDrive.TemporaryUnavailable("BlobService")
            else:
                raise IceDrive.FileNotFound(filename)
        else:
            print("El usuario '{user}' ya no esta disponible.")
    

class DirectoryService(IceDrive.DirectoryService):
    """Implementation of the IceDrive.Directory interface."""
    def __init__(self, discovery : Discovery):
        self.discovery = discovery

    def getRoot(self, user: IceDrive.UserPrx, current: Ice.Current = None) -> IceDrive.DirectoryPrx:
        """Return the proxy for the root directory of the given user."""
        AutenticationPrx = self.discovery.get_Authentication()
        if AutenticationPrx is not None:
            if self.VerificarUser(AutenticationPrx,user) is True:
                with open("directorios.json", "r") as file:
                    d = json.load(file)

                #comprobamos si ya tiene directorios y lo cargamos, si no tiene lo creamos
                if user.getUsername() in d.keys():
                    root = Directory(user.getUsername(), self.discovery)
                    root.name = d[user.getUsername()][0]["name"]
                    root.childrens = d[user.getUsername()][0]["childrens"]
                    root.files = d[user.getUsername()][0]["files"]

                    proxy = current.adapter.addWithUUID(root)
                    return IceDrive.DirectoryPrx.uncheckedCast(proxy)
                else:
                    root = Directory(user.getUsername(), self.discovery)
                    root.name = "root"
                    d[user.getUsername()] = []
                    d[user.getUsername()].append(
                        {"name": "root", "childrens": [], "files": {}}
                    )
                    with open("directorios.json", "w") as file:
                        json.dump(d, file, indent=4)

                    proxy = current.adapter.addWithUUID(root)
                    return IceDrive.DirectoryPrx.uncheckedCast(proxy)
            else:
                raise IceDrive.TemporaryUnavailable("AuthenticationService")
        else:
            raise IceDrive.TemporaryUnavailable("AuthenticationService")

    def VerificarUser(self,prx : IceDrive.AuthenticationPrx, user: IceDrive.UserPrx) -> bool:
        if prx.verifyUser(user) is True:
            if user.isAlive() is True:
                return True
            else: 
                return False
        else:
            return False
        