
var allrepact = document.getElementsByClassName('irrepact');
for (x of allrepact){
  x.style.display = "none";
}
allrepact[0].style.display = "flex";


function update(inf){
  var vendor = inf.split("%")[0]
  var type = inf.split("%")[1]
  var id = inf.split("%")[2]

  console.log(0+vendor.trim());

  document.getElementById(id+'type').value = type.trim();
  document.getElementById(id+'vendor').value = vendor.trim();
}

function changerepact(idd){
  console.log(idd);
  for (x of allrepact){
    x.style.display = "none";
  }

  for (x of document.getElementsByClassName(idd)){
    x.style.display = "flex"
  }

  document.getElementById(idd.replace("repact","type")).parentElement.parentElement.style.border = "4px solid #fff"
  document.getElementById(idd.replace("repact","type")).parentElement.parentElement.style.background = "#fff"

  var serial = document.getElementById(idd.replace("repact","type")).parentElement.parentElement.childNodes[7].childNodes[0].value;
  var model = document.getElementById(idd.replace("repact","type")).parentElement.parentElement.childNodes[5].childNodes[1].options[document.getElementById(idd.replace("repact","type")).parentElement.parentElement.childNodes[5].childNodes[1].selectedIndex].text
  var ir = document.getElementById('irirn').value;

  document.getElementById('ir-add').onclick = function(){ newspare(model + "%" + serial + "%" + ir) };
}

changerepact('0repact')

var active = false;

function setday(id){
  var y = new Date().getFullYear();
  var m = "0" + (new Date().getMonth()+1);
  var d = "0" + new Date().getDate();

  if (m.length>2){
    m = m.substring(1)
  }

  if (d.length>2){
    d = d.substring(1)
  }

  var date = y + "-"+m+"-"+d
  id.value = date;
  window.getSelection().removeAllRanges()
}

function newspare(arg){
  console.log(arg);

  var fd = new FormData();

  var model = arg.split("%")[0];
  var serial = arg.split("%")[1];
  var irn = arg.split("%")[2];

  fd.append("model",model);
  fd.append("serial",serial);
  fd.append("irn",irn);


  var xhttp = new XMLHttpRequest();
  xhttp.open("POST","/newspare",true);
  xhttp.send(fd);
  location.reload();
}

function selectspare(arg){

  document.getElementById('ir-rem').onclick = function(){ removespare(arg) };
}

function removespare(arg){
  console.log(arg);

  var fd = new FormData();

  fd.append("partid",arg);

  var xhttp = new XMLHttpRequest();
  xhttp.open("POST","/remspare",true);
  xhttp.send(fd);

  document.getElementById("list2-ir" + arg).style.display = "none";
}
