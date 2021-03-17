
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
  var inactive = document.getElementsByName("active-parts")[0].checked;
  for(x of allrows){
    if(x.id.split("%")[2] != inactive && inactive == true) {
      x.style.display = "block";
    }else if(inactive == false) {
      x.style.display = "block";
    }
    else{
      x.style.display = "none";
    }
  }
}
