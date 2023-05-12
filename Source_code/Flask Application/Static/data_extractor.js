
var combo_tree_instance= ""

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

  //$('#MultiSelect_Header#1').empty()
  $('#justAnInputBox1').empty();

  // Initialize the comboTree with the provided data
 
  
  if (data.hasOwnProperty('0')) {
    console.log(data[0]['title'])
    $('#MultiSelect_Header_1').text(data[0]['title'])
  } else {
    $('#MultiSelect_Header_1').text("")
  }
  
  combo_tree_instance = $('#justAnInputBox1').comboTree({
    source: data,
    isMultiple: true,
		cascadeSelect: true,
		collapse: true
    // Other options and settings for the comboTree can be specified here
  });
}


$('#submit_response_1').click(function() {
  
  selected_element_names  = combo_tree_instance.getSelectedNames();
  selected_element_id     = combo_tree_instance.getSelectedIds();
  console.log(selected_element_names)
  console.log(selected_element_id)

  post_data( { "id":selected_element_id, "name":selected_element_names} )
});


function post_data (data){

  //console.log("Posting Data", data)

  $.ajax({
    type: "POST",
    url: "/post_data",
    data: data,
      success: function (data, status, xhr) {
      console.log(data);
    },
    error: function (jqXhr, textStatus, errorMessage) {
      console.log(errorMessage);
    }
  })

}