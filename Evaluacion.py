'''
Tema: Examen 2da, Unidad 2
Fecha: 07 de Noviembre del 2022
Autor: Carlos Omar Sánchez Zamora
'''

import json
# Buscar municipio y retornar codigo postal, tipo de asentamiento y zona dentro de un json
def buscar_mpio(mpio):
    try:
        abrir = open("CPdescarga.txt", "r")
        dicc_mpio = {mpio: []}
    except FileNotFoundError:
        print("No se puede abrir el archivo")
    except UnicodeError:
        print("Error al decodificar al leer el archivo")
    finally:
        for i in abrir:
            dicc1 = i.split("|")
            for j in dicc1[0:13]:
                if dicc1[3] == mpio:
                    dicc2 = {}
                    dicc2["Codigo"] = dicc1[0]
                    dicc2["Tipo Asentamiento"] = dicc1[2]
                    dicc2["Zona"] = dicc1[13]
                    dicc_mpio[mpio].append(dicc2)
        print(json.dumps(dicc_mpio))
        abrir.close()

# Buscar estado y retornar codigo postal y municipios en un json
def buscar_edo(edo):
    try:
        abrir = open("CPdescarga.txt", "r")
        dicc_edo = {edo: []}
    except FileNotFoundError:
        print("No se puede abrir el archivo")
    except UnicodeError:
        print("Error al decodificar al leer el archivo")
    finally:
        for i in abrir:
            dicc1 = i.split("|")
            for j in dicc1[0:3]:
                if dicc1[4] == edo:
                    dicc2 = {}
                    dicc2["Codigo"] = dicc1[0]
                    dicc2["Municipio"] = dicc1[3]
                    dicc_edo[edo].append(dicc2)
        print(json.dumps(dicc_edo))
        abrir.close()

buscar_mpio("Jiquilpan")
# buscar_edo("Guanajuato")