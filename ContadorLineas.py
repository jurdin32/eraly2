import os

from eraly2.settings import BASE_DIR

paths=[
    os.path.join(BASE_DIR,'Empresa'),
    os.path.join(BASE_DIR,'eraly2'),
    os.path.join(BASE_DIR,'Home'),
    os.path.join(BASE_DIR,'Personas'),
    os.path.join(BASE_DIR,'Producto'),
    os.path.join(BASE_DIR,'templates'),
    os.path.join(BASE_DIR,'Store'),
    os.path.join(BASE_DIR,'.gitignore'),
    os.path.join(BASE_DIR,'manage.py'),
    os.path.join(BASE_DIR,'requirements.txt'),
]
total= 0
def numLineasFichero(data):
    archivo=str(data)
    fichero = open(archivo, 'r')
    fichero.readline()
    fichero.seek(0)
    c=len(fichero.readlines())
    fichero.close()
    return c

for path in paths:
    contador =0
    lectura=len(path.split('.'))
    if lectura==1:
        for fichero in os.listdir(path):
            try:
                for f in os.listdir(path+"/"+fichero):
                    if f.endswith('py') or f.endswith('html'):
                        data=(os.path.join(path, fichero+"/"+f))
                        contador+=numLineasFichero(data)
            except:
                data=(os.path.join(path, fichero))
                contador+=numLineasFichero(data)
    else:
        contador = numLineasFichero(path)
    total +=contador
    print('Total de Lineas:',contador,'en el path:',path)

print('Total de lineas:',total)
print('Tiempo estimado, en horas:',total/30)
print('Tiempo estimado, en dias:',(total/30)/24)
print('Presupuesto:',total*.20)


