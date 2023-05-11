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
        self.sub_topics_kw  =   "Sub Topics"    
        self.title_kw       =   "Title"
        self.link           =   "Link"
        self.see_also       =   "See also"


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


    def is_next_tag(tag):
        return tag.name in ['h3', 'ul', 'p']

    def scrape_page(self):

        self.page_body = self.page_html.find_all("div", {"class":"mw-parser-output"})
        div_element = self.page_body[-1] #Since we have only one div element with that id, its better to index it separately.
        heading_list = div_element.find_all("h2")
        sub_heading_list = div_element.find_all("h3")
        #topics_list = div_element.find_all("ul")
        self.lr_topic_dict = Json_Object()
                
        #print("H2 heading List", heading_list)
        #print("Number of H2 Element", len(heading_list))

        for heading_iter, head_elem in enumerate(heading_list):

            #print("Heading List", head_elem)
            span_elem =  head_elem.find("span")
            #print("span_elem ", span_elem)
            heading_title = span_elem.text
            heading_index = heading_iter + 1 

            #print("heading title ", heading_title.text)

            self.lr_topic_dict.add_record( heading_index, {}, self.lr_topic_dict.dict_object )
            self.lr_topic_dict.add_record( self.title_kw, heading_title, self.lr_topic_dict.dict_object[heading_index] )
            self.lr_topic_dict.add_record( self.link, "", self.lr_topic_dict.dict_object[heading_index] )
            self.lr_topic_dict.add_record(self.sub_topics_kw, {}, self.lr_topic_dict.dict_object[heading_index])
            
            current_tag = heading_list[heading_iter]
            print("\nCurrent h2 ", heading_list[heading_iter].text)
            intial_loop = True 
            topic_index = 1

            while current_tag and (current_tag.name != "h2" or intial_loop):
                
                if current_tag.name =="h3":

                    title = current_tag.find("span").text
                    #print("Cuurent Tag", title)

                    self.lr_topic_dict.add_record( topic_index, {}, self.lr_topic_dict.dict_object[heading_index][self.sub_topics_kw] )
                    self.lr_topic_dict.add_record( self.title_kw, title, self.lr_topic_dict.dict_object[heading_index][self.sub_topics_kw][topic_index] )
                    self.lr_topic_dict.add_record( self.link, "", self.lr_topic_dict.dict_object[heading_index][self.sub_topics_kw][topic_index] )
                    self.lr_topic_dict.add_record(self.sub_topics_kw, {}, self.lr_topic_dict.dict_object[heading_index][self.sub_topics_kw][topic_index])
                    

                    uls = current_tag.find_next('ul', until=current_tag)
                    list_elem = uls.find_all("li")
                    subtopic_indexer = 1
                 
                    for li in list_elem:
                        anchor_tags = li.find_all("a")
                        
                        for index_subtopic, anchor in enumerate(anchor_tags): 
                            
                            link = anchor.get("href")
                            title = anchor.get("title")
                            sub_topic_index = ".".join([str(topic_index), str(subtopic_indexer)])
                            print(" Adding Data title:{}, Link :{}, index:{}".format(title, link, sub_topic_index))
                            
                            self.lr_topic_dict.add_record( sub_topic_index, {}, self.lr_topic_dict.dict_object[heading_index][self.sub_topics_kw][topic_index][self.sub_topics_kw] )
                            self.lr_topic_dict.add_record( self.title_kw, title, self.lr_topic_dict.dict_object[heading_index][self.sub_topics_kw][topic_index][self.sub_topics_kw][sub_topic_index] )
                            self.lr_topic_dict.add_record( self.link, link, self.lr_topic_dict.dict_object[heading_index][self.sub_topics_kw][topic_index][self.sub_topics_kw][sub_topic_index] )
                            self.lr_topic_dict.add_record(self.sub_topics_kw, {}, self.lr_topic_dict.dict_object[heading_index][self.sub_topics_kw][topic_index][self.sub_topics_kw][sub_topic_index])


                            subtopic_indexer += 1
                   
                    topic_index += 1
                current_tag = current_tag.find_next()
                #print("Current tag Name", current_tag.name)
                #print(current_tag.name != "h2" )
                intial_loop = False

            '''
            # iterate through each h3 element
            for iter in range(len(next_h3_list)):
            
                #print("\n\nHeading : ", type(next_h3_list))
                title = next_h3_list[iter].find("span").text

                # find the next h3 element, if it exists
                next_h3 = next_h3_list[iter + 1] if iter + 1 < len(next_h3_list) else None
                topic_index = iter + 1

                self.lr_topic_dict.add_record( topic_index, {}, self.lr_topic_dict.dict_object[heading_index][self.sub_topics_kw] )
                self.lr_topic_dict.add_record( self.title_kw, title, self.lr_topic_dict.dict_object[heading_index][self.sub_topics_kw][topic_index] )
                self.lr_topic_dict.add_record( self.link, "", self.lr_topic_dict.dict_object[heading_index][self.sub_topics_kw][topic_index] )
                self.lr_topic_dict.add_record(self.sub_topics_kw, {}, self.lr_topic_dict.dict_object[heading_index][self.sub_topics_kw][topic_index])
                
                # find all ul elements between this h3 and the next one
                uls = next_h3_list[iter].find_next('ul', until=next_h3)
                list_elem = uls.find_all("li")
                topic_indexer = 1 
                
                # process each ul element
                for li in list_elem:
                    anchor_tags = li.find_all("a")
                    
                    for index_subtopic, anchor in enumerate(anchor_tags): 
                        
                        link = anchor.get("href")
                        title = anchor.get("title")
                        #print(" Adding Data title:{}, Link :{}, index:{}".format(title, link, topic_indexer))
                        sub_topic_index = ".".join([str(topic_index), str(topic_indexer)])

                        self.lr_topic_dict.add_record( sub_topic_index, {}, self.lr_topic_dict.dict_object[heading_index][self.sub_topics_kw][topic_index][self.sub_topics_kw] )
                        self.lr_topic_dict.add_record( self.title_kw, title, self.lr_topic_dict.dict_object[heading_index][self.sub_topics_kw][topic_index][self.sub_topics_kw][sub_topic_index] )
                        self.lr_topic_dict.add_record( self.link, link, self.lr_topic_dict.dict_object[heading_index][self.sub_topics_kw][topic_index][self.sub_topics_kw][sub_topic_index] )
                        self.lr_topic_dict.add_record(self.sub_topics_kw, {}, self.lr_topic_dict.dict_object[heading_index][self.sub_topics_kw][topic_index][self.sub_topics_kw][sub_topic_index])
                        
                        topic_indexer += 1
            '''
        self.write_to_file( json.dumps(self.lr_topic_dict.dict_object), os.path.join(self.path_manager_h.get_course_outline_dir(), self.base_filename))

    
    def scrape_page_ver_2(self):

        self.page_body = self.page_html.find_all("div", {"class":"mw-parser-output"})
        div_element = self.page_body[-1] #Since we have only one div element with that id, its better to index it separately.
        heading_list = div_element.find_all("h2")
        self.lr_topic_dict = Json_Object()
                
        #print("H2 heading List", heading_list)
        #print("Number of H2 Element", len(heading_list))

        for heading_iter, head_elem in enumerate(heading_list):

            #print("Heading List", head_elem)
            span_elem =  head_elem.find("span")
            #print("span_elem ", span_elem)
            heading_title = span_elem.text
            heading_index = heading_iter + 1 

            #print("heading title ", heading_title.text)

            self.lr_topic_dict.add_record( heading_index, {}, self.lr_topic_dict.dict_object )
            self.lr_topic_dict.add_record( self.title_kw, heading_title, self.lr_topic_dict.dict_object[heading_index] )
            self.lr_topic_dict.add_record( self.link, "", self.lr_topic_dict.dict_object[heading_index] )
            self.lr_topic_dict.add_record(self.sub_topics_kw, {}, self.lr_topic_dict.dict_object[heading_index])
            
            current_tag = heading_list[heading_iter]
            intial_loop = True
            sub_topic_index  = 1
            
            print("\nCurrent h2 ", heading_list[heading_iter].find("span").text)
            
            if (self.see_also.lower() in heading_list[heading_iter].find("span").text.lower()):
                break
             
            while current_tag and (current_tag.name != "h2" or intial_loop):
                
                if current_tag.name =="ul":
                
                    #print("Current Tag ", current_tag.text )
                    list_elem = current_tag.find_all("li")
                    
                    
                    # process each ul element
                    for li in list_elem:
                        anchor_tags = li.find_all("a")

                        if (anchor_tags):
                            #print("anchor tags ", anchor_tags)
                            sub_topic_link = anchor_tags[-1].get("href")
                            sub_topic_title = anchor_tags[-1].get("title")
                            print(" Adding Data title:{}, Link :{}, index:{}".format(sub_topic_link, sub_topic_link, sub_topic_index))

                            self.lr_topic_dict.add_record( sub_topic_index, {}, self.lr_topic_dict.dict_object[heading_index][self.sub_topics_kw] )
                            self.lr_topic_dict.add_record( self.title_kw, sub_topic_title, self.lr_topic_dict.dict_object[heading_index][self.sub_topics_kw][sub_topic_index] )
                            self.lr_topic_dict.add_record( self.link, sub_topic_link, self.lr_topic_dict.dict_object[heading_index][self.sub_topics_kw][sub_topic_index] )
                            self.lr_topic_dict.add_record(self.sub_topics_kw, {}, self.lr_topic_dict.dict_object[heading_index][self.sub_topics_kw][sub_topic_index])
                
                            sub_topic_index += 1

                current_tag = current_tag.find_next()
                #print("Current tag Name", current_tag.name)
                #print(current_tag.name != "h2" )
                intial_loop = False

          
        self.write_to_file( json.dumps(self.lr_topic_dict.dict_object), os.path.join(self.path_manager_h.get_course_outline_dir(), self.base_filename))




    def scrape_page_old(self):    
        
        self.page_body = self.page_html.find_all("div", {"class":"mw-parser-output"})
        div_element = self.page_body[-1] #Since we have only one div element with that id, its better to index it separately.
        heading_list = div_element.find_all("h2")
        sub_heading_list = div_element.find_all("h3")
        topics_list = div_element.find_all("ul")
        self.lr_topic_dict = Json_Object()
        
        if ( len( sub_heading_list ) > 0 ):

            for index, sub_heading in enumerate(sub_heading_list):
                try:
                    link = a_tag.get("href")
                    title = a_tag.get("title")

                    if (link is not None) and (title is not None):
                            self.lr_topic_dict.add_record( index, {}, self.lr_topic_dict.dict_object )
                            self.lr_topic_dict.add_record( self.title_kw, title, self.lr_topic_dict.dict_object[index] )
                            self.lr_topic_dict.add_record( self.link, link, self.lr_topic_dict.dict_object[index] )
                            self.lr_topic_dict.add_record(self.sub_topics_kw, {}, self.lr_topic_dict.dict_object[index])
                except:
                    print("Not able to extract sub-Heading.")
                
                for topics in topics_list:
                    try:
                        a_tags = topics.find_all("a")
                        for a_tag in a_tags:
                            link = a_tag.get("href")
                            title = a_tag.get("title")

                            #print("title:{}, Link :{}".format(link, title))
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


    def scrape_topic_outline(self, web_url, function_ver):

        self.web_url = web_url
        
        self.get_base_filename()
        self.scrape_website ()
        
        if ("ver_2" in function_ver):
            self.scrape_page_ver_2()
        else:
            self.scrape_page()
        
       

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


def main ( outline_scraping=True, hyperlink_scraping=False ):

    ws_h = Wikipedia_Scrapper()

    if (outline_scraping):
        for index, books in enumerate(Machine_Learning["Wikipedia_Outline"]):
            if (Machine_Learning["Wikipedia_Outline"][str(index)]["Scrape"]):
                print(Machine_Learning["Wikipedia_Outline"][str(index)]["Link"])
                ws_h.scrape_topic_outline( Machine_Learning["Wikipedia_Outline"][str(index)]["Link"],\
                                           Machine_Learning["Wikipedia_Outline"][str(index)]["function"] )
    
    elif (hyperlink_scraping):
        
        ###Now after Scraping the Outline of the course we move ahead and scrape the hyperlinks of the pages.
        
        ws_h.scrape_hyperlinks_wikipedia()


if __name__ == "__main__":
    main(outline_scraping=True, hyperlink_scraping=False)