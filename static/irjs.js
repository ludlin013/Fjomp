
var allrepact = document.getElementsByClassName('irrepact');
for (x of allrepact){
  x.style.display = "none";
}
allrepact[0].style.display = "flex";


function update(inf){
  var vendor = inf.split("%")[0]
  var type = inf.split("%")[1]
  var id = inf.split("%")[2]

  console.log(0+vendor.trim());

  document.getElementById(id+'type').value = type.trim();
  document.getElementById(id+'vendor').value = vendor.trim();
}

function changerepact(idd){
  console.log(idd);
  for (x of allrepact){
    x.style.display = "none";
  }
  for (x of document.getElementsByClassName(idd)){
    x.style.display = "flex"
}
  document.getElementById(idd.replace("repact","type")).parentElement.parentElement.style.borderLeft = "4px solid #fff"
  console.log(document.getElementById(idd.replace("repact","type")).parentElement.parentElement);
}

changerepact('0repact')

var active = false;

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
  id.value = date;
  window.getSelection().removeAllRanges()
}
