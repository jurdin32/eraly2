iconos=""

for icon in open('iconos.txt','r').readlines():
    icono="""{
        "id":"%s",
        "text":"%s"
    },\n"""%(icon.strip().replace("(alias)",""),icon.strip().replace("(alias)",""))
    iconos += icono
archivo=open("iconos.json","w")
archivo.writelines(iconos)
print(iconos)

