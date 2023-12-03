import json

with open ('directorios.json', 'r') as file:
    d = json.load(file)
        

print(d["user1"])

if d["user1"]:
    #root = Directory(user)
    #root.name = d[user]["name"]
    #root.loadDirectory()
    for i in d["user1"]:
        for j in i["childrens"]:
            if j=="dir1":
                print(j)

d["user"] = []
d["user"].append({
    "name" : "root",
    "parent" : "None",
    "childrens" : [],
    "files" : []
})
with open ('directorios.json', 'w') as file:
    json.dump(d, file, indent=4)