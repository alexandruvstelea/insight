window.onload = function () {
  var userAgent = navigator.userAgent || navigator.vendor || window.opera;
  if (
    /android/i.test(userAgent) ||
    (/iPad|iPhone|iPod/.test(userAgent) && !window.MSStream)
  ) {
    console.log("Dispozitivul este Android sau iOS.");
  } else {
    window.location.href = "https://www.example.com";
  }
};
