
var allrows = document.getElementsByClassName('row-parts');

var inactive = document.getElementsByName("active-parts")[0].checked;

for(x of allrows){
    if(x.id.split("%")[2] != inactive && inactive == true){
      x.style.display = "block";
    }else if(inactive == false){
      x.style.display = "block";
    }
    else{
      x.style.display = "none";
    }
}


function search(){
  var part = document.getElementsByName("part-parts")[0].value;
  var desc = document.getElementsByName("description-parts")[0].value;
  var inactive = document.getElementsByName("active-parts")[0].checked;

  for(x of allrows){
    if(part=="" && desc==""){
      if(x.id.split("%")[2] != inactive && inactive == true){
        x.style.display = "block";
      }else if(inactive == false){
        x.style.display = "block";
      }
      else{
        x.style.display = "none";
      }
    }else if(x.id.split("%")[0].toLowerCase().includes(part.toLowerCase()) && x.id.split("%")[1].toLowerCase().includes(desc.toLowerCase())){
      if(x.id.split("%")[2] == inactive && inactive == true){
        x.style.display = "block";
      }else if(inactive == false){
        x.style.display = "block";
      }
      else{
        x.style.display = "none";
      }
  }else{
    x.style.display = "none";
  }
}




}
