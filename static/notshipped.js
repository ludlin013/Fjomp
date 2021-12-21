
function previewpart(nr){
  for(var x of document.getElementsByClassName("itempreview")){
    x.style.display = "none";
  }

  document.getElementById(nr).style.display = "flex";

}


function getpart(nr){
  var fd = new FormData();

  fd.append("nr",nr)

  var xhttp = new XMLHttpRequest();

  xhttp.onload = function(){

    for(var x of document.getElementsByClassName("nsitem")){
      x.style.background = "rgb(140,140,140)";
    }

    document.getElementsByClassName(nr)[0].style.background = "rgb(160,160,160)";

    document.cookie = "notshippednr = " + nr;

    document.getElementsByClassName('previewwrap')[0].innerHTML = "";

    var content = JSON.parse(xhttp.responseText);
    var itemspreview = document.createElement("div");
    itemspreview.classList.add("itempreview");
    itemspreview.id = nr;

    document.getElementsByClassName('previewwrap')[0].appendChild(itemspreview);

    var label = document.createElement("label");
    label.classList.add("preref");

    var ref = document.createTextNode("Reference: " + content["ref"])
    label.appendChild(ref);
    itemspreview.appendChild(label);

    if (content["notes"] != ""){

      var text = document.createElement("textarea");
      text.classList.add("pretex");
      text.cols = "80";

      var textanode = document.createTextNode(content["notes"]);

      var lines = content["notes"].split("\n").length;
      text.rows = lines+1;

      text.appendChild(textanode);
      itemspreview.appendChild(text);
    }


    var preelem = document.createElement("div");
    preelem.classList.add("previewpart");
    itemspreview.appendChild(preelem);

    var pnr = document.createElement("p");
    pnr.appendChild(document.createTextNode("Part nr."));
    pnr.classList.add("prepno");
    var pna = document.createElement("p");
    pna.appendChild(document.createTextNode("Part name"));
    pna.classList.add("prepna");
    var pqt = document.createElement("p");
    pqt.appendChild(document.createTextNode("Quantity"));
    pqt.classList.add("preqty");
    var pbo = document.createElement("p");
    pbo.appendChild(document.createTextNode("Back order"));
    pbo.classList.add("prepbo");


    preelem.appendChild(pnr);
    preelem.appendChild(pna);
    preelem.appendChild(pqt);
    preelem.appendChild(pbo);

    for(var x of content["parts"]){
      if(x != null){
        console.log(x[2],x[3]);

        var preelem = document.createElement("div");
        preelem.classList.add("previewpart");
        itemspreview.appendChild(preelem);

        var pnr = document.createElement("p");
        pnr.appendChild(document.createTextNode(x[0]));
        pnr.classList.add("prepno");
        var pna = document.createElement("p");
        pna.appendChild(document.createTextNode(x[1]));
        pna.classList.add("prepna");
        var pqt = document.createElement("p");
        pqt.appendChild(document.createTextNode(x[2]));
        pqt.classList.add("preqty");
        var pbo = document.createElement("p");
        pbo.classList.add("prepbo");
        var pbcheck = document.createElement("input");
        pbcheck.type = "checkbox";
        if(x[3] == "1"){
          pbcheck.checked = true;
        }
        pbo.appendChild(pbcheck);


        preelem.appendChild(pnr);
        preelem.appendChild(pna);
        preelem.appendChild(pqt);
        preelem.appendChild(pbo);


      }
    }
  }


  xhttp.open("POST","/getnspart",true);
  xhttp.send(fd);
}

if(document.cookie.includes("notshippednr")){
  for ( var x of document.cookie.split(";")){
    if(x.includes("notshippednr")){
      getpart(x.replace("notshippednr=",""))
    }
  }
}

function showbo(id) {
  for(var x of document.getElementsByClassName("boelements")){
    x.style.display = "none";
  }

  for(var x of document.getElementsByClassName(id)){
    x.style.display = "flex";
  }

}
