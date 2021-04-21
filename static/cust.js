function setmodel(inf){
  var cat = inf.split("%")[0]
  var type = inf.split("%")[1]
  var vendor = inf.split("%")[2]
  var id = inf.split("%")[3]

  console.log(cat);
  console.log(type);
  console.log(vendor);


  document.getElementById(id+'type').value = type.trim();
  document.getElementById(id+'vendor').value = vendor.trim();
  document.getElementById(id+'cat').value = cat.trim();
}
