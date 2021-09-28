from typing import Optional
import pymongo
from pymongo.mongo_client import MongoClient
import os

class Mongo:
    username="root"
    password=os.environ['MONGO_INITDB_ROOT_PASSWORD']
    hostname="mongo"
    uri=f"mongodb://{username}:{password}@{hostname}:27017"
    session:Optional[MongoClient] = None
    @staticmethod
    def init():
        if('MONGO_STRING_OPTIONS' in os.environ):
            Mongo.uri+=os.environ['MONGO_STRING_OPTIONS']
        temp=pymongo.MongoClient(Mongo.uri)
        Mongo.session=temp

    @staticmethod
    def get_instance():
        if Mongo.session is None:
            Mongo.init()

        return Mongo.session

    