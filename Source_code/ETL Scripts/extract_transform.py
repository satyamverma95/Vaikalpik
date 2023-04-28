import sys
import os 
from dotenv import load_dotenv

load_dotenv(os.sep.join([os.getcwd(), "Source_code", "Scraping", ".env"])) #nned to change the location of .env file.

sys.path.insert(0, os.sep.join([os.getcwd(), os.getenv("SOURCE_DIR"), os.getenv("ARANGODB_DIR")])) ##Need to find better way to do this.
from Arangodb_APIs import ArangoDB 

sys.path.insert(0, os.sep.join([os.getcwd(), os.getenv("SOURCE_DIR"), os.getenv("SCRAPING_SCRIPT")]))
from resources import Machine_Learning
from file_path_manager import File_Path_Manager

import json



class extract_transform:
    def __init__ ( self ):
        self.a_db               =   ArangoDB()
        self.books_index_dict   =   ""

    def read_json(self, filename):
        self.books_index_dict = json.load(open(filename))
        #return (book_json)

    def connect_to_graph_db (self):
        self.a_db.connect_to_db()     

    def create_new_database(self, data_base="_system"):
        self.a_db.create_database(databasename=data_base)

    def create_new_collections(self, data_base="_system", collection_name="default"):
        self.a_db.create_collection(database_name=data_base, collection_name=collection_name)
    
    def add_document(self, collection="", document_to_add=""):
        self.a_db.add_document(collection_name=collection, document=document_to_add)

    def delete_collections(self, collection):
        self.a_db.delete_colection(collection_name=collection)

    def change_file_extension_to_json(self, filename, new_string ="", sep="_"):

        filename_parts = filename.split(".")
        filename_parts_without_extension = filename_parts[:-1][-1]
        #print("filename_parts_without_extension inside function", filename_parts_without_extension)
        filename_parts_without_extension = filename_parts_without_extension + sep + new_string
        #print("filename_parts_without_extension with new name", filename_parts_without_extension)
        filename_parts[:-1] = [filename_parts_without_extension]
        filename_parts[-1] = "json"

        return (".".join(filename_parts)) 

    def create_arango_object (self, title):

        doc =   {
                    'Topic' : title,
                }

        return (doc)

    def setup_arango_env(self):

        self.connect_to_graph_db()
        self.create_new_database(data_base="Data_Science")
        self.create_new_collections(data_base="Data_Science", collection_name="Machine_Learning") 

    def transform_json_data(self):
        
        for section in self.books_index_dict.values():
            
            #print(section["Title"])
            document = self.create_arango_object(section["Title"])
            self.add_document(collection="Machine_Learning", document_to_add=document)
            
            for sub_section in section["Sub Topics"].values():
                
                print(sub_section["Title"])
                document = self.create_arango_object(sub_section["Title"])
                self.add_document(collection="Machine_Learning", document_to_add=document)
                
                for sub_sub_section in sub_section["Sub Topics"].values():
                    
                    print(sub_sub_section["Title"])
                    document = self.create_arango_object(sub_sub_section["Title"])
                    self.add_document(collection="Machine_Learning", document_to_add=document)


def main():
        
    file_manager_h      =   File_Path_Manager()
    extract_transform_h =   extract_transform()

   

    for index, books in enumerate(Machine_Learning["Books"]):
        books_json_folder = file_manager_h.get_book_json_dir()
        if (Machine_Learning["Books"][str(index)]["Scrape"]):
            json_filename = extract_transform_h.change_file_extension_to_json (Machine_Learning["Books"][str(index)]["Name"], new_string ="Index")
            #print(os.path.join(books_json_folder, Machine_Learning["Books"][str(index)]["Name"]))
            #print(os.path.join(books_json_folder,json_filename))
            extract_transform_h.read_json(os.path.join(books_json_folder,json_filename)) 
            extract_transform_h.setup_arango_env()
            #extract_transform_h.delete_collections("Machine_Learning")
            extract_transform_h.transform_json_data()
            


if __name__ == "__main__":
   
    main()

    #extract_transform_h = extract_transform()
    #extract_transform_h.connect_to_graph_db()
    #extract_transform_h.create_new_database(data_base="Data_Science")
    #extract_transform_h.create_new_collections(data_base="Data_Science", collection_name="Machine_Learning") 
    #extract_transform_h.add_document(collection="Machine_Learning", document_to_add="")