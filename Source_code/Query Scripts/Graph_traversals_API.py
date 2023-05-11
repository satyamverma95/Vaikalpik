from Query_engine import ArangoDB_Qurey_Engine

class Graph_API():
    def __init__(self):
        
        self.arangoDB_qurey_engine_h = ArangoDB_Qurey_Engine()

    def set_env_variables(self, database_name, collection_name, graph_name):
        self.database_name      =   database_name
        self.collection_name    =   collection_name
        self.graph_name         =   graph_name


    def get_parent_topic(self, topic_name, parent_level):
        #############################
        # We need to follow protocol while using Query Enging API
        #   1) Always connect to the databse first. 
        #   2) Thsi will initialise the database handle in the script.
        ###############################
        self.arangoDB_qurey_engine_h.connect_to_db()
        doc_id = self.arangoDB_qurey_engine_h.get_collection_id( collection_name=self.collection_name,\
                                                                 topic_name=topic_name,\
                                                                 database_name=self.database_name )
        #print("Document Id ", doc_id)
        if (doc_id):
            parent_query = "FOR parent IN {} OUTBOUND @start_node GRAPH @graph_name RETURN parent".format(parent_level)
            results_list = self.arangoDB_qurey_engine_h.execute_traversal_query ( parent_query, collection=self.collection_name,\
                                                                            node_key= doc_id,\
                                                                            graph_name=self.graph_name,\
                                                                            database_name=self.database_name )
            if(len(results_list)>0):
                parent_topic = results_list[-1].Topic
                print("Parent topic of {} is {}".format(topic_name, parent_topic))
            else:
                print("Cuurently we don't have level {} Parent topic for {}".format( parent_level, topic_name))

        return (parent_topic)

    def get_all_sub_topics(self, topic_name):
        
        self.arangoDB_qurey_engine_h.connect_to_db()
        doc_id = self.arangoDB_qurey_engine_h.get_collection_id( collection_name=self.collection_name,\
                                                                 topic_name=topic_name,\
                                                                 database_name=self.database_name )
        #print("Document Id ", doc_id)
        if (doc_id):
            all_child_query = "FOR node IN 1..1 INBOUND @start_node GRAPH @graph_name RETURN node"
            results_list = self.arangoDB_qurey_engine_h.execute_traversal_query ( all_child_query, collection=self.collection_name,\
                                                                                node_key= doc_id,\
                                                                                graph_name=self.graph_name,\
                                                                                database_name=self.database_name )
            if(len(results_list)>0):
                sorted_sub_topics = sorted(results_list, key=lambda x: tuple(map(int, x['Sequence'].split('.'))))
                sub_topics = ", ".join([doc['Topic'] for doc in sorted_sub_topics])
                print("Sub topics of \"{}\" are : {}".format(topic_name, sub_topics))
            else:
                print("Currently we don't have any sub topic for {}".format(topic_name))

    def get_all_other_sub_topics_of_a_topic(self, topic_name):
        
        self.arangoDB_qurey_engine_h.connect_to_db()
        doc_id = self.arangoDB_qurey_engine_h.get_collection_id( collection_name=self.collection_name,\
                                                                 topic_name=topic_name,\
                                                                 database_name=self.database_name )
        print("Document Id ", doc_id)
        if (doc_id):
            all_child_neighbour_query = "FOR v, e IN 2..2 ANY @start_node GRAPH @graph_name  FILTER e.label == \"depends_on\" RETURN  v"
          
            results_list = self.arangoDB_qurey_engine_h.execute_traversal_query ( all_child_neighbour_query, collection=self.collection_name,\
                                                                                node_key= doc_id,\
                                                                                graph_name=self.graph_name,\
                                                                                database_name=self.database_name )
            
            if(len(results_list)>0):
                sorted_neighbour_topics = sorted(results_list, key=lambda x: tuple(map(int, x['Sequence'].split('.'))))
                neighbour_topics = ", ".join([doc['Topic'] for doc in sorted_neighbour_topics])
                print("Neighbours of \"{}\" are : {}".format(topic_name, neighbour_topics))
            else:
                print("Currently we don't have any sub topic for {}".format(topic_name))


    def get_childer_inbound_edges(self, topic_name):

        parent_node = self.get_parent_topic(topic_name="Pareto distribution", parent_level = 1)
        self.get_all_sub_topics(topic_name=parent_node)



if __name__=="__main__":

    graph_api_h = Graph_API()
    
    graph_api_h.set_env_variables(  
                                    collection_name="Machine_Learning",\
                                    graph_name="Machine_Learning_Relations",\
                                    database_name="Data_Science"
                                )
    
    #graph_api_h.get_parent_topic(topic_name="Pareto distribution", parent_level = 1)

    #Not used in the current Graph Structure
    #graph_api_h.get_all_sub_topics(topic_name="Pareto distribution")

    #graph_api_h.get_all_other_sub_topics_of_a_topic(topic_name="Pareto distribution")

    graph_api_h.get_childer_inbound_edges(topic_name="Pareto distribution")