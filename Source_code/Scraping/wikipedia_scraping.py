from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen
from resources import Machine_Learning
from json_manager import Json_Object
from file_path_manager import File_Path_Manager
import os
from urllib.parse import urlsplit
import re
import json

class Wikipedia_Scrapper:
    def __init__ (self):
        self.url_cuisines   =   ""
        self.table          =   pd.DataFrame()
        self.page_html      =   ""
        self.path_manager_h =   File_Path_Manager()
        self.web_url        =   ""
        self.base_filename  =   ""
        self.outline_dict   =   ""
        self.wikipedia_url  =   "https://en.wikipedia.org/"

    def scrape_website (self):
        '''
        This function will establish connection with the website and read all the content of the pages.
        '''
        try:
            page_context_manager = urlopen(self.web_url)
            self.page_html = BeautifulSoup(page_context_manager, 'html.parser')
            #print(self.page_html)
        except:
            print("Error scraping the website.")

    def read_json(self, filename):
        self.outline_dict = json.load(open(filename))

    def make_valid_filename(self, filename):
        # Replace illegal characters with underscores
        valid_chars = '-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        clean_filename = re.sub('[^{}]+'.format(valid_chars), '_', filename)
        return (clean_filename)

    def get_base_filename(self, optional_str=""):

        parsed_url = urlsplit(self.web_url)

        self.base_filename = ".".join([self.make_valid_filename(parsed_url.path.split("/")[-1]) + optional_str, "json"])

        print(self.base_filename)



    def scrape_page(self):

        self.page_body = self.page_html.find_all("div", {"class":"mw-parser-output"})
        div_element = self.page_body[-1] #Since we have only one div element with that id, its better to index it separately.
        topics_list = div_element.find_all("ul")
        self.lr_topic_dict = Json_Object()

        for topics in topics_list:
            try:
                a_tags = topics.find_all("a")
                for a_tag in a_tags:
                    link = a_tag.get("href")
                    title = a_tag.get("title")

                    print("title:{}, Link :{}".format(link, title))
                    if (link is not None) and (title is not None):
                        self.lr_topic_dict.add_record( title, link, self.lr_topic_dict.dict_object )
            except:
                print("Error retrieving link")            

        self.write_to_file( json.dumps(self.lr_topic_dict.dict_object), os.path.join(self.path_manager_h.get_course_outline_dir(), self.base_filename))
        

    def scrape_hyperlinks(self):

        self.hyperlinks_dict = Json_Object()
       
        self.page_body = self.page_html.find_all("div", {"class":"mw-parser-output"})
        
        if (len(self.page_body)>=1 ):
            div_element = self.page_body[-1] #Since we have only one div element with that id, its better to index it separately.
       
            for hyperlink in div_element.find_all("a"):
                try:
                    link = hyperlink.get("href")
                    title = hyperlink.get("title")

                    print("title:{}, Link :{}".format(link, title))
                    if (link is not None) and (title is not None):
                        self.hyperlinks_dict.add_record( title, link, self.hyperlinks_dict.dict_object )
                except:
                    print("Error retrieving link")            

            self.write_to_file( json.dumps(self.hyperlinks_dict.dict_object), os.path.join(self.path_manager_h.get_hyperlink_data_dir(), self.base_filename))
            


    def write_to_file(self, data, filename):

        with open(filename, "w+", encoding='utf-8') as f:
            f.write(str(data))


    def list_folder_files(self, folder):

        files_list = os.listdir(folder)

        return (files_list)


    def scrape_topic_outline(self, web_url):

        self.web_url = web_url
        
        self.get_base_filename()
        self.scrape_website ()
        self.scrape_page()
        #path = self.path_manager_h.get_web_scraped_dir()
        #print(path)
        #self.write_to_file(self.page_html, os.path.join(self.path_manager_h.get_course_outline_dir(), "scrape.txt"))

    def scrape_hyperlinks_wikipedia(self):
        
        print("Course Outline Dir", self.path_manager_h.get_course_outline_dir())
        files_list = self.list_folder_files(self.path_manager_h.get_course_outline_dir())
        
        for file in files_list:
            print(os.path.join(self.path_manager_h.get_course_outline_dir(), file))
            self.read_json(os.path.join(self.path_manager_h.get_course_outline_dir(), file))
            
            for topics in self.outline_dict.keys():
                self.web_url = self.wikipedia_url + self.outline_dict[topics]
                #self.web_url = "https://en.wikipedia.org/wiki/Conditional_probability"
                self.get_base_filename(optional_str="_hpyerlinks")
                self.scrape_website()
                self.scrape_hyperlinks()


def main ( outline_scraping=False, hyperlink_scraping=False ):

    ws_h = Wikipedia_Scrapper()

    if (outline_scraping):
        for index, books in enumerate(Machine_Learning["Wikipedia_Outline"]):
            if (Machine_Learning["Wikipedia_Outline"][str(index)]["Scrape"]):
                print(Machine_Learning["Wikipedia_Outline"][str(index)]["Link"])
                ws_h.scrape_topic_outline(Machine_Learning["Wikipedia_Outline"][str(index)]["Link"])
    
    elif (hyperlink_scraping):
        
        ###Now after Scraping the Outline of the course we move ahead and scrape the hyperlinks of the pages.
        
        ws_h.scrape_hyperlinks_wikipedia()


if __name__ == "__main__":
    main(outline_scraping=True, hyperlink_scraping=False)