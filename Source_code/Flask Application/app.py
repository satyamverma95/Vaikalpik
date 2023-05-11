from flask import Flask, render_template, request
import json
#from Web_Scraping import Web_Scrapper
#from recipes_mapping import Recipe_Mapping
#from Qurey_Resolver import Query_Resolver

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_file', methods=['POST'])
def create_file():
    if request.method == 'POST':
        '''
        rm_h = Recipe_Mapping()
        ws_h = Web_Scrapper()

        cuisine = request.form.get('cuisine')
        recipe = request.form.get('recipe')

        recipe_link_file = "data/recipe_links.json"
        recipe_link_data = json.load(open(recipe_link_file))

        ws_h.recipe_handle.cuisine_names  = {cuisine : ""}
        ws_h.recipe_handle.recipe_dict = {cuisine : { recipe : recipe_link_data[cuisine][recipe]} }
        
        print("calling the script", ws_h.recipe_handle.recipe_dict )

        ws_h.scrape_recipes()
        print("calling the script")

        recipe_json = "data/recipe_details_1.json"
        recipe_data = json.load(open(recipe_json))

        print("Cuisine :{}, recipe {}".format(cuisine, recipe))

        return (recipe_data[cuisine][recipe])
        '''

@app.route('/Query', methods=['POST'])
def Query():
    if request.method == 'POST':
        
        question = request.form.get('question')
        step_no = int(request.form.get('direction_index') )
        cuisine = request.form.get('cuisine')
        recipe = request.form.get('recipe')
        servings = request.form.get('servings')
        print("Question asked :{} for step No {}".format(question, step_no))

        '''
        qr_h = Query_Resolver()
        qr_h.read_json()
        qr_h.set_cuisine_and_recipe(cuisine, recipe, servings)
        parsed_query = qr_h.parse_question(question)
        answer = qr_h.question_interpreter(parsed_query, step_no)

        return (answer)
        '''

@app.route('/data')
def get_data():  
    json_path = "data/recipe_links.json"
    data = json.load(open(json_path)) 
    ##print(data)
    return json.dumps(data)

if __name__ == '__main__':
    app.run(debug=True)



'''
a. User can read the comments (or listen)
b. Navigate between steps - Done in Front end.
b.1 Go forward - Done with Next Direction.
b.2 Go backward - Done with Prev Direction. 
c. ask questions about 
  c.1. cooking action specified in the step - 
c.2. the ingredients used - 
c.3 the utensil or tool used
c.4 time and temp
'''