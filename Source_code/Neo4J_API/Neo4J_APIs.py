from neo4j import GraphDatabase
import logging
import os
from dotenv import load_dotenv, dotenv_values, find_dotenv
from os.path import join, dirname


class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.credentials_file = "../Credentials"
        #self.password = self.getPassword(password)
        dotenv_path = join(dirname(__file__), '.env')
        dotenv_path = find_dotenv(usecwd=True)
        config = dotenv_values(dotenv_path)
        self.password = ['NEO4J_PASSWORD']
        print(config.items())


    def getPassword ( self, password ):
    
        if not password:
            with open(self.credentials_file, "r+") as file_h:
                # Reading from a file
                print(file_h.read())
        
        return (password)        



if __name__ == "__main__":
    # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
    uri = "neo4j+s://0dcd9665.databases.neo4j.io"
    user = "neo4j"
    password = ""
    app = App(uri, user, password)
    app.create_friendship("Alice", "David")
    app.find_person("Alice")
    app.close()