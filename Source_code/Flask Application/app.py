from flask import Flask, render_template, request
import json
import os
import sys
from dotenv import load_dotenv

load_dotenv(os.sep.join([os.path.dirname(os.getcwd()), "Scraping", ".env"])) 

sys.path.insert(0, os.sep.join([os.path.dirname(os.getcwd()), os.getenv("SCRAPING_SCRIPT")]))
from file_path_manager import File_Path_Manager

sys.path.insert(0, os.sep.join([os.path.dirname(os.getcwd()), os.getenv("QUERY_SCRIPTS_FOLDER")]))
from Prerequisites_finder import Prerequisites 

app = Flask(__name__)
fpm_h = File_Path_Manager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post_data', methods=['POST'])
def post_data():
    if request.method == 'POST':
       
        data                =   list(request.form.items())[0]
        json_string         =   data[0]
        parsed_data         =   json.loads(json_string)
        selected_item_id    =   parsed_data.get("id")
        selected_item_name  =   parsed_data.get("name") 

    print("Selected item id", selected_item_id)
    print("Selected item name", selected_item_name)
   
    p_h = Prerequisites()
    p_h.grab_data({ "id":selected_item_id, "name":selected_item_name})

    return("Data Posted Sucessfully")


@app.route('/Query', methods=['POST'])
def Query():
    if request.method == 'POST':
        
        question = request.form.get('question')
        step_no = int(request.form.get('direction_index') )
        cuisine = request.form.get('cuisine')
        recipe = request.form.get('recipe')
        servings = request.form.get('servings')
        print("Question asked :{} for step No {}".format(question, step_no))


@app.route('/data')
def get_data():  

    json_path = os.sep.join([fpm_h.get_book_json_dir(), "Machine_Learning_A_Probabilistic_Perspective_Index.json"])
    data = json.load(open(json_path)) 
    ##print(data)
    return json.dumps(data)

if __name__ == '__main__':
    app.run(debug=True)
