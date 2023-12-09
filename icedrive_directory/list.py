'''a = ["1","2","3"]
if "1" in a:
    print(a[0])
a.remove("3")
print(list(a))
name = "jaime/1/2/3"
name.split("/")
print(name)
padre = name.split("/")
print(padre[:-1])
padre.pop()

print("/".join(padre))'''

a = {
    "nombre" : "javi",
    "edad" : "12",
    "dni" : "2137979229"
}
print(a)
print(list(a.keys()))
if "nombre" in a.keys():
    print(a["nombre"])
del a["dni"]
print(a)