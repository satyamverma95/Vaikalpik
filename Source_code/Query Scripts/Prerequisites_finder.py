import os
import sys
from Graph_traversals_API import Graph_API
from dotenv import load_dotenv

load_dotenv(os.sep.join([os.path.dirname(os.getcwd()), "Scraping", ".env"])) 

sys.path.insert(0, os.sep.join([os.path.dirname(os.getcwd()), os.getenv("SCRAPING_SCRIPT")]))
from json_manager import Json_Object



class Prerequisites():
    def __init__(self):
        
        self.var = ""

    def grab_data (self, data):

        #print("Data received", data)
        gapi_h = Graph_API()
        gapi_h.set_env_variables(  collection_name="Machine_Learning",\
                                    graph_name="Machine_Learning_Relations",\
                                    database_name="Data_Science"
                                )
        topics_dict = Json_Object()
        title_kw        =   "Title"
        subtopics_kw    =   "subtopics"

        for topic_count, topic_name in enumerate(data["name"]):

            parent_topic, similar_topcis = gapi_h.get_childer_inbound_edges(topic_name)
            print("parent_topic {}, similar_topcis: {}".format(parent_topic, similar_topcis))
            topics_dict.add_record(topic_count, {}, topics_dict.dict_object)
            topics_dict.add_record(title_kw, parent_topic, topics_dict.dict_object[topic_count])
            topics_dict.add_record(subtopics_kw, {}, topics_dict.dict_object[topic_count])

            for similar_topic in similar_topcis:
                print("Adding similar topics", similar_topic)
                if (topic_name in similar_topic):
                    topics_dict.add_record(similar_topic, "1", topics_dict.dict_object[topic_count][subtopics_kw])
                else:
                    topics_dict.add_record(similar_topic, "0", topics_dict.dict_object[topic_count][subtopics_kw])

        topics_dict.print_dict()


if __name__=="__main__":

    pre_h = Prerequisites()
    pre_h.grab_data()