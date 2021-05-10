
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


  console.log(noteNum);
  console.log(storeNum);
  console.log(storeName);
  console.log(contact);
  console.log(date);
  console.log(close);
  console.log(freight);
  console.log(sign);
  console.log(notes);
  console.log(office);
  console.log(pg);
  console.log(offer);
  console.log(final);
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
  document.getElementById('price'+row).value = document.getElementById('pg'+row).value;
}


alltotal()

//savedel()
