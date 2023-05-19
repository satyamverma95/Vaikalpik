from Query_engine import ArangoDB_Qurey_Engine

class Graph_API():
    def __init__(self):
        
        self.arangoDB_qurey_engine_h    =   ArangoDB_Qurey_Engine()
        self.subtopics_kw               =   "sub_topic"

    def set_env_variables(self, database_name, collection_name, graph_name):
        self.database_name      =   database_name
        self.collection_name    =   collection_name
        self.graph_name         =   graph_name


    def get_parent_topic(self, topic_name, parent_level=1, graph_name = None ):
        #############################
        # We need to follow protocol while using Query Enging API
        #   1) Always connect to the databse first. 
        #   2) Thsi will initialise the database handle in the script.
        ###############################

        if (graph_name is None):
            graph_name = self.graph_name

        self.arangoDB_qurey_engine_h.connect_to_db()
        doc_id = self.arangoDB_qurey_engine_h.get_collection_id( collection_name=self.collection_name,\
                                                                 topic_name=topic_name,\
                                                                 database_name=self.database_name )
        #print("Document Id ", doc_id)
        if (doc_id):
            parent_query = "FOR parent IN {} INBOUND @start_node GRAPH @graph_name RETURN parent".format(parent_level)
            results_list = self.arangoDB_qurey_engine_h.execute_traversal_query ( parent_query, collection=self.collection_name,\
                                                                            node_key= doc_id,\
                                                                            graph_name=graph_name,\
                                                                            database_name=self.database_name )
            if(len(results_list)>0):
                parent_topic = results_list[-1].Topic
                parent_seq   = results_list[-1].Sequence
                #print("Parent topic of {} is {}, sequence {}".format(topic_name, parent_topic,parent_seq ))
            else:
                print("Cuurently we don't have level {} Parent topic for {}".format( parent_level, topic_name))

        return ( parent_topic )

    def get_all_sub_topics(self, topic_name):
        
        self.arangoDB_qurey_engine_h.connect_to_db()
        doc_id = self.arangoDB_qurey_engine_h.get_collection_id( collection_name=self.collection_name,\
                                                                 topic_name=topic_name,\
                                                                 database_name=self.database_name )
        #print("Document Id ", doc_id)
        if (doc_id):
            all_child_query = "FOR node IN 1..1 OUTBOUND @start_node GRAPH @graph_name RETURN node"
            results_list = self.arangoDB_qurey_engine_h.execute_traversal_query ( all_child_query, collection=self.collection_name,\
                                                                                node_key= doc_id,\
                                                                                graph_name=self.graph_name,\
                                                                                database_name=self.database_name )
            if(len(results_list)>0):
                sorted_sub_topics = sorted(results_list, key=lambda x: tuple(map(int, x['Sequence'].split('.'))))
                sub_topics_list =  [doc['Topic'] for doc in sorted_sub_topics]
                sub_topics_seq_list = [doc['Sequence'] for doc in sorted_sub_topics]
                sub_topics = ", ".join(["-".join([doc['Topic'], doc['Sequence']]) for doc in sorted_sub_topics])
                #print("Sub topics of \"{}\" are : {}".format(topic_name, sub_topics))
            else:
                sub_topics_list= []
                sub_topics_seq_list = []
                print("Currently we don't have any sub topic for {}".format(topic_name))

        return (sub_topics_list)


    def get_all_neighbours_of_a_topic(self, topic_name, graph_name=None):

        if (graph_name is None):
            graph_name = self.graph_name
        
        self.arangoDB_qurey_engine_h.connect_to_db()
        doc_id = self.arangoDB_qurey_engine_h.get_collection_id( collection_name=self.collection_name,\
                                                                 topic_name=topic_name,\
                                                                 database_name=self.database_name )
        #print("Document Id ", doc_id)
        if (doc_id):
            all_child_query =   """FOR v1, e1, p1 IN 1..1 INBOUND @start_node GRAPH @graph_name
                                FOR v2, e2, p2 IN 1..1 OUTBOUND v1 GRAPH @graph_name 
                                    FILTER e1.label == "{}"
                                    FILTER e2.label == "{}"
                                    FILTER v2._id != @start_node
                                    RETURN v2
                                """.format(self.subtopics_kw, self.subtopics_kw)
            results_list = self.arangoDB_qurey_engine_h.execute_traversal_query ( all_child_query, collection=self.collection_name,\
                                                                                node_key = doc_id,\
                                                                                graph_name = graph_name,\
                                                                                database_name = self.database_name )
            if(len(results_list)>0):
                sorted_sub_topics = sorted(results_list, key=lambda x: tuple(map(int, x['Sequence'].split('.'))))
                sub_topics_list =  [doc['Topic'] for doc in sorted_sub_topics]
                sub_topics_seq_list = [doc['Sequence'] for doc in sorted_sub_topics]
                sub_topics = ", ".join(["-".join([doc['Topic'], doc['Sequence']]) for doc in sorted_sub_topics])
                #print("Neighbour topics of \"{}\" are : {}".format(topic_name, sub_topics))
            else:
                sub_topics_list= []
                sub_topics_seq_list = []
                print("Currently we don't have any Neighbours topic for {}".format(topic_name))

        return ( sub_topics_list )



    def get_all_other_sub_topics_of_a_topic__(self, topic_name):
        
        self.arangoDB_qurey_engine_h.connect_to_db()
        doc_id = self.arangoDB_qurey_engine_h.get_collection_id( collection_name=self.collection_name,\
                                                                 topic_name=topic_name,\
                                                                 database_name=self.database_name )
        print("Document Id ", doc_id)
        if (doc_id):
            all_child_neighbour_query = "FOR v, e IN 2..2 OUTBOUND @start_node GRAPH @graph_name  FILTER e.label == \"sub_topic\" RETURN  v"
          
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


    def get_children_inbound_edges(self, topic_name, level):

        parent_node, parent_seq = self.get_parent_topic(topic_name=topic_name, parent_level = level)
        subtopics_names, subtopics_seq = self.get_all_sub_topics(topic_name=parent_node)

        print( "Parent Topic :{} and Subtopics : {}".format(parent_node, subtopics_names) )
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
    
    def get_IN_Edges_Nodes(self, topic_name, attribute_name="_key"):
        
        self.arangoDB_qurey_engine_h.connect_to_db()

        doc_id = self.arangoDB_qurey_engine_h.get_collection_id(collection_name=self.collection_name,
                                                                topic_name=topic_name,
                                                                database_name=self.database_name)

        if (doc_id):
            starting_node_key = "{}/{}".format(self.collection_name, doc_id)
            traversal_query = """
            LET startingNode = DOCUMENT('{}')
            FOR v, e, p IN 1..1 OUTBOUND startingNode._id GRAPH '{}'
                FILTER e.label == 'IN'
                RETURN v
            """.format(starting_node_key, self.graph_name)

            results = self.arangoDB_qurey_engine_h.execute_document_query(traversal_query, database_name=self.database_name)

            if len(results) > 0:
                sorted_neighbour_topics = sorted(results, key=lambda x: tuple(map(int, x['Sequence'].split('.'))))
                result_list = [doc[attribute_name] for doc in sorted_neighbour_topics]
                #print("Pre-requisites of topics {} are {}".format(topic_name, result_list))
            else:
                result_list = []
                print("Currently, we don't have OUT Nodes from node {} ".format(topic_name))

        return result_list


    def get_OUT_Edges_Nodes(self, topic_name, attribute_name="_key", graph_name=None):
        
        if (graph_name is None):
            graph_name = self.graph_name

        self.arangoDB_qurey_engine_h.connect_to_db()

        doc_id = self.arangoDB_qurey_engine_h.get_collection_id(collection_name=self.collection_name,
                                                                topic_name=topic_name,
                                                                database_name=self.database_name)

        #print("Machine Learning Collection",self.collection_name , graph_name, topic_name)
        if (doc_id):
            starting_node_key = "{}/{}".format(self.collection_name, doc_id)
            traversal_query = """
            LET startingNode = DOCUMENT('{}')
            FOR v, e, p IN 1..1 OUTBOUND startingNode._id GRAPH '{}'
                FILTER e.label == 'OUT'
                RETURN v
            """.format(starting_node_key, graph_name)

            results = self.arangoDB_qurey_engine_h.execute_document_query(traversal_query, database_name=self.database_name)
            #print("Result Found", results)

            if len(results) > 0:
                sorted_neighbour_topics = sorted(results, key=lambda x: tuple(map(int, x['Sequence'].split('.'))))
                result_list = [doc[attribute_name] for doc in sorted_neighbour_topics]
                #print("forward topics of {} are {}".format(topic_name, result_list))
            else:
                result_list = []
                print("Currently, we don't have OUT Nodes from node {} ".format(topic_name))

        return result_list
    


    def check_if_out_edges_exits(self, topic_name ):
        
        self.arangoDB_qurey_engine_h.connect_to_db()

        doc_id = self.arangoDB_qurey_engine_h.get_collection_id(collection_name=self.collection_name,
                                                                topic_name=topic_name,
                                                                database_name=self.database_name)

        if (doc_id):
            starting_node_key = "{}/{}".format(self.collection_name, doc_id)
            traversal_query = """
            LET node = DOCUMENT(@start_node)
                LET outboundEdges = (
                    FOR v, e IN OUTBOUND node GRAPH @graph_name
                    FILTER e.label == "OUT"
                    RETURN e
                )
                RETURN COUNT(outboundEdges)
            """
            #.format( starting_node_key )

            #print("starting_node_key :{}, doc_id :{}".format( starting_node_key, doc_id ) )

            results_list = self.arangoDB_qurey_engine_h.execute_traversal_query ( traversal_query, collection=self.collection_name,\
                                                                                node_key= doc_id,\
                                                                                graph_name=self.graph_name,\
                                                                                database_name=self.database_name )
            if (results_list.result):
                no_of_out_edges = results_list.result[-1]
                #print( "No of out edges received : {}".format(no_of_out_edges))
                
                return (no_of_out_edges)





if __name__=="__main__":

    graph_api_h = Graph_API()
    
    graph_api_h.set_env_variables(  
                                    collection_name="Machine_Learning",\
                                    graph_name="Machine_Learning_Ontology",\
                                    database_name="Data_Science"
                                )
    
    #graph_api_h.get_parent_topic(topic_name="Pareto distribution", parent_level = 1)

    #Not used in the current Graph Structure
    #graph_api_h.get_all_sub_topics(topic_name="Some common continuous distributions")

    #graph_api_h.get_all_neighbours_of_a_topic(topic_name="Regression")

    #graph_api_h.get_children_inbound_edges(topic_name="Pareto distribution", level = 1)

    #graph_api_h.get_document_attribute("Supervised learning", attribute_name="Sequence")
    graph_api_h.get_IN_Edges_Nodes(topic_name="Unsupervised learning", attribute_name="Topic")
    #graph_api_h.get_OUT_Edges_Nodes(topic_name="Supervised learning", attribute_name="Topic")

    #graph_api_h.check_if_out_edges_exits(topic_name="A brief review of probability theory")