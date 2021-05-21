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
        for(m of document.getElementsByClassName('0active')){
          m.style.display = "table-row";
        }
        for(n of document.getElementsByClassName('1active')){
          n.style.display = "none";
        }
      }else if(state=="hist"){
        console.log(state);
        document.getElementById('activehistory').checked = true;
          for(m of document.getElementsByClassName('1active')){
            m.style.display = "table-row";
          }
          for(n of document.getElementsByClassName('0active')){
            n.style.display = "none";
          }
        }else if(state=="both"){
          console.log(state);
          document.getElementById('activeboth').checked = true;
          for(m of document.getElementsByClassName('0active')){
            m.style.display = "table-row";
          }
          for(n of document.getElementsByClassName('1active')){
            n.style.display = "table-row";
          }
      }
    }
  }
}
