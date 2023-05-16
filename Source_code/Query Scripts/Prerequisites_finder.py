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
        
        self.topics_dict    =   Json_Object()
        self.title_kw       =   "Title"
        self.subtopics_kw   =   "subtopics"

    def grab_data( self, data):

        processed_data = self.process_data(data)
        #self.post_result(data)

        return(processed_data)


    def process_data (self, data):

        #print("Data received", data)
        gapi_h = Graph_API()

        gapi_h.set_env_variables(  collection_name="Machine_Learning",\
                                    graph_name="Machine_Learning_Relations",\
                                    database_name="Data_Science"
                                )

        for topic_count, topic_name in enumerate(data["name"], start=1):

            parent_topic, parent_seq, similar_topics, similar_topics_seq = gapi_h.get_childer_inbound_edges(topic_name, level=1)
            #topic_seq = gapi_h.get_document_attribute(topic_name, "Sequence")
            print("parent_topic {}, topic Seq: {} similar_topics: {}".format(parent_topic, "", similar_topics))

            if (parent_topic not in self.topics_dict.dict_object):
                self.topics_dict.add_record(parent_topic, {}, self.topics_dict.ordered_dict_obj)

                for similar_topic, similar_topic_seq  in zip(similar_topics, similar_topics_seq):
                    self.topics_dict.add_record(similar_topic, "0", self.topics_dict.ordered_dict_obj[parent_topic])
            
           
            self.topics_dict.update_record(topic_name, "1", self.topics_dict.ordered_dict_obj[parent_topic])

        self.topics_dict.print_dict(self.topics_dict.ordered_dict_obj)
        
        return(self.topics_dict.ordered_dict_obj)


    def post_result (self, data):
        pass
        



if __name__=="__main__":

    pre_h = Prerequisites()
    pre_h.grab_data()