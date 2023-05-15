from Query_engine import ArangoDB_Qurey_Engine

class Graph_API():
    def __init__(self):
        
        self.arangoDB_qurey_engine_h = ArangoDB_Qurey_Engine()

    def set_env_variables(self, database_name, collection_name, graph_name):
        self.database_name      =   database_name
        self.collection_name    =   collection_name
        self.graph_name         =   graph_name


    def get_parent_topic(self, topic_name, parent_level=1):
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
                parent_seq   = results_list[-1].Sequence
                print("Parent topic of {} is {}, sequence {}".format(topic_name, parent_topic,parent_seq ))
            else:
                print("Cuurently we don't have level {} Parent topic for {}".format( parent_level, topic_name))

        return (parent_topic, parent_seq)

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
                sub_topics_list =  [doc['Topic'] for doc in sorted_sub_topics]
                sub_topics_seq_list = [doc['Sequence'] for doc in sorted_sub_topics]
                sub_topics = ", ".join(["-".join([doc['Topic'], doc['Sequence']]) for doc in sorted_sub_topics])
                print("Sub topics of \"{}\" are : {}".format(topic_name, sub_topics))
            else:
                sub_topics_list= []
                sub_topics_seq_list = []
                print("Currently we don't have any sub topic for {}".format(topic_name))

        return (sub_topics_list, sub_topics_seq_list)

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
                #print("Neighbours of \"{}\" are : {}".format(topic_name, neighbour_topics))
            else:
                print("Currently we don't have any sub topic for {}".format(topic_name))


    def get_childer_inbound_edges(self, topic_name, level):

        parent_node, parent_seq = self.get_parent_topic(topic_name=topic_name, parent_level = level)
        subtopics_names, subtopics_seq = self.get_all_sub_topics(topic_name=parent_node)

        return (parent_node, parent_seq, subtopics_names, subtopics_seq)


    def get_document_attribute(self, topic_name, attribute_name="_key"):

        self.arangoDB_qurey_engine_h.connect_to_db()

        doc_id = self.arangoDB_qurey_engine_h.get_collection_id( collection_name=self.collection_name,\
                                                                 topic_name=topic_name,\
                                                                 database_name=self.database_name )

        if (doc_id):
            parent_query = "FOR doc IN {} FILTER doc._id == \"{}/{}\" RETURN doc".format( self.collection_name, self.collection_name, doc_id)
            results = self.arangoDB_qurey_engine_h.execute_document_query ( parent_query, database_name=self.database_name )
           
            if(len(results)>0):
                result_list = [doc[attribute_name] for doc in results]
                sequence = result_list[0]
                print("{} of the document is {}".format(attribute_name, sequence))
            else:
                print("Cuurently we don't have {} attributr in the collection".format(attribute_name))

        return(sequence)

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

    #graph_api_h.get_childer_inbound_edges(topic_name="Pareto distribution", level = 1)

    graph_api_h.get_document_attribute("Supervised learning", attribute_name="Sequence")