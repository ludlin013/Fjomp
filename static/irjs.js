
var allrepact = document.getElementsByClassName('irrepact');
for (x of allrepact){
  x.style.display = "none";
}
allrepact[0].style.display = "block";


function update(inf){
  var vendor = inf.split("%")[0]
  var type = inf.split("%")[1]
  var id = inf.split("%")[2]

  console.log(0+vendor.trim());

  document.getElementById(id+'type').value = type.trim();
  document.getElementById(id+'vendor').value = vendor.trim();
}

function changerepact(idd){
  for (x of allrepact){
    x.style.display = "none";
  }
  document.getElementById(idd).style.display = "block"
}
