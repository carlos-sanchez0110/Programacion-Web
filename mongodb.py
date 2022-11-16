# Clase para conectarnos a MongoDB
import pymongo
from crudmysql import MySQL
from configuracion import varmongo
from env import variables as varsmysql

class PyMongo():
    def __init__(self, varmongo):
        self.MONGO_DATABASE = varmongo["db"]
        self.MONGO_URI = 'mongodb://' + varmongo["host"] + ':' + str(varmongo["port"])
        self.MONGO_CLIENT = None
        self.MONGO_RESPUESTA = None
        self.MONGO_TIMEOUT = varmongo["timeout"]

    def conectar_MongoDB(self):
        try:
            self.MONGO_CLIENT = pymongo.MongoClient(self.MONGO_URI, serverSelectionTimeoutMS=self.MONGO_TIMEOUT)
        except Exception as error:
            print("ERROR", error)
        else:
            pass
            #print("Conexion al servidor de MongoDB finalizada")
        # finally:

    def desconectar_MongoDB(self):
        if self.MONGO_CLIENT:
            self.MONGO_CLIENT.close()

    def eliminar_objeto(self, tabla, filtro):
        response = {'status': False}
        self.MONGO_RESPUESTA = self.MONGO_CLIENT[self.MONGO_DATABASE][tabla].delete_one(filtro)
        if self.MONGO_RESPUESTA:
            return self.MONGO_RESPUESTA
        else:
            return None

    def consulta_MongoDB(self, tabla, filtro, atributos={"_id": 0}):
        response = {"status": False, "resultado": []}
        self.MONGO_RESPUESTA = self.MONGO_CLIENT[self.MONGO_DATABASE][tabla].find(filtro, atributos)
        if self.MONGO_RESPUESTA:
            response["status"] = True
            for reg in self.MONGO_RESPUESTA:
                # print(reg)
                response["resultado"].append(reg)
        return response

        # Actualizar documentos en las colecciones
    def actualizar_valor(self, tabla, filtro, nuevos_valores):
        response = {"status": False}
        self.MONGO_RESPUESTA = self.MONGO_CLIENT[self.MONGO_DATABASE][tabla].update_many(filtro, nuevos_valores)
        if self.MONGO_RESPUESTA:
            response["status"] = True
            # return self.MONGO_RESPUESTA
        # else:
        # return None
        return response

    def insetar_estudiante(self, tabla, documento):
        self.MONGO_RESPUESTA = self.MONGO_CLIENT[self.MONGO_DATABASE][tabla].insert_one(documento)
        if self.MONGO_RESPUESTA:
            return self.MONGO_RESPUESTA
        else:
            return None


    # Obtener el promedio de estudiantes
    def obtener_promedios(self, tabla):
        response = {"status": False, "resultado": []}
        self.MONGO_RESPUESTA = self.MONGO_CLIENT[self.MONGO_DATABASE][tabla].aggregate(
                [
                    {
                        "$group": {
                            "_id": "$control",
                            "promedio": { "$avg": "$calificacion"}
                             }
                    }
                ]
        )
        if self.MONGO_RESPUESTA:
            response["status"] = True
            for reg in self.MONGO_RESPUESTA:
                # print(reg)
                response["resultado"].append(reg)
        return response

def cargar_estudiantes():
    obj_MySQL = MySQL(varsmysql)
    obj_Mongo = PyMongo(varmongo)
    sql = "SELECT * FROM estudiantes;"
    obj_MySQL.conectar_mysql()
    obj_Mongo.conectar_MongoDB()
    lista_estudiantes = obj_MySQL.desconectar_mysql()
    for est in lista_estudiantes:
        e = {
            "control": est[0],
            "nombre": est[1]
        }
        obj_Mongo.insetar_estudiante(e)
    obj_Mongo.desconectar_MongoDB()


# alumno = {
#     'control': 200,
#     'nombre': 'Juan Orozco Perez'
# }
# obj_Mongo = PyMongo(varmongo)
# cargar_estudiantes()
# # obj_Mongo.conectar_MongoDB()
# # obj_Mongo.insetar_estudiante(alumno)
# # obj_Mongo.desconectar_MongoDB()
# # def conexion_mongo(host='localhost', db='opensource', port=27017, timeout=1000, user='', password=''):

