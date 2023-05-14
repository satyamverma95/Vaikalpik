import os
import sys
from Graph_traversals_API import Graph_API
from dotenv import load_dotenv

load_dotenv(os.sep.join([os.path.dirname(os.getcwd()), "Scraping", ".env"])) 

sys.path.insert(0, os.sep.join([os.path.dirname(os.getcwd()), os.getenv("SCRAPING_SCRIPT")]))
from json_manager import Json_Object



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

            parent_topic, similar_topcis = gapi_h.get_childer_inbound_edges(topic_name)
            print("parent_topic {}, similar_topcis: {}".format(parent_topic, similar_topcis))
            #self.topics_dict.add_record(topic_count, {}, self.topics_dict.dict_object)
            #self.topics_dict.add_record(self.title_kw, parent_topic, self.topics_dict.dict_object[topic_count])
            #self.topics_dict.add_record(self.subtopics_kw, {}, self.topics_dict.dict_object[topic_count])

            if (parent_topic not in self.topics_dict.dict_object):
                self.topics_dict.add_record(parent_topic, {}, self.topics_dict.dict_object)
                
                for similar_topic in similar_topcis:
                    self.topics_dict.add_record(similar_topic, "0", self.topics_dict.dict_object[parent_topic])
            
            
            self.topics_dict.update_record(topic_name, "1", self.topics_dict.dict_object[parent_topic])


        self.topics_dict.print_dict()
        
        return(self.topics_dict.dict_object)


    def post_result (self, data):
        pass
        



if __name__=="__main__":

    pre_h = Prerequisites()
    pre_h.grab_data()