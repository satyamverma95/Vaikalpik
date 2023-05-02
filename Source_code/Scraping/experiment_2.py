import json
from pyArango.connection import Connection
from pyArango.collection import Collection, Field
from pyArango.graph import Graph, EdgeDefinition

# connect to the database
conn = Connection(username="root", password="iluvu00")
db = conn["Data_Science"]

# define the Topic vertex collection
class Topic(Collection):
    _fields = {
        "Title": Field(),
        "id": Field()
    }

# define the SubTopic vertex collection
class SubTopic(Collection):
    _fields = {
        "Title": Field(),
        "id": Field()
    }

# define the relationship edge
class HasSubTopic(EdgeDefinition):
    _fields = {
        "order": Field()
    }

# define the Topic-SubTopic graph
class TopicGraph:
    def __init__(self, db, jsonInit=None):
        _edgeDefinitions = [HasSubTopic]
        _orphanedCollections = []

# create the Topic-SubTopic graph
graph = TopicGraph(db)

json_data = '''
{
  "1": {
    "Title": "Introduction",
    "Sub Topics": {
      "1.1": {
        "Title": "Machine learning: what and why?",
        "Sub Topics": {
          "1.1.1": {
            "Title": "Types of machine learning"
          }
        }
      },
      "1.2": {
        "Title": "Supervised learning",
        "Sub Topics": {
          "1.2.1": {
            "Title": "Classification"
          },
          "1.2.2": {
            "Title": "Regression"
          }
        }
      }
    }
  },
  "2": {
    "Title": "Probability",
    "Sub Topics": {
      "2.1": {
        "Title": "Introduction",
        "Sub Topics": {}
      },
      "2.2": {
        "Title": "A brief review of probability theory",
        "Sub Topics": {
          "2.2.1": {
            "Title": "Discrete random variables"
          },
          "2.2.5": {
            "Title": "Continuous random variables"
          }
        }
      }
    }
  }
}
'''

#load the JSON data
data = json.loads(json_data)

# define a function to insert a topic and its subtopics recursively
def insert_topic(topic, parent=None):
    # insert the topic vertex
    topic_v = Topic(graph)
    topic_v["Title"] = topic["Title"]
    topic_v["id"] = list(data.keys()).index(topic["Title"]) + 1
    topic_v.save()

    # if a parent is provided, create a relationship between the parent and the topic
    if parent is not None:
        edge = HasSubTopic(graph)
        edge["_from"] = parent._id
        edge["_to"] = topic_v._id
        edge["order"] = list(parent["Sub Topics"].keys()).index(topic["id"])
        edge.save()

    # recursively insert the subtopics
    for subtopic in topic["Sub Topics"].values():
        insert_topic(subtopic, parent=topic_v)

# insert each topic and its subtopics into the database
for topic in data.values():
    insert_topic(topic)
