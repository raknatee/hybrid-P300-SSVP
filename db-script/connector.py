from typing import Optional
import pymongo #type: ignore
from pymongo.mongo_client import MongoClient #type: ignore
import config

class Mongo:
    username=config.USERNAME
    password=config.PASSWORD
    hostname=config.HOSTNAME
    uri=f"mongodb://{username}:{password}@{hostname}:{config.PORT}"
    session:Optional[MongoClient] = None
    @staticmethod
    def init():
        if(config.MONGO_STRING_OPTIONS != ""):
            Mongo.uri+=config.MONGO_STRING_OPTIONS
        temp=pymongo.MongoClient(Mongo.uri)
        Mongo.session=temp

    @staticmethod
    def get_instance()->MongoClient:
        if Mongo.session is None:
            Mongo.init()

        return Mongo.session

    