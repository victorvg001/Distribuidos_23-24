a = ["1","2","3"]
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

print("/".join(padre))