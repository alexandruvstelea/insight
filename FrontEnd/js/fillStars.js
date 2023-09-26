function seteazaProcentaje(procente) {
  for (var i = 1; i <= 5; i++) {
    var notaElement = document.getElementById("nota" + i);
    var progressFillElement = document.getElementById("progress" + i);
    notaElement.textContent = procente[i - 1] + "%";
    progressFillElement.style.width = procente[i - 1] + "%";
  }
  
  // Calculeaza media si coloreaza stelutele in functie de medie
  var media = procente.reduce((a, b) => a + b, 0) / 5;
  coloreazaStelutele(media);
}

function coloreazaStelutele(media) {
  var starsElement = document.getElementById("media");
  if (media >= 90) {
    starsElement.textContent = "★★★★★";
  } else if (media >= 70) {
    starsElement.textContent = "★★★★☆";
  } else if (media >= 50) {
    starsElement.textContent = "★★★☆☆";
  } else if (media >= 30) {
    starsElement.textContent = "★★☆☆☆";
  } else {
    starsElement.textContent = "★☆☆☆☆";
  }
  document.getElementById("nota-medie").innerHTML += " " +media
}


seteazaProcentaje([30, 10, 30, 20, 10]); 
