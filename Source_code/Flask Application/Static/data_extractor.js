
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

  //console.log("Data Received", cuisine_recipe_list)
  cuisine_recipe_list = data_object //Stroing varibale in global varibale for access across all function.

  var select = document.getElementById("cuisine_id");
  var options = Object.keys(data_object)

  el = document.createElement("option");
  el.textContent = "None";
  el.value = opt;
  select.appendChild(el)

  for(var i = 0; i < options.length; i++) {
      var opt = options[i];
      var el = document.createElement("option");
      el.textContent = opt;
      el.value = opt;
      select.appendChild(el);
  }

}

function populate_recipe(){

  cuisine_selected = document.getElementById("cuisine_id").value
  document.getElementById('recipe_id').innerHTML = ""

  var select = document.getElementById("recipe_id");
  var options = Object.keys(cuisine_recipe_list[cuisine_selected])


  for(var i = 0; i < options.length; i++) {
      var opt = options[i];
      var el = document.createElement("option");
      el.textContent = opt;
      el.value = opt;
      select.appendChild(el);
  }


}


function fetch_recipe_details (){

  cuisine_selected = document.getElementById("cuisine_id").value
  recipe_selected = document.getElementById("recipe_id").value

  document.getElementById('recipe_directions').innerHTML = "";
  document.getElementById('Question_input_id').value = "";
  document.getElementById('Answer_div').innerHTML = "";
  direction_index = 1;

  console.log(cuisine_selected, recipe_selected )

  $.ajax({
    type: "POST",
    url: "/create_file",
    data: {
      "cuisine" : cuisine_selected, 
      "recipe"  : recipe_selected
    },success: function (data, status, xhr) {
      //console.log(data);
      recipe_data = data
      process_recipes_data('')
    },
    error: function (jqXhr, textStatus, errorMessage) {
      console.log(errorMessage);
    }
  })

}

function process_recipes_data(call){

  console.log(recipe_data)

  document.getElementById('recipe_directions').innerHTML = ""
  document.getElementById('Servings_id').value = ""


  if (call.match("Next")){
    direction_index += 1
  }
  else if (call.match("Prev")){
    direction_index -= 1
  }

  if (direction_index > 1){
    document.getElementById("Prev").disabled = false;
  }
  else{
    document.getElementById("Prev").disabled = true;
  }


  if ( direction_index <= Object.keys(recipe_data.Directions).length){
  
      var para = document.createElement("p");
      var node_1 = document.createTextNode("Step " + direction_index + ":");
      para.appendChild(node_1);
      var node_2 = document.createTextNode(recipe_data["Directions"][direction_index]);
      para.appendChild(node_2);
      var element = document.getElementById("recipe_directions");
      element.appendChild(para);
      document.getElementById("Next").disabled = false;

      if (direction_index == Object.keys(recipe_data.Directions).length){
        document.getElementById("Next").disabled = true;
      }
    
    }

    document.getElementById('Servings_id').value = recipe_data["Meta_Info"]["Servings:"]

}

function ask_question(speechToText){

  
  question_asked = document.getElementById("Question_input_id").value
  cuisine_selected = document.getElementById("cuisine_id").value
  recipe_selected = document.getElementById("recipe_id").value
  servings = document.getElementById("Servings_id").value

  if (speechToText){
    question_asked = speechToText
  }

  $.ajax({
    type: "POST",
    url: "/Query",
    data: {
      "question" : question_asked,
      "direction_index" : direction_index,
      "cuisine" : cuisine_selected, 
      "recipe"  : recipe_selected, 
      "servings": servings
    },success: function (data, status, xhr) {
      post_answer(data)
    },
    error: function (jqXhr, textStatus, errorMessage) {
      console.log(errorMessage);
    }
  })

}

function post_answer(answer){

  document.getElementById('Answer_div').innerHTML = ""

    var para = document.createElement("p");
    var node_1 = document.createTextNode(answer);
    para.appendChild(node_1);
    var element = document.getElementById("Answer_div");
    element.appendChild(para);

  speakTheAnswer(answer)
}

function speakTheAnswer(answer){

  var msg = new SpeechSynthesisUtterance(answer);
  window.speechSynthesis.speak(msg);

}

function runSpeechRecognition() {
  // get output div reference
  var output = document.getElementById("output");
  // get action element reference
  var action = document.getElementById("action");
      // new speech recognition object
      var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition;
      var recognition = new SpeechRecognition();
  
      // This runs when the speech recognition service starts
      recognition.onstart = function() {
          action.innerHTML = "<small>listening, please speak...</small>";
      };
      
      recognition.onspeechend = function() {
          action.innerHTML = "<small>stopped listening, hope you are done...</small>";
          recognition.stop();
      }
    
      // This runs when the speech recognition service returns result
      recognition.onresult = function(event) {
          var transcript = event.results[0][0].transcript;
          var confidence = event.results[0][0].confidence;
          //output.innerHTML = "<b>Text:</b> " + transcript + "<br/> <b>Confidence:</b> " + confidence*100+"%";
          output.innerHTML = "<b>You Said:</b> " + transcript + "<br/> <b>";
          output.classList.remove("hide");
          console.log("confidence", confidence)
          ask_question(transcript)
      };
    
       // start recognition
       recognition.start();

}

