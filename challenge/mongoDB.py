#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import pymongo
"""
from desafio import Desafio
import os
"""


class BaseDatos:
    def __init__(self, direccion, prueba=False):
        logging.info("MONGO:Tratando de conectar con la base de datos.")
        MONGODB_URI = direccion
        client = pymongo.MongoClient(MONGODB_URI, connectTimeoutMS=40000)
        db = client["desafio"]
        """
        if ('NONAME' in os.environ):
            db = client["desafio"]
        else:
            db = client["desafio"]
        """
        if (not prueba):
            self.desafio = db.desafio
        else:
            self.desafio = db.prueba
        logging.info("MONGO:Conexión completada con éxito.")

    def insertDesafio(self, desafio):
        entrada = desafio.__dict__()
        if(self.desafio.find_one({"nombre": entrada['nombre']})):
            logging.warning(
                "MONGO:Desafio %s ya existente, no se ha podido insertar.", entrada['nombre'])
            # return False
            return True
        else:
            self.desafio.insert_one(entrada)
            logging.info(
                "MONGO:Desafio %s insertado en la base de datos.", entrada['nombre'])
            return True

    def getDesafio(self, nombre):
        desafio = self.desafio.find_one({"nombre": nombre})
        logging.info(
            "MONGO:Desafio %s devuelto por la base de datos.", nombre)

        if desafio is not None:
            # borra el objeto _id para no mostrarlo. mantiene el resto
            del desafio['_id']
            logging.info(
                "MONGO:Desafio %s devuelto por la base de datos.", nombre)
        return desafio

    def getDesafios(self):
        salida = {}
        for j in self.desafio.find():
            del j['_id']
            salida[j['nombre']] = j
        logging.info("MONGO:Todos los Desafios de la base de datos devueltos.")
        return salida
    """
    def insertDesafio(self, desafio):
        entrada = desafio.__dict__()
        if(self.desafio.find_one({"nombre": entrada['nombre']})):
            logging.warning(
                "MONGO:Desafio %s ya existente, no se ha podido insertar en la base de datos.", entrada['nombre'])
            return False
        else:
            self.desafio.insert_one(entrada)
            logging.info(
                "MONGO:Desafio %s insertado en la base de datos.", entrada['nombre'])
            return True
    """

    def removeDesafio(self, nombre):
        logging.info(
            "MONGO:Desafio %s eliminado de la base de datos.", nombre)
        self.desafio.delete_one({"nombre": nombre})

    def mostrarDesafios(self):
        cursor = self.desafio.find()
        for j in cursor:
            print(j['nombre'], ' - ', j['fecha_ini'], ' - ', j['fecha_fin'])

    def removeDesafios(self):
        for j in self.desafio.find():
            self.removeDesafio(j['nombre'])
        logging.info("MONGO:Base de datos de Desafio vaciada por completo.")

    def getSize(self):
        return self.desafio.count_documents({})

    def updateDesafio(self, nombre, updates):
        try:
            desafio = self.getDesafio(nombre)
            self.desafio.update_one({'nombre': desafio['nombre']}, {
                '$set': updates}, upsert=False)
        except:
            print("except")
            logging.warning(
                "MONGO:Error Se pretende actualizar una entrada inexistente.")