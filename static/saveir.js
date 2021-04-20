
function saveir(){
  var irirn = document.getElementById("irirn");
  var cid = document.getElementById("ircusn");
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

  for(x of send){
    if(x!=""){
      document.getElementById("save"+x.id).value = x.value;
    }
  }

  var xhttp = new XMLHttpRequest();

  xhttp.open("POST","/saveir",true);
  const fd = new FormData(document.getElementById('irsaveform'))
  xhttp.send(fd)
  //document.getElementById('irsaveform').submit()
}
