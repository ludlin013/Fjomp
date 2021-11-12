var sd = {
  0 : "red",
  1 : "yellow",
  2 : "green"
}

function updateusers(id){

  var xhttp = new XMLHttpRequest();


  xhttp.onload = function(){

    for(x in JSON.parse(xhttp.responseText)){
      document.getElementById(x).style.background = sd[JSON.parse(xhttp.responseText)[x]];
    }
  }

  xhttp.open("POST","/updateusers",true);
  xhttp.send();




}
updateusers()
setInterval(function(){updateusers()}, 5000);
