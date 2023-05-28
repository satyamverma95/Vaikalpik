import os
import sys
from Graph_traversals_API import Graph_API
from dotenv import load_dotenv

load_dotenv(os.sep.join([os.path.dirname(os.getcwd()), "Scraping", ".env"])) 

sys.path.insert(0, os.sep.join([os.path.dirname(os.getcwd()), os.getenv("SCRAPING_SCRIPT")]))
from json_manager import Json_Object
from Query_engine import ArangoDB_Qurey_Engine


class Prerequisites():
    def __init__(self):
        
        self.topics_dict            =   Json_Object()
        self.title_kw               =   "Title"
        self.subtopics_kw           =   "subtopics"
        self.forward_topics         =   set()
        self.input_data_set         =   set()
        self.recommended_topics     =   set()
        self.ontology_graph_name    =   "Machine_Learning_Ontology"
        self.dependency_graph_name  =   "Machine_Learning_Dependency"

    def grab_data( self, data):

        processed_data = self.process_data(data)

        return(processed_data)


    def process_data (self, data):

        #print("Data received", data)
        self.gapi_h = Graph_API()
        
        self.input_data_set = set(data["name"])

        self.gapi_h.set_env_variables(  collection_name="Machine_Learning",\
                                    graph_name="Machine_Learning_Dependency",\
                                    database_name="Data_Science"
                                )
        

        for topic_count, topic_name in enumerate(data["name"], start=1):

            #parent_topic, parent_seq, similar_topics, similar_topics_seq = gapi_h.get_childer_inbound_edges(topic_name, level=1)
            
            neighbours_of_node  =   self.gapi_h.get_all_neighbours_of_a_topic(topic_name, graph_name=self.ontology_graph_name)
            
            print("DEBUG - Neighbours of the '{}' are : {}".format(topic_name, neighbours_of_node))

            if ( neighbours_of_node.issubset( self.input_data_set) ):
                
                print("DEBUG - All the neighbours of the topic '{}' are covered by the student.".format(topic_name))

                parent_node = self.check_parent_with_out_edges( topic_name )
                #print("DEBUG - Parent of the topic is - {}".format(parent_node))

                if( parent_node not in self.input_data_set ):
                    fwd_topics_for_a_topic  =   self.gapi_h.get_OUT_Edges_Nodes(parent_node, attribute_name="Topic", graph_name=self.dependency_graph_name)
                    self.input_data_set.add(parent_node)
                    self.forward_topics.update(fwd_topics_for_a_topic)
                    print("DEBUG - Updated Forward topics of '{}' are : {}".format( parent_node, self.forward_topics ) )

            #Using OUT Neighbours edges to get all the forwards nodes of a topic.
            fwd_topics_for_a_topic  =   self.gapi_h.get_OUT_Edges_Nodes(topic_name, attribute_name="Topic")
            self.forward_topics.update(fwd_topics_for_a_topic)
            
            print("DEBUG - All Forward topics of are : {}".format( self.forward_topics ) )


        if self.forward_topics.intersection(self.input_data_set):
            print( "DEBUG - Topic Name : {} is found in forward topics, removing them".format(topic_name) )
            self.forward_topics.difference_update(self.input_data_set)
            

        print("DEBUG - All final forward Topics are :{}".format(self.forward_topics))
        

        for fwd_topic in self.forward_topics:
        
            prerequisite_for_a_topic  =   self.gapi_h.get_IN_Edges_Nodes(fwd_topic, attribute_name="Topic")
            print( "DEBUG - prerequisite of '{}' are : {}".format( fwd_topic, prerequisite_for_a_topic ) )

            if ( self.is_prerequisite_already_covered( set(prerequisite_for_a_topic) ) ):
                self.recommended_topics.add(fwd_topic)
        
        print("DEBUG - Recommending {} as its prerequisite are already done".format(self.recommended_topics))

        '''
        self.gapi_h.set_env_variables(collection_name="Machine_Learning",\
                                    graph_name="Machine_Learning_Ontology",\
                                    database_name="Data_Science"
                                    )
        '''
        for rec_topic in self.recommended_topics:
            parent_topic  =   self.gapi_h.get_parent_topic(rec_topic, graph_name = self.ontology_graph_name)
        
            print("parent_topic {}, for recommended topic : {}".format(parent_topic, rec_topic))

            if (parent_topic not in self.topics_dict.dict_object):
                self.topics_dict.add_record(parent_topic, {}, self.topics_dict.ordered_dict_obj)
                self.topics_dict.add_record(rec_topic, "0", self.topics_dict.ordered_dict_obj[parent_topic])
            
            
            #self.topics_dict.update_record(topic_name, "1", self.topics_dict.ordered_dict_obj[parent_topic])

        self.topics_dict.print_dict(self.topics_dict.ordered_dict_obj)
        print("All Recommenmded Topics {}".format(self.recommended_topics))
        
        
        return(self.topics_dict.ordered_dict_obj)        


    def is_prerequisite_already_covered (self, pre_of_a_topic):

        print("DEBUG - Checking Pre-requisite of a topic are covered")
        print("DEBUG - Pre-req : {}, topic covered : {}".format( pre_of_a_topic, self.input_data_set ))

        if pre_of_a_topic.issubset(self.input_data_set):
            print("DEBUG - Pre-requisite all covered")
            return (True)

        print("DEBUG - Pre-requisite not covered")
        return(False)


    def check_parent_with_out_edges(self, topic_name):

        parent_node = self.gapi_h.get_parent_topic(topic_name, graph_name = self.ontology_graph_name)
        
        no_of_out_edges = self.gapi_h.check_if_out_edges_exits( parent_node )
        #print("no of out edges received", no_of_out_edges)

        if no_of_out_edges != 0:
                print("DEBUG - Returning Parent node :'{}' having {} out nodes".format(parent_node, no_of_out_edges))
                return (parent_node)
        else:
            self.check_parent_with_out_edges(parent_node)


if __name__=="__main__":

    pre_h = Prerequisites()
    pre_h.grab_data()