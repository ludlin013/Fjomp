
function savedel(){
  var noteNum = document.getElementById('delivnote-number').value;
  var storeNum = document.getElementById('storeNumber').value;
  var storeName = document.getElementById('storeName').value;
  var contact = document.getElementById('contact').value;
  var date = document.getElementById('dndate').value;

  var close = document.getElementById('dnclosed').checked;
  var freight = document.getElementById('dnfreight').value;
  var sign = document.getElementById('dnsign').value;
  var notes = document.getElementById('textarea-delivnotes').value;
  var office = document.getElementById('dnoffice').value;
  var pg = document.getElementById('inputnum').value;
  var offer = document.getElementById('dnoffer').checked;
  var final = document.getElementById('dnfinal').checked;


  var fd = new FormData();

   fd.append("noteNum",noteNum);
   fd.append("storeNum",storeNum);
   fd.append("storeName",storeName);
   fd.append("contact",contact);
   fd.append("date",date);
   fd.append("close",close);
   fd.append("freight",freight);
   fd.append("sign",sign);
   fd.append("notes",notes);
   fd.append("office",office);
   fd.append("pg",pg);
   fd.append("offer",offer);
   fd.append("final",final);


  var all = document.getElementsByClassName('forminput-delivnotes3');

  console.log(all.length);
  for (x of all){
    if(x.type === "checkbox" ){
      fd.append(x.id,x.checked)
    }else{
      fd.append(x.id,x.value)
    }
  }

  var xhttp = new XMLHttpRequest();
  xhttp.open("POST","/savedeliv",true);
  xhttp.send(fd);
  alert("Delivery note saved!")
}


function priceupdate(row){
  var price = document.getElementById('price'+row).value;
  var discount = document.getElementById('dc'+row).value;

  if (discount){
    document.getElementById('net'+row).value = ((price * (100 - discount))/100).toFixed(2);
  }else{
    document.getElementById('net'+row).value = price;
  }
}

function totalupdate(row){
  var price = document.getElementById('qty'+row).value;
  var net = document.getElementById('net'+row).value;
  document.getElementById('tot'+row).value = (price * net).toFixed(2);


}

function alltotal(){
  var total = 0;

  for (var x = 0; x < document.getElementsByClassName('row-delivnotes').length; x++ ){
      total = total + parseFloat(document.getElementById('tot'+x).value)

  }

  total = parseInt(total).toFixed(2)
  document.getElementById('alltotal').value = total;

}

function setpricegroup(row){
  document.getElementById('price'+row).value = document.getElementById('pg'+row).value.split(" ")[1];
}


alltotal()

//savedel()
