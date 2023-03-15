import json
import os 


class Json_Object:
    def __init__ ( self ):
        self.dict_object    =   dict()
        self.cwd            =   os.getcwd()

    def add_record(self, key, value, dictionary):

        if ( key not in dictionary):
            dictionary[ key ] = value

    def delete_record (self, key, value, dictionary):

        if ( key in dictionary):
           del dictionary[ key ]

    def print_dict (self, dictionary) :
        print (dictionary)

    def write_to_file(self, data, filename):

        with open( filename, "w", encoding='utf-8') as f:
            data = json.dumps(data)
            f.write(str(data))

    def load_json (self, filename):

        f_h = open(filename)

        self.cuisine_names = json.load(f_h)
      

