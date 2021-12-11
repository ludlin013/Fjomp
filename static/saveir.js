
function saveir(){
  var irirn = document.getElementById("irirn");
  var cid = document.getElementById("storenumber");
  var opdate = document.getElementById("iropendate");
  var redate = document.getElementById("irredate");
  var shdate = document.getElementById("irshipdate");
  var techid = document.getElementById("irrepairid");
  var note = document.getElementById("irnotefield");
  var infreight =document.getElementById("irinfreight");
  var outfreight = document.getElementById("irrefreight");
  var closed = document.getElementById("irclosed");
  var openid = document.getElementById("techid");
  var office = document.getElementById("irloc");

  var send = [irirn,cid,opdate,redate,shdate,techid,note,infreight,outfreight,closed,openid,office]

  console.log(send);

  for(x of send){
    if(x!=""){
      console.log(x);
      document.getElementById("save"+x.id).value = x.value;
    }
  }
  /*
  var xhttp = new XMLHttpRequest();

  const sparedata = new FormData(document.getElementById('sparepartform'));
  console.log(sparedata.keys());
  xhttp.open("POST","/savespare",true);
  xhttp.send(sparedata);
  setTimeout(formir(), 1000);
  unitsave()

  */
}
function formir(){
  var xhttp = new XMLHttpRequest();
  xhttp.open("POST","/saveir",true);
  const fd = new FormData(document.getElementById('irsaveform'));
  xhttp.send(fd);
}

function unitsave(){
  var xhttp = new XMLHttpRequest();
  const fd = new FormData(document.getElementById('irunitform'))
  xhttp.open("POST","/unitsave",true);
  console.log(fd.keys());
  xhttp.send(fd);

}

function saveall(){
  saveir()
  var xhttp = new XMLHttpRequest();
  const fd = new FormData(document.getElementById('allform'))
  xhttp.open("POST","/irsaveall",true);
  console.log(fd.keys());
  xhttp.send(fd);

  document.getElementById('statusmsg').style.maxHeight = "50px";
  document.getElementById('statusmsg').style.borderBottom = "1px solid";

  setTimeout(function(){document.getElementById('statusmsg').style.maxHeight = "0";document.getElementById('statusmsg').style.borderBottom = "0";}, 2000);

}

function hiddensave(){
  saveir()
  var xhttp = new XMLHttpRequest();
  const fd = new FormData(document.getElementById('allform'))
  xhttp.open("POST","/irsaveall",true);
  console.log(fd.keys());
  xhttp.send(fd);
}


function savenewunit(id){
  saveir()
  var xhttp = new XMLHttpRequest();
  const fd = new FormData(document.getElementById('allform'))
  xhttp.open("POST","/irsaveall",true);
  console.log(fd.keys());
  xhttp.send(fd);



  xhttp.onload = function(){
    window.location.href= '/newunit/' + id
  }

  document.getElementById('statusmsg').style.maxHeight = "50px";
  document.getElementById('statusmsg').style.borderBottom = "1px solid";

  setTimeout(function(){document.getElementById('statusmsg').style.maxHeight = "0";document.getElementById('statusmsg').style.borderBottom = "0";}, 2000);

}

document.addEventListener("keydown", function(e){
  if ((window.navigator.platform.match("Mac") ? e.metaKey : e.ctrlKey)  && e.keyCode == 83) {
     e.preventDefault();
     saveall();
     console.log("vi sparar");
}else if(e.keyCode == 115){
  e.preventDefault();
  document.getElementById('irirn').select()
}
}, false);

//document.getElementById("ircusn").addEventListener("keydown", function(e){
//  if (e.keyCode == 13) {
//     console.log("vi sparar");
//}
//}, false);
