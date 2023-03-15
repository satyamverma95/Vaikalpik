from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen
import re
import os
import PyPDF2
from file_path_manager import File_Path_Manager
from books_names import Machine_Learning
from json_manager import Json_Object

class Index_Scrapper:
    def __init__ (self):

        #Decalring the variables
        self.books_dict_h   =   Json_Object()
        self.table          =   pd.DataFrame()
        self.file_manager_h      =   File_Path_Manager()
         
        
    def read_book(self, filename):
        
        with open(filename, 'r') as f:
            self.book_content = f.read()

        print(self.book_content)


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
                self.books_dict_h.add_record(page_no, page_content, self.books_dict_h.dict_object['Pages'])
                #print(page.extract_text())
            
            #self.books_dict_h.print_dict(self.books_dict_h.dict_object)
            data_dict_dir = self.file_manager_h.get_book_json_dir()
            #print(os.path.join(data_dict_dir,book_name.split('.')[0]))
            self.books_dict_h.write_to_file(self.books_dict_h.dict_object, os.path.join(data_dict_dir,book_name.split(".")[0]))

def main():

    #Initializing the class handle
    is_h = Index_Scrapper()
    

    for books in Machine_Learning:
        books_folder = is_h.file_manager_h.get_books_dir()
        print("books Folder ", books_folder)
        is_h.pdf_reader( os.path.join(books_folder, books), books)


if __name__ == "__main__":
    main()


