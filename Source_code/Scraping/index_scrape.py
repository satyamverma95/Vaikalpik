from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen
import re
import os
import PyPDF2
from file_path_manager import File_Path_Manager
from resources import Machine_Learning
from json_manager import Json_Object
import json
from tika import parser 
import pypdf
import ssl 

class Scrapper:
    def __init__ (self):

        #Decalring the variables
        self.books_dict_h       =   Json_Object()
        self.table              =   pd.DataFrame()
        self.file_manager_h     =   File_Path_Manager()
         
        
    def read_book(self, filename):
        
        with open(filename, 'r') as f:
            self.book_content = f.read()

        print(self.book_content)

    
    def read_json(self, filename):
        self.books_dict_h = json.load(open(filename))
        #return (book_json)


    def json_exists (self, filename):

       return ( os.path.exists(filename) )

    def change_file_extension_to_json(self, filename, new_string ="", sep=""):

        filename_parts = filename.split(".")
        filename_parts_without_extension = filename_parts[:-1][-1]
        #print("filename_parts_without_extension inside function", filename_parts_without_extension)
        filename_parts_without_extension = filename_parts_without_extension + sep + new_string
        #print("filename_parts_without_extension with new name", filename_parts_without_extension)
        filename_parts[:-1] = [filename_parts_without_extension]
        filename_parts[-1] = "json"

        return (".".join(filename_parts)) 

    def check_if_index_page(self, page_content):
        
        if ("contents" in page_content.lower()):
            #print("Page", page_content)
            return (True)

        return(False)


    def compare_versions(version1, version2):
        # Split the version strings into their individual parts
        v1_parts = [int(part) for part in version1.split('.')]
        v2_parts = [int(part) for part in version2.split('.')]

        # Pad the shorter version number with zeros so that both have the same length
        if len(v1_parts) < len(v2_parts):
            v1_parts += [0] * (len(v2_parts) - len(v1_parts))
        elif len(v2_parts) < len(v1_parts):
            v2_parts += [0] * (len(v1_parts) - len(v2_parts))

        # Compare the parts of the version numbers from left to right
        for i in range(len(v1_parts)):
            if v1_parts[i] < v2_parts[i]:
                return -1
            elif v1_parts[i] > v2_parts[i]:
                return 1

        # If all parts are equal, the versions are the same
        return 0


    def check_if_major_topic(self, version):

        v_parts = [int(part) for part in version.split('.')]

        if (len(v_parts) == 1):
            return (True)
        
        return (False)

    def check_if_sub_topics(self, version):

        v_parts = [int(part) for part in version.split('.')]

        if (len(v_parts) == 2):
            return (True)
        
        return (False)


    def get_parent_index(self, version, level = 1):

        v_parts = [str(part) for part in version.split('.')]
        for i in range(level):
            popped_element = v_parts.pop()

        return(".".join(v_parts))


    def pdf_reader(self, filename, book_name):
        
        with open(filename, 'rb') as pdf_file:

            pdf_reader = PyPDF2.PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)

            self.books_dict_h.add_record("Name", book_name, self.books_dict_h.dict_object)
            self.books_dict_h.add_record("Pages", {}, self.books_dict_h.dict_object)
            
            # Loop through each page and print the page text
            for page_no in range(num_pages):
                page = pdf_reader.pages[page_no]
                page_content = page.extract_text()
                #page_content = " ".join(page_content.replace(u".", "").strip())
                self.books_dict_h.add_record(page_no, page_content, self.books_dict_h.dict_object['Pages'])
                #print(page.extract_text())
            
            #self.books_dict_h.print_dict(self.books_dict_h.dict_object)
            data_dict_dir = self.file_manager_h.get_book_json_dir()
            #print(os.path.join(data_dict_dir,book_name.split('.')[0]))
            self.books_dict_h.write_to_file(self.books_dict_h.dict_object, os.path.join(data_dict_dir,".".join([book_name.split(".")[0], "json"])))


    def pdf_reader_tika(self, filename, book_name):
        
        
        pdf_reader = pypdf.PdfReader(filename)

        self.books_dict_h.add_record("Name", book_name, self.books_dict_h.dict_object)
        self.books_dict_h.add_record("Pages", {}, self.books_dict_h.dict_object)
        
        # Loop through each page and print the page text
        for page_no, page in enumerate(pdf_reader.pages):
            page_content = page.extract_text() + "\n"
            #page_content = " ".join(page_content.replace(u".", "").strip())
            self.books_dict_h.add_record(page_no, page_content, self.books_dict_h.dict_object['Pages'])
            #print(page.extract_text())
        
        #self.books_dict_h.print_dict(self.books_dict_h.dict_object)
        data_dict_dir = self.file_manager_h.get_book_json_dir()
        #print(os.path.join(data_dict_dir,book_name.split('.')[0]))
        self.books_dict_h.write_to_file(self.books_dict_h.dict_object, os.path.join(data_dict_dir,".".join([book_name.split(".")[0], "json"])))




    def scrape_index (self, filename):
         
        json_dir            =   self.file_manager_h.get_book_json_dir()
        book_name           =   filename.split(os.path.sep)[-1]
        json_filename       =   self.change_file_extension_to_json(book_name)
        #print("json_filename", json_filename)
        json_filename_fp    =   os.path.join(json_dir,json_filename)
        intro_json_filename =   self.change_file_extension_to_json(book_name, new_string="Index", sep = "_")
        #print("intro_json_filename", intro_json_filename)
        intro_json_filename =   os.path.join(json_dir, intro_json_filename)
        print("intro_json_filename with  dir", intro_json_filename)
        index_struct_json   =   Json_Object()
        sub_topics_kw       =   "Sub Topics"    
        title_kw            =   "Title"

        
        #Check if the file exists
        if (not self.json_exists(json_filename_fp)):
            print("JSON version of book not available. Doing the processing. Please wait....")
            self.pdf_reader_tika(filename, book_name)
        
        self.read_json(json_filename_fp)
        
        for page, content in self.books_dict_h["Pages"].items():
            
            if (int(page) <= 10):
                if (self.check_if_index_page(content)):

                    sections = content.split('\n')[1:]
                    print("Sections :", sections)
                    pattern = re.compile(r'^([\d.]+) (.+) (\d+)$')

                    #print("Sections", sections)
                    for section in sections:
                        match = pattern.search(section)
                        try :
                            if match:
                                section = match.group(1)
                                title = match.group(2).replace(".", "").strip()
                                page = match.group(3)
                                #print("Section:{}, Title:{}, Page:{}".format(section, title, page))

                                
                                if ( self.check_if_major_topic(section) ):
                                    #print("Inside IF loop")
                                    index_struct_json.add_record(section, {}, index_struct_json.dict_object)
                                    index_struct_json.add_record(title_kw, title, index_struct_json.dict_object[section])
                                    #print(type(index_struct_json.dict_object))
                                    index_struct_json.add_record(sub_topics_kw, {}, index_struct_json.dict_object[section])
                                    #index_struct_json.print_dict()
                                
                                elif (self.check_if_sub_topics(section)):
                                    #print("Inside Else If Loop")
                                    #index_struct_json.print_dict() 
                                    parent_section = self.get_parent_index(section)
                                    #print("parent Section", parent_section)
                                    index_struct_json.add_record(section, {}, index_struct_json.dict_object[parent_section][sub_topics_kw])
                                    index_struct_json.add_record(title_kw, title, index_struct_json.dict_object[parent_section][sub_topics_kw][section])
                                    index_struct_json.add_record(sub_topics_kw, {}, index_struct_json.dict_object[parent_section][sub_topics_kw][section])
                                else:
                                    #print("Inside Else Loop")
                                    #index_struct_json.print_dict() 
                                    parent_1_section = self.get_parent_index(section)
                                    parent_2_section = self.get_parent_index(section, 2)
                                    #print("parent 1 Section", parent_1_section)
                                    #print("parent 2 Section", parent_2_section)
                                    index_struct_json.add_record(section, {}, index_struct_json.dict_object[parent_2_section][sub_topics_kw][parent_1_section][sub_topics_kw])
                                    index_struct_json.add_record(title_kw, title, index_struct_json.dict_object[parent_2_section][sub_topics_kw][parent_1_section][sub_topics_kw][section])
                                    #index_struct_json.add_record(sub_topics_kw, {}, index_struct_json.dict_object[parent_section][sub_topics_kw][section])


                            else:
                                pass
                                #print("No match found.")
                                
                            
                        except Exception as e: # work on python 2.x
                            print('Failed to add index: '+ str(e)) 


                    #index_struct_json.print_dict()
                    index_struct_json.write_to_file(index_struct_json.dict_object, intro_json_filename)
                        






    def scrape_website (self, url):
        '''
        This function will establish connection with the website and read all the content of the pages.
        '''
        page_context_manager = urlopen(url)
        self.page_html = BeautifulSoup(page_context_manager, 'html.parser')
        print(self.page_html)



def main():

    #Initializing the class handle
    s_h = Scrapper()
    

    for index, books in enumerate(Machine_Learning["Books"]):
        books_folder = s_h.file_manager_h.get_books_dir()
        print("books Folder ", books_folder)
        if (Machine_Learning["Books"][str(index)]["Scrape"]):
            s_h.scrape_index( os.path.join(books_folder, Machine_Learning["Books"][str(index)]["Name"]))

    #print(Machine_Learning["web_resources"]["0"]["Link"])
    #s_h.scrape_website(Machine_Learning["web_resources"]["0"]["Link"])

    



if __name__ == "__main__":
    main()


