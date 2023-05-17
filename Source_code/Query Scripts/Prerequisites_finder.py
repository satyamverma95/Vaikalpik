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
        
        self.topics_dict        =   Json_Object()
        self.title_kw           =   "Title"
        self.subtopics_kw       =   "subtopics"
        self.forward_topics     =   set()
        self.input_data_set     =   set()
        self.recommended_topics =   set()

    def grab_data( self, data):

        processed_data = self.process_data(data)

        return(processed_data)


    def process_data (self, data):

        #print("Data received", data)
        gapi_h = Graph_API()
        
        self.input_data_set = set(data["name"])

        gapi_h.set_env_variables(  collection_name="Machine_Learning",\
                                    graph_name="Machine_Learning_Relations",\
                                    database_name="Data_Science"
                                )
        

        for topic_count, topic_name in enumerate(data["name"], start=1):

            #parent_topic, parent_seq, similar_topics, similar_topics_seq = gapi_h.get_childer_inbound_edges(topic_name, level=1)
            
            #Using OUT Neighbours edges to get all the forwards nodes of a topic.
            fwd_topics_for_a_topic  =   gapi_h.get_OUT_Edges_Nodes(topic_name, attribute_name="Topic")
            self.forward_topics.update(fwd_topics_for_a_topic)
            
            if topic_name in self.forward_topics:
                print( "Topic Name : {} is found in forward topics, removing them".format(topic_name) )
                self.forward_topics.remove(topic_name)
            

            for fwd_topic in self.forward_topics:
            
                prerequisite_for_a_topic  =   gapi_h.get_IN_Edges_Nodes(fwd_topic, attribute_name="Topic")

                if ( self.is_prerequisite_already_covered( set(prerequisite_for_a_topic) ) ):
                    self.recommended_topics.add(fwd_topic)
                    print("Recommending {} as its prerequisite are already done".format(fwd_topic))

            
            '''
            print("parent_topic {}, topic Seq: {} similar_topics: {}".format(parent_topic, "", similar_topics))

            if (parent_topic not in self.topics_dict.dict_object):
                self.topics_dict.add_record(parent_topic, {}, self.topics_dict.ordered_dict_obj)

                for similar_topic, similar_topic_seq  in zip(similar_topics, similar_topics_seq):
                    self.topics_dict.add_record(similar_topic, "0", self.topics_dict.ordered_dict_obj[parent_topic])
            
           
            self.topics_dict.update_record(topic_name, "1", self.topics_dict.ordered_dict_obj[parent_topic])

        self.topics_dict.print_dict(self.topics_dict.ordered_dict_obj)
        '''
        print("All Recommenmded Topics {}".format(self.recommended_topics))
        return(self.topics_dict.ordered_dict_obj)        


    def is_prerequisite_already_covered (self, pre_of_a_topic):

        if pre_of_a_topic.issubset(self.input_data_set):
            return (True)

        return(False)


if __name__=="__main__":

    pre_h = Prerequisites()
    pre_h.grab_data()