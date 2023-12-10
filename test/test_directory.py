from icedrive_directory.directory import Directory
import json



'''def test_getRoot():
    communicator = Ice.initialize()
    adapter = communicator.createObjectAdapterWithEndpoints("MyAdapter", "tcp -h localhost -p 10000")

    # Crea una instancia de la clase que estás probando
    directory_service = DirectoryService()

    # Simula un objeto Current para pasar a la prueba
    current = Ice.Current()
    assert DirectoryService().getRoot("user1",current) == IceDrive.DirectoryPrx
'''

def test_getChilds():
    with open("directorios.json", "r") as file:
        d = json.load(file)

    dir = Directory("user1")
    dir.name = "root"
    for i in d["user1"]:
        if i["name"] == dir.name:
            dir.childrens = i["childrens"]
            dir.files = i["files"]

    assert dir.getChilds() == ["dir1", "dir2"]

def test_removeChild():
    with open("directorios.json", "r") as file:
        d = json.load(file)

    dir = Directory("user1")
    dir.name = "root"
    for i in d["user1"]:
        if i["name"] == dir.name:
            dir.childrens = i["childrens"]
            dir.files = i["files"]
    
    assert dir.removeChild("dir1") is None

def test_getFiles():
    with open("directorios.json", "r") as file:
        d = json.load(file)

    dir = Directory("user1")
    dir.name = "root"
    for i in d["user1"]:
        if i["name"] == dir.name:
            dir.childrens = i["childrens"]
            dir.files = i["files"]
    assert dir.getFiles() == []

def test_linkFile():
    with open("directorios.json", "r") as file:
        d = json.load(file)

    dir = Directory("user1")
    dir.name = "root"
    for i in d["user1"]:
        if i["name"] == dir.name:
            dir.childrens = i["childrens"]
            dir.files = i["files"]
    assert dir.linkFile("file1", "12345") is None


def test_getBlobId():
    with open("directorios.json", "r") as file:
        d = json.load(file)

    dir = Directory("user1")
    dir.name = "root"
    for i in d["user1"]:
        if i["name"] == dir.name:
            dir.childrens = i["childrens"]
            dir.files = i["files"]
    assert dir.getBlobId("file1") == "12345"

def test_unlinkFile():
    with open("directorios.json", "r") as file:
        d = json.load(file)

    dir = Directory("user1")
    dir.name = "root"
    for i in d["user1"]:
        if i["name"] == dir.name:
            dir.childrens = i["childrens"]
            dir.files = i["files"]
    assert dir.unlinkFile("file1") is None