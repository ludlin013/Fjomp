console.log("hello");

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
          console.log(state);
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

  document.getElementById(id).remove();

  var xhttp = new XMLHttpRequest();
  xhttp.open("POST","/custremunit",true);
  xhttp.send(fd);
}
