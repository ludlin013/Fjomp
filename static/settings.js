function submitTechs(){
  for (x of document.getElementsByName('tech')){
    if (x.checked == false){
      x.value = 0
      x.checked = true
    }
  }

  for (x of document.getElementsByName('office')){
    if (x.checked == false){
      x.value = 0
      x.checked = true
    }
  }

  var xhttp = new XMLHttpRequest();
  xhttp.open("POST","/savetechs",true);
  const fd = new FormData(document.getElementById('techuserform'));
  xhttp.send(fd);
}


function savevarform(){
  var xhttp = new XMLHttpRequest();
  xhttp.open("POST","/savevariable",true);
  const fd = new FormData(document.getElementById('variableform'));
  xhttp.send(fd);
}

function savemodelform(){
  var xhttp = new XMLHttpRequest();
  xhttp.open("POST","/savemodels",true);
  const fd = new FormData(document.getElementById('modelform'));
  xhttp.send(fd);
}

function newmodel(){

  var xhttp = new XMLHttpRequest();
  xhttp.open("POST","/newmodel",true);
  xhttp.send();

}

function savepg(){
  var xhttp = new XMLHttpRequest();
  const fd = new FormData(document.getElementById('pgform'));

  xhttp.onload = function(){
    document.getElementById('pgsave').textContent = "Saved!"
  }

  xhttp.open("POST","/savepg",true);
  xhttp.send(fd);

}

function newpg(){
  var no = document.getElementById("pgform").children[document.getElementById("pgform").children.length - 1].children[0].name.substring(0,1);
  no = parseInt(no)+1

  var parent = document.getElementById('pgform');
  var row = document.createElement("a");
  row.classList.add("settingadmintech");

  var id = document.createElement("input");
  id.name = no + "id";
  id.type = "hidden";
  var number = document.createElement("input");
  number.classList.add("settingspg");
  number.classList.add("noselect");
  number.classList.add("pgno");
  number.spellcheck = "false";
  number.name = no + "no";
  var name = document.createElement("input");
  name.classList.add("settingspg");
  name.classList.add("noselect");
  name.classList.add("pgname");
  name.spellcheck = "false";
  name.name = no + "name";

  row.appendChild(id);
  row.appendChild(number);
  row.appendChild(name);

  parent.appendChild(row)

  var xhttp = new XMLHttpRequest();

  xhttp.onload = function(){
    console.log(this.responseText);
    id.value = this.responseText;
  }

  xhttp.open("POST","/newpg",true);
  xhttp.send();


}

function rempg(id){

  var fd = new FormData();

  fd.append("id",id)

  var xhttp = new XMLHttpRequest();

  xhttp.onload = function(){

    for(x of document.getElementsByClassName('settingadmintech')){
      if (x.children[0].value == id){
        x.remove();
      }
    }
    //document.getElementById(id+'id').parentElement.remove();
  }

  xhttp.open("POST","/rempg",true);
  xhttp.send(fd);

}
