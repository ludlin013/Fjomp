
var allrows = document.getElementsByClassName('row-parts');

function search(){
  var part = document.getElementsByName("part-parts")[0].value;
  var desc = document.getElementsByName("description-parts")[0].value;
  var lp = document.getElementsByName("LP-parts")[0].value;
  var rest = document.getElementsByName("restocklvl-parts")[0].value;

  console.log(part);

  for(x of allrows){
    if(part=="" && desc=="" && lp=="" && rest==""){
      x.style.display = "block";
    }else if(x.id.split("%")[0].toLowerCase().includes(part.toLowerCase()) && x.id.split("%")[1].toLowerCase().includes(desc.toLowerCase()) && x.id.split("%")[2].toLowerCase().includes(lp.toLowerCase())){
      x.style.display = "block";
  }else{
    x.style.display = "none";
  }
}
}
