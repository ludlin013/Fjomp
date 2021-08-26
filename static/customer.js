
if(!document.cookie.includes("custactive")){
  console.log("hitta inget");
  document.getElementById('activecurrent').checked = true;
  document.cookie = "custactive = curr"
}else{
  for(x of document.cookie.split(";")){
    if(x.includes("custactive")){
      var state = x.replace("custactive=","").trim()
      if(state=="curr"){
        console.log(state);
        document.getElementById('activecurrent').checked = true;
        for(m of document.getElementsByClassName('active0')){
          m.style.display = "table-row";
        }
        for(n of document.getElementsByClassName('active1')){
          n.style.display = "none";
        }
      }else if(state=="hist"){
        console.log(state);
        document.getElementById('activehistory').checked = true;
        for(m of document.getElementsByClassName('active1')){
          m.style.display = "table-row";
        }
        for(n of document.getElementsByClassName('active0')){
          n.style.display = "none";
        }
      }else if(state=="both"){
        document.getElementById('activeboth').checked = true;
        for(m of document.getElementsByClassName('active0')){
          m.style.display = "table-row";
        }
        for(n of document.getElementsByClassName('active1')){
          n.style.display = "table-row";
        }
      }
    }
  }
}

function editunit(id){

  var vendor = document.getElementById(id).children[1].children[0].value;
  var model = document.getElementById(id).children[2].children[0].options[document.getElementById(id).children[2].children[0].selectedIndex].text;
  var serial = document.getElementById(id).children[3].children[0].value;
  var install = document.getElementById(id).children[4].children[0].value;
  var warend = document.getElementById(id).children[5].children[0].value;
  var charge = document.getElementById(id).children[6].children[0].value;
  var replace = document.getElementById(id).children[7].children[0].value;

  console.log(replace);

  const fd = new FormData();

  fd.append("id",id)
  fd.append("vendor",vendor)
  fd.append("model",model)
  fd.append("serial",serial)
  fd.append("install",install)
  fd.append("warend",warend)
  fd.append("charge",charge)
  fd.append("replace",replace)

  var xhttp = new XMLHttpRequest();

  xhttp.onload = function(){
    document.getElementById(id+'img').style.filter = "invert()";

    setTimeout(function(){
      document.getElementById(id+'img').style.filter = "";
    },2000)
  }

  xhttp.open("POST","/unitedit",true);
  xhttp.send(fd);


}

function remunit(id){
  const fd = new FormData();

  fd.append("id",id)

  var inactive = false;

  for (x of document.getElementById(id).classList){
    if(x.includes("active1")){
      inactive = true;
    }
  }

  if(inactive){
    fd.append("inactive","true");
    q = "Are you sure you want to delete this unit completely?"
  }else{
    fd.append("inactive","false")
    q = "Are you sure you to make this unit inactive?"
  }

  if(confirm(q)){
    document.getElementById(id).classList.remove("active0");
    document.getElementById(id).classList.add("active1");

    if(inactive){
      document.getElementById(id).remove();
    }

    var xhttp = new XMLHttpRequest();
    xhttp.open("POST","/custremunit",true);
    xhttp.send(fd);
  }
}

function removecust(last){
  const fd = new FormData();

  fd.append("custid",document.getElementById('custidid').value)

  var xhttp = new XMLHttpRequest();
  xhttp.open("POST","/removecust",true);
  xhttp.send(fd);

  window.location.href = "/customers?customer=" + last
}

function savecustomer(){

  var xhttp = new XMLHttpRequest();
  const fd = new FormData(document.getElementById('customerform1'))
  fd.append("custphone",document.getElementById("phoneinput-customers").value)
  fd.append("custopen",document.getElementById("open").value)
  fd.append("custinst",document.getElementById("inst").value)
  fd.append("custclose",document.getElementById("close").value)
  fd.append("custdt",document.getElementById("checkdt").checked)
  fd.append("custwt",document.getElementById("checkwt").checked)
  xhttp.open("POST","/customersave",true);
  console.log(fd.keys());
  xhttp.send(fd);

  //alert("Customer saved")

  document.getElementById('statusmsg').style.maxHeight = "50px";
  document.getElementById('statusmsg').style.borderBottom = "1px solid";

  setTimeout(function(){document.getElementById('statusmsg').style.maxHeight = "0";document.getElementById('statusmsg').style.borderBottom = "0";}, 2000);

}

function warrantycalc(){

  var days = {}

  days["1"] = 0;
  days["2"] = 0;
  days["3"] = 365-1;
  days["4"] = 0;
  days["5"] = (365*2) - 1;
  days["6"] = 0;
  days["7"] = 0;
  days["8"] = (364*3) - 1;
  days["10"] = 0;
  days["11"] = 90;
  days["12"] = 365/2;
  days["9"] = (364*5) - 1;


  var date = document.getElementById('adddate').value.split("-");
  var time = document.getElementById('addcharge').value;

  datt = new Date(date[0],date[1]-1,date[2])

  if(days[time] != 0){
    datt.setDate(datt.getDate() + days[time])

    console.log(datt);
    var dd = datt.getDate();
    var mm = datt.getMonth() + 1;
    var yy = datt.getFullYear();

    if(dd.toString().length == 1){
      dd = "0"+dd;
    }
    if(mm.toString().length == 1){
      mm = "0"+mm;
    }


    document.getElementById('addwarranty').value = yy + "-" + mm + "-" + dd;

  }else{
    document.getElementById('addwarranty').value = 1900 + "-" + "01" + "-" + "01";

  }
}


document.addEventListener("keydown", function(e){
  if ((window.navigator.platform.match("Mac") ? e.metaKey : e.ctrlKey)  && e.keyCode == 83) {
     e.preventDefault();
     savecustomer();
     console.log("vi sparar");
}else if(e.keyCode == 115){
  e.preventDefault();
  document.getElementById('custid').select()
}
}, false);
