
var x = true

function hamburger(){
  var menu = document.getElementsByClassName('navin')[0]
  var top = document.getElementById('hamtop')
  var mid = document.getElementById('hammid')
  var bot = document.getElementById('hambot')
  var dim = document.getElementById('menudim')

  if(x){
    menu.style.maxWidth = "60vw";
    top.style.transform = "rotate(45deg)"
    top.style.top = "14px";
    top.style.left = "19px";
    mid.style.maxWidth = "0";
    bot.style.transform = "rotate(-45deg)"
    bot.style.top = "42px";
    bot.style.left = "19px";

    dim.style.display = "block";
    document.body.style.overflow = "hidden"
    setTimeout(function(){
      dim.style.opacity = ".5";
    },50);

    x = false
  }else{
    menu.style.maxWidth = "0";
    top.style.transform = "rotate(0)"
    top.style.top = "16px";
    top.style.left = "15px";
    mid.style.maxWidth = "40px";
    bot.style.transform = "rotate(0)"
    bot.style.top = "40px";
    bot.style.left = "15px";
    document.body.style.overflow = "auto"

    dim.style.opacity = "0";
    setTimeout(function(){
      dim.style.display = "none";
    },100);

    x = true
  }
}

document.getElementById('userstatuscolor').onclick = function(){

  const fd = new FormData();
  var xhttp = new XMLHttpRequest();

  xhttp.onload = function(){
    document.getElementById('userstatuscolor').style.background = xhttp.responseText;
  }

  xhttp.open("POST","/changestatus",true);
  xhttp.send(fd);

}
