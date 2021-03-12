
var allrows = document.getElementsByClassName('row-parts');

function search(){
  var part = document.getElementsByName("part-parts")[0].value;
  var desc = document.getElementsByName("description-parts")[0].value;
  var supp = document.getElementsByName("supplier-parts")[0].value;
  var lp = document.getElementsByName("LP-parts")[0].value;
  var rest = document.getElementsByName("restocklvl-parts")[0].value;

  for(x of allrows){
    if(part=="" && desc=="" && supp=="" && lp=="" && rest==""){
      x.style.display = "block";
      console.log(part.strip());
    }
  }
}
