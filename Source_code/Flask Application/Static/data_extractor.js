
var cuisine_recipe_list = {}
var direction_index = 1
var recipe_data = {}

function init(){

  readTextFile("../data/recipe_links.json")
  
}

function readTextFile(file)
{
  $.getJSON('/data',function(data, status, xhr){
    populate_list(data)       
  })  
  
}


function populate_list(data_object){

  var treeJson = convertPythonJSONToTreeBasedJSON(data_object);
  console.log(treeJson);
  initializeComboTree(treeJson)
}


function convertPythonJSONToTreeBasedJSON(jsonObj) {
  let idCounter = 1;

  function processSubTopics(subTopics) {
    const nodes = [];

    for (const key in subTopics) {
      const subTopic = subTopics[key];
      const id = idCounter++;
      const node = { id, title: subTopic.Title };

      if (subTopic["Sub Topics"]) {
        node.subs = processSubTopics(subTopic["Sub Topics"]);
      }

      nodes.push(node);
    }

    return nodes;
  }

  const root = [{ id: idCounter++, title: jsonObj.Title, subs: processSubTopics(jsonObj["Sub Topics"]) }];
  return root;
}

function initializeComboTree(data) {
  // Clear existing data in the comboTree, if any
  console.log("Populating with Data", data)
  
  $('#justAnInputBox1').empty();

  // Initialize the comboTree with the provided data
  $('#justAnInputBox1').comboTree({
    source: data,
    isMultiple: true // Set to true if you want to allow multiple selections
    // Other options and settings for the comboTree can be specified here
  });
}
