
const validateNota = (nota) => {
  if(!nota) return false;
  let rangeValid = nota >= 1 && nota <= 7;
  
  return rangeValid;
}

async function validateNota_form(aid) {
    const slider = document.getElementById('notaRange-' + aid);
    const notaValor = parseInt(slider.value);
    let notaValid = validateNota(notaValor);
    let invalidInputs = [];
    let isValid = true;
    const setInvalidInput = (inputName) => {
        invalidInputs.push(inputName);
        isValid &&= false;
    };
    if(!notaValid) {
        setInvalidInput('nota');
    }
    if (!isValid) {
        alert('Debe seleccionar una nota válida entre 1 y 7');
        return;
    }
    
    fetch(`/evaluar`, {
        method: "POST",
        body: JSON.stringify({ aviso_id: parseInt(aid), nota: notaValor }),
        credentials: "include",
        cache: "no-cache",
        headers: {
            "Content-Type": "application/json",
        },
    }).then(response => {
        if (!response.ok) {
            throw new Error("Nota no pudo ser enviada.");
        }
        location.reload();
    })
    .catch(error => {
        console.error("There has been a problem with your fetch operation:", 
            error);
    });
}

const sliders = document.querySelectorAll('.slider');

sliders.forEach(slider => {
    const avisoId = slider.getAttribute('data-aviso-id');
    const valueSpan = document.getElementById('notaValue-' + avisoId);
    
    valueSpan.textContent = slider.value;
    
    slider.addEventListener('input', function() {
        valueSpan.textContent = this.value;
    });
});

const botonesEvaluar = document.querySelectorAll('.evaluar-btn');
botonesEvaluar.forEach(boton => {
    boton.addEventListener('click', (event) => {
        event.preventDefault();
        const avisoId = boton.getAttribute('data-aviso-id');
        const slidecontainer = document.querySelector(`.slidecontainer[data-aviso-id="${avisoId}"]`);
        
        boton.style.display = 'none';
        slidecontainer.style.display = 'block';
    });
});

const botonesEnviar = document.querySelectorAll('.enviar-nota-btn');
botonesEnviar.forEach(boton => {
    boton.addEventListener('click', (event) => {
        event.preventDefault();
        const avisoId = boton.getAttribute('data-aviso-id');
        validateNota_form(avisoId);
    });
});