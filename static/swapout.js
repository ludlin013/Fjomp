document.getElementById('opensw').addEventListener("keydown", function (e) {
  if (e.keyCode == 13) {
    window.location.href = '/swapouts?sw=' + document.getElementById('opensw').value
  }
}, false);

function swapsave() {

  var xhttp = new XMLHttpRequest();
  const fd = new FormData(document.getElementById('allform'))
  xhttp.open("POST", "/swapsave", true);
  xhttp.send(fd);

  //alert("Swapout saved")

  document.getElementById('statusmsg').style.maxHeight = "50px";
  document.getElementById('statusmsg').style.borderBottom = "1px solid";

  setTimeout(function () { document.getElementById('statusmsg').style.maxHeight = "0"; document.getElementById('statusmsg').style.borderBottom = "0"; }, 2000);

}
