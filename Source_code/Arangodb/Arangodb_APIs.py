from pyArango.connection import *
from pyArango.collection import Collection, Field



class ArangoDB:

    def __init__(self):
        self.local_host =   "http://localhost:8529"
        self.password   =   'iluvu00'
        self.conn       =   ""
        self.new_connection =   ""
        self.db         =   ""

    def connect_to_db (self):
    
        self.conn = Connection(username="root", password=self.password, arangoURL=self.local_host)

        return(self.conn)

    def create_database (self, databasename = "deafult"):
        
        db_name = databasename
        if not self.conn.hasDatabase(db_name):
            self.conn.createDatabase(name=db_name)

    def create_collection (self, database_name = "", collection_name = "" ):

        self.db = self.conn[database_name]

        if collection_name not in self.db.collections:
            self.new_collection  = self.db.createCollection(name=collection_name)
        else:
            print("Collections already exists.")

        #return (self.new_collection)

    def add_document (self, collection_name, document):

        collection = self.db[collection_name]
        
        doc = collection.createDocument()
        doc.set(document)
        doc.save()
        document_id = doc["_id"]

        return(document_id)

    def delete_colection (self, collection_name=""):

        collection = self.db[collection_name]
        collection.delete()



if __name__ == "__main__":
   ArangoDB_h = ArangoDB()
   ArangoDB_h.connect_to_db()