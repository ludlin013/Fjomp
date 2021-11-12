document.getElementById('gotoir').addEventListener("keydown", function(e){
  if(e.keyCode == 13){
    window.location.href = '/ir?ir='+document.getElementById('gotoir').value
  }
}, false);

var allrepact = document.getElementsByClassName('irrepact');
var allirunit = document.getElementsByClassName('irunitselect');
for (x of allrepact){
  x.style.display = "none";
}
try{
  allrepact[0].style.display = "flex";
  allirunit[0].style.display = "none";
}catch(error){
  console.log("no actions");
}




function update(inf){
  var vendor = inf.split("%")[0]
  var type = inf.split("%")[1]
  var id = inf.split("%")[2]

  console.log(0+vendor.trim());

  document.getElementById(id+'type').value = type.trim();
  document.getElementById(id+'vendor').value = vendor.trim();
}

function changerepact(idd){
  for (x of allrepact){
    x.style.display = "none";
  }

  for (x of allirunit){
    x.style.display = "block";
  }

  try{
    document.getElementById(idd.replace("repact","button")).style.display = "none"
  }catch(error){
    console.log(error);
  }
  for (x of document.getElementsByClassName(idd)){
    x.style.display = "flex"
  }

  //document.getElementById(idd.replace("repact","type")).parentElement.parentElement.style.border = "4px solid #fff"
  //document.getElementById(idd.replace("repact","type")).parentElement.parentElement.style.background = "#fff"
try{
  var serial = document.getElementById(idd.replace("repact","type")).parentElement.parentElement.childNodes[7].childNodes[0].value;
  var model = document.getElementById(idd.replace("repact","type")).parentElement.parentElement.childNodes[5].childNodes[1].options[document.getElementById(idd.replace("repact","type")).parentElement.parentElement.childNodes[5].childNodes[1].selectedIndex].text
  var ir = document.getElementById('irirn').value;
}catch(error){
  console.log(error);
}

  document.getElementById('ir-add').onclick = function(){ newspare(model + "%" + serial + "%" + ir) };
  document.getElementById('irunitremove').onclick = function(){removeunit(document.getElementById(idd.replace("repact","id")).value)};
}

changerepact('0repact')


function removeunit(arg){
  console.log(arg);

  var fd = new FormData();

  fd.append("unitid",arg);

  var xhttp = new XMLHttpRequest();
  xhttp.open("POST","/remunit",true);
  xhttp.send(fd);

  document.getElementById(arg+"id").style.display = "none";
}


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
  saveir()
  var xhttp = new XMLHttpRequest();
  const fd = new FormData(document.getElementById('allform'))
  xhttp.open("POST","/irsaveall",true);
  console.log(fd.keys());
  xhttp.send(fd);



  xhttp.onload = function(){
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

    setTimeout(function(){
      location.reload();
    },500);
  }

  document.getElementById('statusmsg').style.maxHeight = "50px";
  document.getElementById('statusmsg').style.borderBottom = "1px solid";

  setTimeout(function(){document.getElementById('statusmsg').style.maxHeight = "0";document.getElementById('statusmsg').style.borderBottom = "0";}, 2000);



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

function irpartselect(id, key, price){
  if(key.key == "Enter"){
    var partnum = document.getElementById(id+"num").value;
    var partname = document.getElementById(id+"nam").value;

    document.getElementById('idOfPart').value = id;

    fd = new FormData();

    fd.append("partnum", partnum)
    fd.append("partname", partname)
    fd.append("pg", price)

    const xhttp = new XMLHttpRequest();



    xhttp.onload = function() {
      document.getElementById('partselect').style.display = "flex";

      var parent = document.getElementById('partselect');

      parent.innerHTML = "";

      var parts = this.responseText.split("\n");
      parts.splice(parts.length-1, 1)


      for(x of parts){
        var part = document.createElement("div");
        part.classList.add("partitem");
        part.tabIndex = "0";
        part.addEventListener('keydown',choosePart)
        part.addEventListener('mousedown',choosePart)

        var num = document.createElement("p");
        num.classList.add("partnum")
        var name = document.createElement("p");
        name.classList.add("partname")
        var price = document.createElement("p");
        price.classList.add("partprice")
        var qty = document.createElement("p");
        qty.classList.add("partqty")

        num.appendChild(document.createTextNode(x.split("\t")[0]));
        name.appendChild(document.createTextNode(x.split("\t")[1]));
        price.appendChild(document.createTextNode(x.split("\t")[2]));
        qty.appendChild(document.createTextNode(x.split("\t")[3]));

        part.appendChild(num);
        part.appendChild(name);
        part.appendChild(price);
        part.appendChild(qty);

        parent.appendChild(part);
      }
      document.getElementsByClassName('partitem')[0].focus();
    }

    xhttp.open("POST","/delivpartselect",true);
    xhttp.send(fd);
  }
}

function choosePart(e){
  var id = document.getElementById("idOfPart").value;
  if(e.key == "Enter" || e.button == 0){
    document.getElementById(id+"num").value = e.srcElement.children[0].textContent;
    document.getElementById(id+"nam").value = e.srcElement.children[1].textContent;
    document.getElementById("price"+id).value = e.srcElement.children[3].textContent;
    document.getElementById("qty"+id).value = "1.00";
    document.getElementById('partselect').style.display = "none";
    document.getElementById("price"+document.getElementById("idOfPart").value).focus()
  }else if(e.key == "Escape"){
    document.getElementById('partselect').style.display = "none";
    document.getElementById(document.getElementById("idOfPart").value + "num").focus()
  }else if(e.keyCode == "40"){
    e.preventDefault();
    var me = e.srcElement;
    var stop = false;
    for(x of document.getElementsByClassName('partitem')){
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
    for(x of document.getElementsByClassName('partitem')){
      if (x == me){
        break
      }
      stop = x;

    }

    stop.focus()
  }
}

document.getElementById('storenumber').addEventListener("keydown", getstore);
console.log("store");

function getstore(e){
  console.log("Sök kund");
  if(e.key == "Enter"){

    fd = new FormData();

    fd.append("search", document.getElementById('storenumber').value)

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
        store = stores[0].split("\t");

        document.getElementById("storenumber").value = store[0];
        document.getElementById("storeName").value = store[1];
        document.getElementById("storestreet").value = store[2];
        document.getElementById("ZIP").value = store[3];
        document.getElementById("City").value = store[4];

        document.getElementById("contact").value = store[5];


        document.getElementById("inputnum").value = store[6];

        for (x of document.getElementsByClassName('forminput-delivnotes3')){
          if(x.id.includes("pg")){
            x.value = store[6];
          }

        }

        const fd = new FormData();

        fd.append("store",store[0])
        fd.append("contact",store[5])
        fd.append("noteid",document.getElementById("irirn").value)
        fd.append("name",store[1])

        var xhttp = new XMLHttpRequest();
        xhttp.open("POST","/savestore",true);
        xhttp.send(fd);

        for(x of document.getElementsByClassName('numfoc')){
          x.focus()
        }
      }
    }

    xhttp.open("POST","/irstoreselect",true);
    xhttp.send(fd);
  }
}
