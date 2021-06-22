function submitTechs(){
  for (x of document.getElementsByName('tech')){
    if (x.checked == false){
      x.value = 0
      x.checked = true
    }
  }

  for (x of document.getElementsByName('office')){
    if (x.checked == false){
      x.value = 0
      x.checked = true
    }
  }

  var xhttp = new XMLHttpRequest();
  xhttp.open("POST","/savetechs",true);
  const fd = new FormData(document.getElementById('techuserform'));
  xhttp.send(fd);
}
