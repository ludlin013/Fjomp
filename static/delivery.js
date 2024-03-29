for (x of document.cookie.split(";")){
  if (x.includes("delivfocused")){
    try{
    document.getElementById(x.replace("delivfocused=","").trim()).focus()
  } catch(error){
  }
}
}

function savedelprint(note){
  var noteNum = document.getElementById('delivnote-number').value;
  var storeNum = document.getElementById('storeNumber').value;
  var storeName = document.getElementById('storeName').value;
  var contact = document.getElementById('contact').value;
  var date = document.getElementById('dndate').value;

  var close = document.getElementById('dnclosed').checked;
  var freight = document.getElementById('dnfreight').value;
  var sign = document.getElementById('dnsign').value;
  var notes = document.getElementById('textarea-delivnotes').value;
  var office = document.getElementById('dnoffice').value;
  var pg = document.getElementById('inputnum').value;
  var offer = document.getElementById('dnoffer').checked;
  var final = document.getElementById('dnfinal').checked;


  var fd = new FormData();

   fd.append("noteNum",noteNum);
   fd.append("storeNum",storeNum);
   fd.append("storeName",storeName);
   fd.append("contact",contact);
   fd.append("date",date);
   fd.append("close",close);
   fd.append("freight",freight);
   fd.append("sign",sign);
   fd.append("notes",notes);
   fd.append("office",office);
   fd.append("pg",pg);
   fd.append("offer",offer);
   fd.append("final",final);


  var all = document.getElementsByClassName('forminput-delivnotes3');

  for (x of all){
    if(x.type === "checkbox" ){
      fd.append(x.id,x.checked)
    }else{
      fd.append(x.id,x.value)
    }
  }

  var xhttp = new XMLHttpRequest();

  xhttp.onload = function(){
    window.location.href= '/pdffile?dn=' + note
  }

  xhttp.open("POST","/savedeliv",true);
  xhttp.send(fd);

  document.getElementById('statusmsg').style.maxHeight = "50px";
  document.getElementById('statusmsg').style.borderBottom = "1px solid";

  setTimeout(function(){document.getElementById('statusmsg').style.maxHeight = "0";document.getElementById('statusmsg').style.borderBottom = "0";}, 2000);

}


function savedeldir(){
  var noteNum = document.getElementById('delivnote-number').value;
  var storeNum = document.getElementById('storeNumber').value;
  var storeName = document.getElementById('storeName').value;
  var contact = document.getElementById('contact').value;
  var date = document.getElementById('dndate').value;

  var close = document.getElementById('dnclosed').checked;
  var freight = document.getElementById('dnfreight').value;
  var sign = document.getElementById('dnsign').value;
  var notes = document.getElementById('textarea-delivnotes').value;
  var office = document.getElementById('dnoffice').value;
  var pg = document.getElementById('inputnum').value;
  var offer = document.getElementById('dnoffer').checked;
  var final = document.getElementById('dnfinal').checked;


  var fd = new FormData();

   fd.append("noteNum",noteNum);
   fd.append("storeNum",storeNum);
   fd.append("storeName",storeName);
   fd.append("contact",contact);
   fd.append("date",date);
   fd.append("close",close);
   fd.append("freight",freight);
   fd.append("sign",sign);
   fd.append("notes",notes);
   fd.append("office",office);
   fd.append("pg",pg);
   fd.append("offer",offer);
   fd.append("final",final);


  var all = document.getElementsByClassName('forminput-delivnotes3');

  for (x of all){
    if(x.type === "checkbox" ){
      fd.append(x.id,x.checked)
    }else{
      fd.append(x.id,x.value)
    }
  }

  var xhttp = new XMLHttpRequest();

  xhttp.onload = function(){
    document.cookie = "delivfocused=" + document.activeElement.id + ";path=/";
    location.reload()
  }

  xhttp.open("POST","/savedeliv",true);
  xhttp.send(fd);

  document.getElementById('statusmsg').style.maxHeight = "50px";
  document.getElementById('statusmsg').style.borderBottom = "1px solid";

  setTimeout(function(){document.getElementById('statusmsg').style.maxHeight = "0";document.getElementById('statusmsg').style.borderBottom = "0";}, 2000);

}


function savedel(){
  var noteNum = document.getElementById('delivnote-number').value;
  var storeNum = document.getElementById('storeNumber').value;
  var storeName = document.getElementById('storeName').value;
  var contact = document.getElementById('contact').value;
  var date = document.getElementById('dndate').value;

  var close = document.getElementById('dnclosed').checked;
  var freight = document.getElementById('dnfreight').value;
  var sign = document.getElementById('dnsign').value;
  var notes = document.getElementById('textarea-delivnotes').value;
  var office = document.getElementById('dnoffice').value;
  var pg = document.getElementById('inputnum').value;
  var offer = document.getElementById('dnoffer').checked;
  var final = document.getElementById('dnfinal').checked;


  var fd = new FormData();

   fd.append("noteNum",noteNum);
   fd.append("storeNum",storeNum);
   fd.append("storeName",storeName);
   fd.append("contact",contact);
   fd.append("date",date);
   fd.append("close",close);
   fd.append("freight",freight);
   fd.append("sign",sign);
   fd.append("notes",notes);
   fd.append("office",office);
   fd.append("pg",pg);
   fd.append("offer",offer);
   fd.append("final",final);


  var all = document.getElementsByClassName('forminput-delivnotes3');

  for (x of all){
    if(x.type === "checkbox" ){
      fd.append(x.id,x.checked)
    }else{
      fd.append(x.id,x.value)
    }
  }

  var xhttp = new XMLHttpRequest();

  xhttp.open("POST","/savedeliv",true);
  xhttp.send(fd);

  document.getElementById('statusmsg').style.maxHeight = "50px";
  document.getElementById('statusmsg').style.borderBottom = "1px solid";

  setTimeout(function(){document.getElementById('statusmsg').style.maxHeight = "0";document.getElementById('statusmsg').style.borderBottom = "0";}, 2000);

}

document.addEventListener("keydown", function(e){
  if ((window.navigator.platform.match("Mac") ? e.metaKey : e.ctrlKey)  && e.keyCode == 83) {
     e.preventDefault();
     savedeldir();
}else if((window.navigator.platform.match("Mac") ? e.metaKey : e.ctrlKey)  && e.keyCode == 80){
  savedel();
  e.preventDefault();
  setTimeout(function(){
    document.getElementById("printbutton").click();
  },100)
}else if((window.navigator.platform.match("Mac") ? e.metaKey : e.ctrlKey)  && e.keyCode == 77){
  e.preventDefault();
  savedelmail();
}else if((window.navigator.platform.match("Mac") ? e.metaKey : e.ctrlKey)  && e.keyCode == 81){
  e.preventDefault();
  newunit();
}else if(e.key == "Escape"){
  document.getElementById('storelist').style.display = "none";
}else if((window.navigator.platform.match("Mac") ? e.metaKey : e.ctrlKey)  && e.keyCode == 46){
  e.preventDefault();
  document.getElementById('deletedeliv').click();
}else if((window.navigator.platform.match("Mac") ? e.metaKey : e.ctrlKey)  && e.keyCode == 75){
  e.preventDefault();
  if(confirm("Leave page and create new note? Unsaved changes will be lost")){
    window.location.href = "/newdeliverynote"
  }

}else if((window.navigator.platform.match("Mac") ? e.metaKey : e.ctrlKey)  && e.keyCode == 76){
  e.preventDefault();
  dndone();
}else if((window.navigator.platform.match("Mac") ? e.metaKey : e.ctrlKey)  && e.keyCode == 68){
  e.preventDefault();
  if(confirm("Leave page and copy this note? Unsaved changes will be lost")){
    window.location.href = "/newdeliverynote"
  }

}else if((window.navigator.platform.match("Mac") ? e.metaKey : e.ctrlKey)  && e.keyCode == 90){
  e.preventDefault();
  location.reload();
}else if(e.keyCode == 115){
  e.preventDefault();
  document.getElementById('gotonum').select()
}

}, false);

function priceupdate(row){
  var price = document.getElementById('price'+row).value;
  var discount = document.getElementById('dc'+row).value;

  if (discount){
    document.getElementById('net'+row).value = ((price * (100 - discount))/100).toFixed(2);
  }else{
    document.getElementById('net'+row).value = price;
  }
}

function totalupdate(row){
  var price = document.getElementById('qty'+row).value;
  var net = document.getElementById('net'+row).value;
  document.getElementById('tot'+row).value = (price * net).toFixed(2);


}

function alltotal(){
  var total = 0;

  for (var x = 0; x < document.getElementsByClassName('row-delivnotes').length; x++ ){
      total = total + parseFloat(document.getElementById('tot'+x).value)

  }

  total = parseInt(total).toFixed(2)
  document.getElementById('alltotal').value = total;

}

function setpricegroup(row){
  document.getElementById('price'+row).value = document.getElementById('pg'+row).value.split(" ")[1];
}


alltotal()


function newunit(){

  const fd = new FormData();
  var noteNum = document.getElementById('delivnote-number').value;
  var pg = document.getElementById('inputnum').value;

  fd.append("notenum",noteNum)
  fd.append("pg",pg)

  var xhttp = new XMLHttpRequest();

  xhttp.onload = function(){
    savedeldir()
  }

  xhttp.open("POST","/newdelunit",true);
  xhttp.send(fd);

}

function remdelunit(id){

  if (document.getElementsByClassName('row-delivnotes').length == 1){

    if(confirm("Are you sure? This will delete the delivery note completely")){

      const fd = new FormData();

      fd.append("id",id)

      document.getElementById(id).remove();

      var xhttp = new XMLHttpRequest();
      xhttp.open("POST","/remdelunit",true);
      xhttp.send(fd);

    }
  }else{
    const fd = new FormData();

    fd.append("id",id)

    document.getElementById(id).remove();

    var xhttp = new XMLHttpRequest();
    xhttp.open("POST","/remdelunit",true);
    xhttp.send(fd);
  }
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

function delivpartselect(id, key, price){
  if(key.key == "Enter"){
    var partnum = document.getElementById("num"+id).value;
    var partname = document.getElementById("nam"+id).value;
    var pricegroup = document.getElementById("inputnum").value;

    document.getElementById('idOfPart').value = id;

    fd = new FormData();

    fd.append("partnum", partnum)
    fd.append("partname", partname)
    fd.append("pg", pricegroup)

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
        part.onclick = function(){clickpart(this)}

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
  if(e.key == "Enter"){
    document.getElementById("num"+id).value = e.srcElement.children[0].textContent;
    document.getElementById("nam"+id).value = e.srcElement.children[1].textContent;
    document.getElementById("price"+id).value = e.srcElement.children[3].textContent;
    document.getElementById("qty"+id).value = "1.00";
    priceupdate(id);totalupdate(id);alltotal();
    document.getElementById('partselect').style.display = "none";
    document.getElementById("qty"+document.getElementById("idOfPart").value).select()
    savedel();
  }else if(e.key == "Escape"){
    document.getElementById('partselect').style.display = "none";
    document.getElementById("num"+document.getElementById("idOfPart").value).focus()
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

function clickpart(c){
  var id = document.getElementById("idOfPart").value;

    document.getElementById("num"+id).value = c.children[0].textContent;
    document.getElementById("nam"+id).value = c.children[1].textContent;
    document.getElementById("price"+id).value = c.children[3].textContent;
    document.getElementById("qty"+id).value = "1.00";
    priceupdate(id);totalupdate(id);alltotal();
    document.getElementById('partselect').style.display = "none";
    document.getElementById("qty"+document.getElementById("idOfPart").value).select();

    savedel();
}

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
        store = stores[0].split("\t");

        document.getElementById("storeNumber").value = store[0];
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
        fd.append("noteid",document.getElementById("delivnote-number").value)
        fd.append("name",store[1])
        fd.append("pg",store[6])

        var xhttp = new XMLHttpRequest();
        xhttp.open("POST","/savestore",true);
        xhttp.send(fd);

        for(x of document.getElementsByClassName('numfoc')){
          x.focus()
        }
      }
    }

    xhttp.open("POST","/delivstoreselect",true);
    xhttp.send(fd);
  }
}

function chooseStore(e){
  if(e.key == "Enter"){
    document.getElementById('storelist').style.display = "none";
    document.getElementById("storeNumber").value = e.srcElement.children[0].textContent;

    document.getElementById("contact").value = e.srcElement.children[1].textContent;

    document.getElementById("storeName").value = e.srcElement.children[2].textContent;
    document.getElementById("storestreet").value = e.srcElement.children[3].textContent;
    document.getElementById("City").value = e.srcElement.children[5].textContent;
    document.getElementById("ZIP").value = e.srcElement.children[4].textContent;

    document.getElementById("inputnum").value = e.srcElement.children[6].textContent;

    for (x of document.getElementsByClassName('forminput-delivnotes3')){
      if(x.id.includes("pg")){
        x.value = e.srcElement.children[6].textContent;
      }

    }

    const fd = new FormData();

    fd.append("store",e.srcElement.children[0].textContent)
    fd.append("contact",e.srcElement.children[1].textContent)
    fd.append("noteid",document.getElementById("delivnote-number").value)
    fd.append("name",e.srcElement.children[2].textContent)
    fd.append("pg",e.srcElement.children[6].textContent)

    var xhttp = new XMLHttpRequest();
    xhttp.open("POST","/savestore",true);
    xhttp.send(fd);



    document.getElementById('contact').focus()

  } else if(e.key == "Escape"){
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
  document.getElementById('storelist').style.display = "none";
  document.getElementById("storeNumber").value = chosen.children[0].textContent;


  document.getElementById("contact").value = chosen.children[1].textContent;


  document.getElementById("storeName").value = chosen.children[2].textContent;
  document.getElementById("storestreet").value = chosen.children[3].textContent;
  document.getElementById("City").value = chosen.children[5].textContent;
  document.getElementById("ZIP").value = chosen.children[4].textContent;

  document.getElementById("inputnum").value = chosen.children[6].textContent;

  for (x of document.getElementsByClassName('forminput-delivnotes3')){
    if(x.id.includes("pg")){
      x.value = chosen.children[6].textContent;
    }

  }

  const fd = new FormData();

  fd.append("store",chosen.children[0].textContent)
  fd.append("contact",chosen.children[1].textContent)
  fd.append("noteid",document.getElementById("delivnote-number").value)
  fd.append("name",chosen.children[2].textContent)
  fd.append("pg",chosen.children[6].textContent)

  var xhttp = new XMLHttpRequest();
  xhttp.open("POST","/savestore",true);
  xhttp.send(fd);

  document.getElementById('contact').focus()

}

for(x of document.getElementsByClassName('numfoc')){

  if(x.value == ""){
    x.focus();
  }
}

if(document.getElementById("storeNumber").value == ""){
  document.getElementById("storeNumber").focus()
}





function selectpg(pgid, row){

  var part = document.getElementById('num'+row).value;

  const fd = new FormData();

  fd.append("pgid",pgid)
  fd.append("part",part)

  var xhttp = new XMLHttpRequest();

  xhttp.onload = function(){

    document.getElementById('price'+row).value = this.responseText;
    priceupdate(row);
    totalupdate(row);
    alltotal()
  }

  xhttp.open("POST","/setpricegroup",true);
  xhttp.send(fd);
}

function dndone(){

  document.getElementById("dnclosed").checked = "checked";

  savedelmail(true);

}
