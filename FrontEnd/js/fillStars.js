function setPercentages(percentages) {
  for (let i = 1; i <= percentages.length; i++) {
    let notaElement = document.getElementById("nota" + i);
    let progressFillElement = document.getElementById("progress" + i);
    notaElement.textContent = percentages[i - 1].toFixed(0) + "%";
    progressFillElement.style.width = percentages[i - 1].toFixed(0) + "%";
  }

}

function coloreazaStelutele(media) {
  let starsElement = document.getElementById("media");
  if (media >= 4.5 && media <= 5) {
    starsElement.innerHTML = "&#9733;&#9733;&#9733;&#9733;&#9734;";
  } else if (media >= 2.5 && media < 3.5) {
    starsElement.innerHTML = `&#9733;&#9733;&#9733;&#9734;&#9734;`;
  } else if (media >= 1.5 && media < 2.5) {
    starsElement.innerHTML = "&#9733;&#9733;&#9734;&#9734;&#9734;";
  } else if (media > 0 && media < 1.5) {
    starsElement.innerHTML = "&#9733;&#9734;&#9734;&#9734;&#9734;";
  } else if (media == 0) {
    starsElement.innerHTML = "&#9733;&#9734;&#9734;&#9734;&#9734;";
  }
  document.getElementById("nota-medie").innerHTML = ` ${media}`;
}



