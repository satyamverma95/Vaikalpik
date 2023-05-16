
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


function convertPythonJSONToTreeBasedJSON__(jsonObj) {
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

function convertPythonJSONToTreeBasedJSON(jsonData) {

  function processSubTopics(subTopics, idCounter) {
    const nodes = [];
  
    for (const key in subTopics) {
      const subTopic = subTopics[key];
      const node = { id: idCounter++, title: subTopic.Title };
  
      if (subTopic["Sub Topics"]) {
        const result = processSubTopics(subTopic["Sub Topics"], idCounter);
        nodes.push(...result);
        idCounter = result.length > 0 ? result[result.length - 1].id + 1 : idCounter;
      }
  
      nodes.push(node);
    }
  
    return nodes;
  }

let idCounter = 0;
const nodes = processSubTopics(jsonData["Sub Topics"], idCounter);
const result = [{ id: idCounter++, title: jsonData.Title, subs: nodes, isSelectable: false }];

return result

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


function createTableFromJSON(data) {
  const table = document.createElement('table');

  const thead = document.createElement('thead');
  const tr = document.createElement('tr');

  const thSequence = document.createElement('th');
  thSequence.textContent = 'Sequence';
  tr.appendChild(thSequence);

  const thTopic = document.createElement('th');
  thTopic.textContent = 'Topic';
  tr.appendChild(thTopic);

  const thTopicsRecommended = document.createElement('th');
  thTopicsRecommended.textContent = 'Topics Recommended';
  tr.appendChild(thTopicsRecommended);

  const thAlreadyRead = document.createElement('th');
  thAlreadyRead.textContent = 'Already Read';
  tr.appendChild(thAlreadyRead);

  thead.appendChild(tr);
  table.appendChild(thead);

  const tbody = document.createElement('tbody');

  let sequence = 1; // Initialize sequence number

  for (const topic in data) {
    const subtopics = data[topic];

    const tr = document.createElement('tr');

    const tdSequence = document.createElement('td');
    tdSequence.textContent = sequence;
    tr.appendChild(tdSequence);

    const tdTopic = document.createElement('td');
    tdTopic.textContent = topic;
    tr.appendChild(tdTopic);

    const tdTopicsRecommended = document.createElement('td');
    tdTopicsRecommended.classList.add('topics-recommended');

    const tdAlreadyRead = document.createElement('td');
    tdAlreadyRead.classList.add('already-read');

    let topicsRecommendedCount = 0; // Initialize topics recommended count
    let alreadyReadCount = 0; // Initialize already read count

    for (const subtopic in subtopics) {
      const div = document.createElement('div');
      div.textContent = subtopic;

      if (subtopics[subtopic] === '0') {
        tdTopicsRecommended.appendChild(div);
        topicsRecommendedCount++;
      } else if (subtopics[subtopic] === '1') {
        tdAlreadyRead.appendChild(div);
        alreadyReadCount++;
      }
    }

    if (topicsRecommendedCount === 0) {
      tdTopicsRecommended.textContent = '-';
    } else {
      tdTopicsRecommended.setAttribute('data-count', topicsRecommendedCount);
    }

    if (alreadyReadCount === 0) {
      tdAlreadyRead.textContent = '-';
    } else {
      tdAlreadyRead.setAttribute('data-count', alreadyReadCount);
    }

    tr.appendChild(tdSequence);
    tr.appendChild(tdTopic);
    tr.appendChild(tdTopicsRecommended);
    tr.appendChild(tdAlreadyRead);

    tbody.appendChild(tr);

    sequence++; // Increment sequence number
  }

  table.appendChild(tbody);

  return table;
}




function publish_data_to_user(jsonData){

  // Get the container element
 
  var container = document.getElementById('table-container');
  container.innerHTML = ""

  // Create the table
  var table = createTableFromJSON(jsonData);

  // Append the table to the container
  container.appendChild(table);
  $("#table_header_ele").show()
}


$('#submit_response_1').click(function() {
  
  selected_element_names  = combo_tree_instance.getSelectedNames();
  selected_element_id     = combo_tree_instance.getSelectedIds();
  console.log(selected_element_names)
  console.log(selected_element_id)

  post_data( { "id":selected_element_id, "name":selected_element_names} )
});


function post_data (data_post){

  // Show the loading gif
  $("#loading_gif_container").css("display", "flex");
  $("#table_header_ele").css("display", "none");
  $("#table-container").empty()
  //$("#loading_gif_container").show();

  $.ajax({
    type: "POST",
    url: "/post_data",
    data: JSON.stringify(data_post),
      success: function (data, status, xhr) {
      //console.log(data);
      $("#loading_gif_container").hide();
      console.log("Data Received", data)
      publish_data_to_user(data)
    },
    error: function (jqXhr, textStatus, errorMessage) {
      console.log(errorMessage);
    }
  })

}