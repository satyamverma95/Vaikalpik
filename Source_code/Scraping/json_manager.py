import json
import os
from collections import OrderedDict
 


class Json_Object:
    def __init__ ( self ):
        self.dict_object        =   dict()
        self.ordered_dict_obj   =   OrderedDict()
        self.cwd                =   os.getcwd()

    def add_record(self, key, value, dictionary):

        if ( key not in dictionary):
            dictionary[ key ] = value

    def update_record (self, key, value, dictionary):
    
        dictionary[ key ] = value

    def delete_record (self, key, value, dictionary):

        if ( key in dictionary):
           del dictionary[ key ]

    def print_dict (self, dict) :
        print (dict)

    def write_to_file(self, data, filename):

        with open( filename, "w", encoding='utf-8') as f:
            data = json.dumps(data)
            f.write(str(data))

    def load_json (self, filename):

        f_h = open(filename)

        self.dict_object = json.load(f_h)
      

