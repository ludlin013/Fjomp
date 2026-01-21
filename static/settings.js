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

function savemod(){
  var xhttp = new XMLHttpRequest();
  xhttp.open("POST","/savemodels",true);
  const fd = new FormData(document.getElementById('modform'));
  for(var x of fd.entries()){
    console.log(x[0] + ": " + x[1]);
  }

  xhttp.onload = function(){
    document.getElementById('modsave').textContent = "Saved!"
  }

  xhttp.send(fd);
}

function newmod(){
  var xhttp = new XMLHttpRequest();
  xhttp.open("POST","/newmodel",true);
  xhttp.send();
  xhttp.onload = function(){
    location.reload();
  }

}


function newve(){
  var xhttp = new XMLHttpRequest();
  xhttp.open("POST","/newve",true);
  xhttp.send();
  xhttp.onload = function(){
    location.reload();
  }

}

function newfe(){
  var xhttp = new XMLHttpRequest();
  xhttp.open("POST","/newfe",true);
  xhttp.send();
  xhttp.onload = function(){
    location.reload();
  }

}

function savefe(){
  var xhttp = new XMLHttpRequest();
  const fd = new FormData(document.getElementById('feform'));

  xhttp.onload = function(){
    document.getElementById('fesave').textContent = "Saved!"
  }

  xhttp.open("POST","/savefe",true);
  xhttp.send(fd);

}

function remfe(id){

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



  xhttp.open("POST","/remfe",true);
  xhttp.send(fd);

}

function savecp(){
  var xhttp = new XMLHttpRequest();
  const fd = new FormData(document.getElementById('cpform'));

  xhttp.onload = function(){
    document.getElementById('cpsave').textContent = "Saved!"
  }

  xhttp.open("POST","/savecp",true);
  xhttp.send(fd);

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

function savepredef(){
  var xhttp = new XMLHttpRequest();
  const fd = new FormData(document.getElementById('predefform'));

  console.log(fd);
  

  xhttp.onload = function(){
    document.getElementById('pgsave').textContent = "Saved!"
  }

  xhttp.open("POST","/savepredef",true);
  xhttp.send(fd);

}

function saveve(){
  var xhttp = new XMLHttpRequest();
  const fd = new FormData(document.getElementById('veform'));

  xhttp.onload = function(){
    document.getElementById('vesave').textContent = "Saved!"
  }

  xhttp.open("POST","/saveve",true);
  xhttp.send(fd);

}

function savech(){
  var xhttp = new XMLHttpRequest();
  const fd = new FormData(document.getElementById('chform'));

  xhttp.onload = function(){
    document.getElementById('chsave').textContent = "Saved!"
  }

  xhttp.open("POST","/savech",true);
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

  //parent.appendChild(row)

  var xhttp = new XMLHttpRequest();

  xhttp.onload = function(){
    console.log(this.responseText);
    id.value = this.responseText;

    location.reload();
  }

  xhttp.open("POST","/newpg",true);
  xhttp.send();


}

function newch(){
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

  //parent.appendChild(row)

  var xhttp = new XMLHttpRequest();

  xhttp.onload = function(){
    console.log(this.responseText);
    id.value = this.responseText;

    location.reload();
  }

  xhttp.open("POST","/newch",true);
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

function remve(id){

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



  xhttp.open("POST","/remve",true);
  xhttp.send(fd);

}


function remch(id){

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



  xhttp.open("POST","/remch",true);
  xhttp.send(fd);

}

function remmod(id){

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



  xhttp.open("POST","/remmod",true);
  xhttp.send(fd);

}

function savete(){
  var xhttp = new XMLHttpRequest();

  var notech = []

  for(x of document.getElementsByClassName('techcheck')){
    console.log(x.value);
    if(x.checked == false){
      notech.push(x)
      x.value = 0;
      x.checked = true;
    }
  }

  const fd = new FormData(document.getElementById('teform'));

  xhttp.onload = function(){
    for(x of notech){
      x.value = 1;
      x.checked = false;
    }
    document.getElementById('tesave').textContent = "Saved!";

    setTimeout(function(){
      document.getElementById('tesave').textContent = "Save";
    }, 5000);
  }

  xhttp.open("POST","/savete",true);
  xhttp.send(fd);

}


function newte(){


  var no = document.getElementById("teform").children[document.getElementById("teform").children.length - 1].children[0].name;
  console.log(no);
  no = parseInt(no)+1

  var parent = document.getElementById('teform');
  var row = document.createElement("a");
  row.classList.add("settingadmintech");

  var id = document.createElement("input");
  id.name = no + "id";
  id.type = "hidden";
  var nid = document.createElement("input");
  nid.classList.add("settingspg");
  nid.classList.add("noselect");
  nid.classList.add("teid");
  nid.spellcheck = "false";
  nid.name = no + "ids";
  nid.maxLength = "3";
  var first = document.createElement("input");
  first.classList.add("settingspg");
  first.classList.add("noselect");
  first.classList.add("tefirst");
  first.spellcheck = "false";
  first.name = no + "first";
  var last = document.createElement("input");
  last.classList.add("settingspg");
  last.classList.add("noselect");
  last.classList.add("telast");
  last.spellcheck = "false";
  last.name = no + "last";
  var office = document.createElement("input");
  office.classList.add("settingspg");
  office.classList.add("noselect");
  office.classList.add("teoffice");
  office.spellcheck = "false";
  office.name = no + "office";

  var telabel = document.createElement("label");
  telabel.classList.add("settingspg");
  telabel.classList.add("noselect");
  telabel.classList.add("tetech");

  var techte = document.createElement("input");
  techte.classList.add("techcheck");
  techte.type = "checkbox";
  techte.value = "1";
  techte.spellcheck = "false";
  techte.name = no + "tech";

  telabel.appendChild(techte);

  row.appendChild(id);
  row.appendChild(nid);
  row.appendChild(first);
  row.appendChild(last);
  row.appendChild(office);
  row.appendChild(telabel);


  //parent.appendChild(row)

  var xhttp = new XMLHttpRequest();

  xhttp.onload = function(){
    console.log(this.responseText);
    id.value = this.responseText;
    location.reload();


  }

  xhttp.open("POST","/newte",true);
  xhttp.send();


}

function remtech(id){

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

  xhttp.open("POST","/remte",true);
  xhttp.send(fd);

}

function saveof(){
  var xhttp = new XMLHttpRequest();
  const fd = new FormData(document.getElementById('ofform'));

  xhttp.onload = function(){
    document.getElementById('ofsave').textContent = "Saved!"
  }

  xhttp.open("POST","/saveof",true);
  xhttp.send(fd);

}

function newof(){
  var no = document.getElementById("ofform").children[document.getElementById("ofform").children.length - 1].children[0].name.substring(0,1);
  no = parseInt(no)+1

  var parent = document.getElementById('ofform');
  var row = document.createElement("a");
  row.classList.add("settingadmintech");

  var id = document.createElement("input");
  id.name = no + "id";
  id.type = "hidden";
  var number = document.createElement("input");
  number.classList.add("settingsof");
  number.classList.add("noselect");
  number.classList.add("ofno");
  number.spellcheck = "false";
  number.name = no + "no";
  var name = document.createElement("input");
  name.classList.add("settingsof");
  name.classList.add("noselect");
  name.classList.add("ofname");
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

  xhttp.open("POST","/newof",true);
  xhttp.send();


}

function clearCookies(){
  if(confirm('Do you want to clear all cookies?')){
    document.cookie = "custactive=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    document.cookie = "custid=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    document.cookie = "irselected=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    document.cookie = "lastbtwdate1=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    document.cookie = "lastbtwdate2=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    document.cookie = "lastdes=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    document.cookie = "lastdn=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    document.cookie = "lastir=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    document.cookie = "lastlooknumname=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    document.cookie = "lastpar=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    document.cookie = "lastserial=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    document.cookie = "rbball=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    alert('Cookies was deleted successfully!')
  }else{
    alert('Cookies was not deleted')
  }
}

function remof(id){

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



  xhttp.open("POST","/remof",true);
  xhttp.send(fd);

}
