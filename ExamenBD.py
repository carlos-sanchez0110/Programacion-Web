import json

from mongodb import PyMongo
from configuracion import varmongo
#-------------------------------------

def consultar_materias(ctrl):
    obj_PyMongo = PyMongo(varmongo)
    print(" ================== Consultar Materias por Estudiante ===================== ")
    filtro = {'control': ctrl}
    atributos_estudiante = {"_id": 0, "nombre": 1}
    atributos_kardex = {"_id": 0, "materia": 1, "calificacion": 1}
    obj_PyMongo.conectar_MongoDB()
    respuesta1 = obj_PyMongo.consulta_MongoDB('estudiantes', filtro, atributos_estudiante)
    respuesta2 = obj_PyMongo.consulta_MongoDB('kardex', filtro, atributos_kardex)
    obj_PyMongo.desconectar_MongoDB()
    if respuesta1["status"] and respuesta2["status"]:
        json_estudiante = {"Nombre: ": respuesta1["resultado"][0]["nombre"], "Materias": []}
        json_materias = {"Nombre": [], "Promedio": []}
        for mat in respuesta2["resultado"]:
            json_materias["Nombre"].append(mat["materia"])
            json_materias["Promedio"].append(mat["calificacion"])
        json_estudiante["Materias"].append(json_materias)
    print(json.dumps(json_estudiante))

consultar_materias("18420455")