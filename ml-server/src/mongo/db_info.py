from mongo.connector import Mongo


def get_db_info(database_name:str)->dict[str,int]:
    collection_names:list[str] =  Mongo.get_instance()[database_name].list_collection_names()
    returned:dict[str,int] = {}
    for collection_name in collection_names:
        
        returned[collection_name] = Mongo.get_instance()[database_name][collection_name].estimated_document_count()
    return returned