log();
setInterval(log, 1000);

function log(){
  if(!document.cookie.includes("loggedin=True")){
    location.reload();
  }
}
