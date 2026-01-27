/*document.getElementById('gotosw').addEventListener("keydown", function(e){
  if(e.keyCode == 13){
    window.location.href = '/swapouts?sw='+document.getElementById('gotosw').value
  }
}, false);*/

document.getElementById('opensw').addEventListener("keydown", function (e) {
  if (e.keyCode == 13) {
    window.location.href = '/swapouts?sw=' + document.getElementById('opensw').value
  }
}, false);

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

  if(id == "SWP_RepReturn" && document.getElementById("SWP_Loan").checked == false || id == "SWP_LoanReturn" && document.getElementById("SWP_Loan").checked == false){
    return;
  }

  document.getElementById(id).value = date;
  window.getSelection().removeAllRanges()
}

function saveitem(id){
  var sw = document.getElementById("opensw");
  var item = document.getElementById(id);
  
  fd = new FormData();

  fd.append("swap", sw.value);
  fd.append("type", id);
  
  if(item.type=="checkbox"){
    var check = 0;

    if (item.checked==true){
      check = 1;
    }

  fd.append("item", check);
  }else{
  fd.append("item", item.value);

  }


  const xhttp = new XMLHttpRequest();

  xhttp.onload = function(){
    console.log("Sparad");

    //document.getElementById(id).style.background = "green";

    setTimeout(function () { 
      //document.getElementById(id).style.background =  "rgb(80,80,80)"; 
    }, 500);
  }


  xhttp.open("POST","/swapsaveitem",true);
  xhttp.send(fd);

}


document.getElementById('storenumber').addEventListener("keydown", getstore);

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

        document.getElementById("SWP_Contact").value = store[5];
        document.getElementById("storenumber").value = store[0];
        document.getElementById("storeName").value = store[1];
        document.getElementById("storestreet").value = store[2];
        document.getElementById("irzip").value = store[3];
        document.getElementById("ircity").value = store[4];

        console.log("Spara store");

        //document.getElementById("phone").value = store[6];

        for (x of document.getElementsByClassName('forminput-delivnotes3')){
          if(x.id.includes("pg")){
            x.value = store[6];
          }

        }

        const fd = new FormData();

        fd.append("store",store[0])
        fd.append("SWP_Contact",store[5])
        fd.append("noteid",document.getElementById("opensw").value)
        //fd.append("name",store[1])

        var xhttp = new XMLHttpRequest();
        xhttp.open("POST","/swapsavestore",true);
        xhttp.send(fd);

        for(x of document.getElementsByClassName('numfoc')){
          x.focus()
        }
        //swapsavestore();
      }
    }

    xhttp.open("POST","/swapstoreselect",true);
    xhttp.send(fd);
  }
}

function chooseStore(e){
  console.log(e.keyCode);
  if(e.key == "Enter"){
    document.getElementById('storelist').style.display = "none";
    document.getElementById("storenumber").value = e.srcElement.children[0].textContent;

    document.getElementById("SWP_Contact").value = e.srcElement.children[1].textContent;

    document.getElementById("storeName").value = e.srcElement.children[2].textContent;
    document.getElementById("storestreet").value = e.srcElement.children[3].textContent;
    document.getElementById("ircity").value = e.srcElement.children[5].textContent;
    document.getElementById("irzip").value = e.srcElement.children[4].textContent;

    const fd = new FormData();

    fd.append("store",e.srcElement.children[0].textContent)
    fd.append("SWP_Contact",e.srcElement.children[1].textContent)
    fd.append("noteid",document.getElementById("opensw").value)
    fd.append("name",e.srcElement.children[2].textContent)

    var xhttp = new XMLHttpRequest();
    xhttp.onload = function(){
      //hiddensave();
    }
    xhttp.open("POST","/swapsavestore",true);
    xhttp.send(fd);

    document.getElementById('SWP_NewPartno').focus()

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
  document.getElementById("storenumber").value = chosen.children[0].textContent;


  document.getElementById("SWP_Contact").value = chosen.children[1].textContent;


  document.getElementById("storeName").value = chosen.children[2].textContent;
  document.getElementById("storestreet").value = chosen.children[3].textContent;
  document.getElementById("ircity").value = chosen.children[5].textContent;
  document.getElementById("irzip").value = chosen.children[4].textContent;

  const fd = new FormData();

  xhttp.onload = function(){
    //hiddensave();
  }

  fd.append("store",chosen.children[0].textContent)
  fd.append("SWP_Contact",chosen.children[1].textContent)
  fd.append("noteid",document.getElementById("opensw").value)
  fd.append("name",chosen.children[2].textContent)

  var xhttp = new XMLHttpRequest();
  xhttp.onload = function(){
    //hiddensave();
  }
  xhttp.open("POST","/swapsavestore",true);
  xhttp.send(fd);

  document.getElementById('SWP_NewPartno').focus()

}


function loanusable(){
  var loan = document.getElementsByClassName("loan");
  var check = document.getElementById("SWP_Loan").checked;
  var tech = document.getElementsByClassName("loantech");

  if(check == "1"){
    for(x of loan){
      x.readOnly = false;
      x.style.color = null;
    }

    for(x of tech){
      x.disabled = false;
    }
  }

  else if(check == "0"){
    console.log("0")
    for(x of loan){
      x.readOnly = true;
      x.value = "";
      x.style.color = "grey"
    }

    for(x of tech){
      x.disabled = true;
    }
  }
  

}

function swapreplace(swp){

  if(!confirm('Är du säker?')){
    return
  }

  const fd = new FormData();

  fd.append("SWP_ID",swp)

  var xhttp = new XMLHttpRequest();
  xhttp.onload = function(){
    if (this.status == 200){
      alert(xhttp.response)
    }
    
  }
  xhttp.open("POST","/swapreplace",true);
  xhttp.send(fd);

}