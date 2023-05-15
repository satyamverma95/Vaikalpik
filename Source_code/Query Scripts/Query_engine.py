from pyArango.connection import *
import json


class ArangoDB_Qurey_Engine:

    def __init__(self):
        self.local_host =   "http://localhost:8529"
        self.password   =   'iluvu00'
        self.conn       =   ""
        self.new_connection =   ""
        self.db         =   ""

    def connect_to_db (self):
    
        self.conn = Connection(username="root", password=self.password, arangoURL=self.local_host)

        return(self.conn)


    def get_collection_id (self, database_name, collection_name, topic_name):
        
        db = self.conn[database_name]
        collection = db[collection_name] 

        docs = collection.fetchByExample({"Topic" : topic_name }, batchSize=None)
        doc_id = docs[0]._key

        return (doc_id)


    def execute_document_query (self, query, database_name="_system"):

        db_h = self.conn[database_name]

        cursor = db_h.AQLQuery(query)

        return (cursor)

    def execute_traversal_query (self, query, collection, node_key, graph_name, database_name="_system"):

        db_h = self.conn[database_name]

        start_node = db_h[collection][node_key]

        cursor = db_h.AQLQuery( query, bindVars={"start_node": start_node["_id"], "graph_name": graph_name} )
        return (cursor)




if __name__ == "__main__":
    ArangoDB_h = ArangoDB_Qurey_Engine()
    ArangoDB_h.connect_to_db()
      
    ArangoDB_h.get_collection_id("Data_Science", "Machine_Learning","Regression")  
    
    all_child_query = "FOR node IN 1..1 OUTBOUND @start_node GRAPH @graph_name RETURN node"
    result = ArangoDB_h.execute_traversal_query(all_child_query, collection="Machine_Learning", node_key="112590",\
                                                 graph_name="Machine_Learning_Concepts", database_name="Data_Science")
    print("\n\nAll Childs :\n\n", result)
    
    parent_query = "FOR parent IN 1 INBOUND @start_node GRAPH @graph_name RETURN parent"
    result = ArangoDB_h.execute_traversal_query(parent_query, collection="Machine_Learning", node_key="112614",\
                                                 graph_name="Machine_Learning_Concepts", database_name="Data_Science")
    print("\n\nParent of Child :\n\n", result)
    
    all_child_neighbour_query = "FOR v, e IN 2..2 ANY @start_node GRAPH @graph_name  FILTER e.label == \"Sub_sub_topic\" RETURN  v"

    result = ArangoDB_h.execute_traversal_query(all_child_neighbour_query, collection="Machine_Learning", node_key="112614", \
                                                graph_name="Machine_Learning_Concepts", database_name="Data_Science"\
                                                )
    print("\n\nNeighbours of a Child :\n\n", result)
    