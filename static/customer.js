
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

  alert("Customer saved")
}
