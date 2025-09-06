const selectContactar = document.getElementById("contactar");
const divContacto = document.getElementById("contactoo");

selectContactar.addEventListener("change", () => {
    if (selectContactar.value != "seleccionar") {
        divContacto.style.display = "block";                  
    } else {
        divContacto.style.display = "none";                   
    }
});
