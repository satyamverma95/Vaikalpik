from dotenv import load_dotenv
import os

class File_Path_Manager:
    def __init__ (self):
        #Loading env variables
        load_dotenv()
        self.root_dir       =   os.getenv('ROOT_DIR')
        self.project_dir    =   os.getenv("PROJECT_DIR")
        self.users          =   os.getenv("USERS")
        self.users_name     =   os.getenv("USERS_NAME")
        self.cloud          =   os.getenv("CLOUD")
        self.category_folder=   os.getenv("CATEGORY_FOLDER")
        self.git_folder     =   os.getenv("GIT_FOLDER")
        self.source_dir     =   os.getenv("SOURCE_DIR")
        self.data_dir       =   os.getenv("DATA_PATH")
        self.books_dir      =   os.getenv("BOOKS_PATH")
        self.book_Json      =   os.getenv("BOOK_JSON")
        self.web_dir        =   os.getenv("WEB_PATH")
        self.web_json_dir   =   os.getenv("WEB_JSON_PATH")


    def get_root_dir(self):
    
        return (self.root_dir)

    def get_project_dir(self):
        
        return (os.path.join(self.root_dir, self.users, self.users_name, self.cloud, self.category_folder, self.git_folder))
    

    def get_source_dir(self):    

        return (os.path.join(self.root_dir, self.users, self.users_name, self.cloud, self.category_folder, self.git_folder,\
                             self.source_dir))


    def get_books_dir(self):      
        
        return (os.path.join(self.root_dir, self.users, self.users_name, self.cloud, self.category_folder, self.git_folder,\
                             self.project_dir, self.data_dir, self.books_dir))

    def get_data_dir(self):      
        
        return (os.path.join(self.root_dir, self.users, self.users_name, self.cloud, self.category_folder, self.git_folder,\
                             self.project_dir, self.data_dir ))

    def get_book_json_dir(self):      
        
        return (os.path.join(self.root_dir, self.users, self.users_name, self.cloud, self.category_folder, self.git_folder,\
                             self.project_dir, self.data_dir, self.book_Json))

    def get_web_res_dir(self):      
        
        return (os.path.join(self.root_dir, self.users, self.users_name, self.cloud, self.category_folder, self.git_folder,\
                             self.project_dir, self.data_dir, self.web_dir ))


    def get_web_josn_res_dir(self):      
        
        return (os.path.join(self.root_dir, self.users, self.users_name, self.cloud, self.category_folder, self.git_folder,\
                             self.project_dir, self.data_dir, self.web_json_dir ))


def main():
    #Checking the functions results

    fpm_h = File_Path_Manager()
    
    #root_dir = fpm_h.get_root_dir()
    #print("Root_dir", root_dir)

    #project_dir = fpm_h.get_project_dir()
    #print("Root_dir", project_dir)

    #source_dir = fpm_h.get_source_dir()
    #print("Source_dir", source_dir)

    books_dir = fpm_h.get_books_dir()
    print("Books_dir", books_dir)

if __name__ == "__main__":
    main()


