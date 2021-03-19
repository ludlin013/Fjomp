
function update(inf){
  var vendor = inf.split("%")[0]
  var type = inf.split("%")[1]
  var id = inf.split("%")[2]

  document.getElementById(id+'type').value = type;
  document.getElementById(id+'vendor').value = vendor;
}
