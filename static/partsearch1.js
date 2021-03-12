
var allrows = document.getElementsByClassName('row-parts');

function search(l,c){
  if(c.includes("restocklvl-parts")){
    console.log("restock");
  }
  var part = document.getElementsByName(c)[0].value;
  console.log(part);
  if(part==""){
    for(x of allrows){
      x.style.display = "block";
    }
  }else{
    for(x of allrows){
      x.style.display = "none";
    }
    for(x of allrows){
      if(!c.includes("restocklvl-parts")){
        if(x.id.split("%")[l].toLowerCase().startsWith(part.toLowerCase())){
          x.style.display = "block";
          console.log(x.id);
      }

      if(c.includes("restock")){
        console.log("restock");
        if(x.id.split("%")[l].toLowerCase() == part.toLowerCase()){
          x.style.display = "block";
        }
      }
    }
  }

}
}
