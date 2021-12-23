try{
if(!document.cookie.includes("custactive")){
  document.getElementById('activecurrent').checked = true;
  document.cookie = "custactive = curr"
}else{
  for(x of document.cookie.split(";")){

    if(x.includes("custactive")){
      var state = x.replace("custactive=","").trim()
      if(state=="curr"){
        document.getElementById('activecurrent').checked = true;
        for(m of document.getElementsByClassName('active0')){
          m.style.display = "table-row";
        }
        for(n of document.getElementsByClassName('active1')){
          n.style.display = "none";
        }
      }else if(state=="hist"){
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

document.getElementById('unitaddvend').value = "";
document.getElementById('addmodel').value = "";
document.getElementById('addserial').value = "";
document.getElementById('adddate').value = "";
document.getElementById('addcharge').value = "";
document.getElementById('addwarranty').value = "";

function addunit(){
  const fd = new FormData();
  var xhttp = new XMLHttpRequest();

  xhttp.responseType = 'text';

  fd.append("customer", document.getElementById('custidid').value);
  fd.append("vendor", document.getElementById('unitaddvend').value);
  fd.append("model", document.getElementById('addmodel').value);
  fd.append("serial", document.getElementById('addserial').value);
  fd.append("date", document.getElementById('adddate').value);
  fd.append("charge", document.getElementById('addcharge').value);
  fd.append("warranty", document.getElementById('addwarranty').value);

  xhttp.onload = function(){
    document.getElementById('unitmsg').innerHTML = xhttp.responseText;
    document.getElementById('unitmsg').style.maxHeight = "50px";
    document.getElementById('unitmsg').style.borderBottom = "1px solid";

    setTimeout(function(){document.getElementById('unitmsg').style.maxHeight = "0";document.getElementById('unitmsg').style.borderBottom = "0";}, 2000);

  }

  xhttp.open("POST","/customernewunit",true);
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
}
catch(error){
  console.log(error);
}

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
  document.getElementById(id).value = date;
  window.getSelection().removeAllRanges()
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
}else if(e.keyCode == 115){
  e.preventDefault();
  document.getElementById('custid').select()
}
}, false);


document.getElementById('storeNumber').addEventListener("keydown", getstore);


function getstore(e){
  if(e.key == "Enter"){

    fd = new FormData();

    fd.append("search", document.getElementById('storeNumber').value)

    const xhttp = new XMLHttpRequest();



    xhttp.onload = function(){
      var stores = this.responseText.split("\n");
      stores.splice(stores.length-1, 1);

      var parent = document.getElementById('storelist');
      parent.innerHTML = ""

      if(stores.length > 1){
        parent.style.display = "flex";
        for (x of stores){
          var store = x.split("\t");

          var storeitem = document.createElement("div");
          storeitem.classList.add("storeitem");
          storeitem.tabIndex = "0";
          storeitem.addEventListener('keydown',chooseStore)
          storeitem.onclick = function(){clickstore(this)};

          var id = document.createElement("p");
          id.classList.add("storeid")
          var ref = document.createElement("p");
          ref.classList.add("storeref")
          var name = document.createElement("p");
          name.classList.add("storename")
          var street = document.createElement("p");
          street.classList.add("storestreet")
          var zip = document.createElement("p");
          zip.classList.add("storezip")
          var city = document.createElement("p");
          city.classList.add("storecity")
          var pg = document.createElement("p");
          pg.classList.add("storepg")

          id.appendChild(document.createTextNode(x.split("\t")[0]));
          ref.appendChild(document.createTextNode(x.split("\t")[5]));
          name.appendChild(document.createTextNode(x.split("\t")[1]));
          street.appendChild(document.createTextNode(x.split("\t")[2]));
          zip.appendChild(document.createTextNode(x.split("\t")[3]));
          city.appendChild(document.createTextNode(x.split("\t")[4]));
          pg.appendChild(document.createTextNode(x.split("\t")[6]));

          storeitem.appendChild(id);
          storeitem.appendChild(ref);
          storeitem.appendChild(name);
          storeitem.appendChild(street);
          storeitem.appendChild(zip);
          storeitem.appendChild(city);
          storeitem.appendChild(pg);

          parent.appendChild(storeitem)

        }
        document.getElementsByClassName('storeitem')[0].focus();
      }else{
        try{
          store = stores[0].split("\t");
          document.cookie = "custid = "+store[0]+"; expires=Thu, 01 Jan 2077 00:00:00 UTC; path=/;"
          window.location.href = "customers?customer=" + store[0];
        }catch(error){
          document.getElementById('error').innerHTML = "No customers found"
        }


      }
    }

    xhttp.open("POST","/custstoreselect",true);
    xhttp.send(fd);
  }
}

function chooseStore(e){
  if(e.key == "Enter"){
    document.cookie = "custid = "+e.srcElement.children[0].textContent+"; expires=Thu, 01 Jan 2077 00:00:00 UTC; path=/;"

    window.location.href = "customers?customer=" + e.srcElement.children[0].textContent;



  } else if(e.key == "Escape"){
    document.getElementById('storeNumber').select();
    document.getElementById('storelist').style.display = "none";
  } else if(e.keyCode == "40"){
    e.preventDefault();
    var me = e.srcElement;
    var stop = false;
    for(x of document.getElementsByClassName('storeitem')){
      if(stop == true){
        break
      }
      if (x == me){
        stop = true;
      }

    }

    x.focus()
  } else if(e.keyCode == "38"){
    e.preventDefault();
    var me = e.srcElement;
    var stop = me;
    for(x of document.getElementsByClassName('storeitem')){
      if (x == me){
        break
      }
      stop = x;

    }

    stop.focus()
  }


}

function clickstore(chosen){

  document.cookie = "custid = "+chosen.children[0].textContent+"; expires=Thu, 01 Jan 2077 00:00:00 UTC; path=/;"

  window.location.href = "customers?customer=" + chosen.children[0].textContent;


}
