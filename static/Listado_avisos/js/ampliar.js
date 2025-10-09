function ampliar(img) {
  let overlay = document.getElementById("overlay");
  let overlayImg = overlay.querySelector("img");
  overlayImg.src = img.src;
  overlay.style.display = "flex";
}
function cerrar() {
  document.getElementById("overlay").style.display = "none";
}