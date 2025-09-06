const validateName = (name) => {
  if(!name) return false;
  let lengthValid = name.trim().length >= 3 && name.trim().length <= 200;
  
  return lengthValid;
}

const validateContact = (contact) => {
  if(!contact) return true;
  let lengthValid = contact.trim().length >= 4 && contact.trim().length <= 50;

  return lengthValid;
}

const validateSector = (sector) => {
  if(!sector){
    return true;
  }
  if(!sector) return false;
  let lengthValid =  sector.trim().length <= 100;
  
  return lengthValid;
}

const validateEmail = (email) => {
  if (!email) return false;
  let lengthValid = email.length <= 100;

  // validamos el formato
  let re = /^[\w.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/;
  let formatValid = re.test(email);

  // devolvemos la lógica AND de las validaciones.
  return lengthValid && formatValid;
};

const validatePhoneNumber = (phoneNumber) => {
  if (!phoneNumber) return true;
  // validación de longitud
  let lengthValid = phoneNumber.length >= 8;

  // validación de formato
  let re = /^[0-9]+$/;
  let formatValid = re.test(phoneNumber);

  // devolvemos la lógica AND de las validaciones.
  return lengthValid && formatValid;
};

const validateFiles = (files) => {
  if (!files || files.length === 0) return false;

  // validación del número de archivos
  let lengthValid = 1 <= files.length && files.length <= 5;

  // validación del tipo de archivo
  let typeValid = true;

  for (const file of files) {
    // el tipo de archivo debe ser "image/<foo>" o "application/pdf"
    let fileFamily = file.type.split("/")[0];
    typeValid &&= fileFamily == "image" || file.type == "application/pdf";
  }

  // devolvemos la lógica AND de las validaciones.
  return lengthValid && typeValid;
};

const validateSelect = (select) => {
  if(!select) return false;
  return true
}

const validateType = (select) => {
  if(!select || select!="perro" && select!="gato") return false;
  return true
}

const validateUnit = (select) => {
  if(!select || select!="meses" && select!="años") return false;
  return true
}

const validateNumber = (number) => {
  if(number===undefined || number<1) return false;
  if (!Number.isInteger(Number(number))) return false;

  return true;
}
const validateDate = (date) => {
  if(date===undefined || date.trim() === "") return false;

  // Validar formato de fecha (DD-MM-AAAA)
  let re = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$/;
  return re.test(date);
}

const validateForm = () => {
  // obtener elementos del DOM usando el nombre del formulario.
  let myForm = document.forms["myForm"];
  let email = myForm["email"].value;
  let phoneNumber = myForm["numero"].value;
  let name = myForm["nombre"].value;
  let region = myForm["region"].value;
  let comuna = myForm["comuna"].value;
  let cantidad = myForm["cantidad"].value;
  let edad = myForm["edad"].value;
  let fecha = myForm["fecha"].value;
  let sector = myForm["sector"].value;
  let tipo = myForm["tipo"].value;
  let unidad = myForm["unidad"].value;
  let contacto = myForm["contacto"].value;



  // variables auxiliares de validación y función.
  let invalidInputs = [];
  let isValid = true;
  const setInvalidInput = (inputName) => {
    invalidInputs.push(inputName);
    isValid &&= false;
  };

  let fileInputs = myForm.querySelectorAll('input[name="foto[]"]');
  let files = [];
  fileInputs.forEach(input => {
    if (input.files.length > 0) {
      files.push(...input.files);
    }
  });


  // lógica de validación
  if (!validateSector(sector)) {
    setInvalidInput("Sector");
  }
  if (!validateName(name)) {
    setInvalidInput("nombre");
  }
  if (!validateEmail(email)) {
    setInvalidInput("Email");
  }
  if (!validatePhoneNumber(phoneNumber)) {
    setInvalidInput("Número");
  }
  if (!validateFiles(files)) {
    setInvalidInput("Fotos");
  }
  if (!validateSelect(region)) {
    setInvalidInput("Región");
  }
  if (!validateSelect(comuna)) {
    setInvalidInput("Comuna");
  }
  if (!validateNumber(cantidad)) {
    setInvalidInput("Cantidad de mascotas");
  }
  if (!validateNumber(edad)) {
    setInvalidInput("Edad de la mascota");
  }
  if (!validateDate(fecha)) {
    setInvalidInput("Fecha disponible para entrega");
  }
  if (!validateType(tipo)) {
    setInvalidInput("Tipo de animal");
  }
  if (!validateUnit(unidad)) {
    setInvalidInput("Unidad de edad");
  }
  if (!validateContact(contacto)) {
    setInvalidInput("Contacto");
  }


  // finalmente mostrar la validación
  let validationBox = document.getElementById("val-box");
  let validationMessageElem = document.getElementById("val-msg");
  let validationListElem = document.getElementById("val-list");
  let formContainer = document.querySelector(".main-container");

  if (!isValid) {
    validationListElem.textContent = "";
    // agregar elementos inválidos al elemento val-list.
    for (input of invalidInputs) {
      let listElement = document.createElement("li");
      listElement.innerText = input;
      validationListElem.append(listElement);
    }
    // establecer val-msg
    validationMessageElem.innerText = "Los siguientes campos son inválidos:";

    // aplicar estilos de error
    validationBox.style.backgroundColor = "#ffdddd";
    validationBox.style.borderLeftColor = "#f44336";

    // hacer visible el mensaje de validación
    validationBox.hidden = false;
  } else {
    // Ocultar el formulario
    myForm.style.display = "none";

    // establecer mensaje de éxito
    validationMessageElem.innerText = "¿Está seguro que desea agregar este aviso de adopción?";
    validationListElem.textContent = "";

    // aplicar estilos de éxito
    validationBox.style.backgroundColor = "#ddffdd";
    validationBox.style.borderLeftColor = "#4CAF50";

    // Agregar botones para enviar el formulario o volver
    let submitButton = document.createElement("button");
    submitButton.innerText = "Sí, estoy seguro";
    submitButton.style.marginRight = "10px";
    submitButton.addEventListener("click", () => {
      validationMessageElem.innerText = "Hemos recibido la información de adopción, muchas gracias y suerte!";
      validationListElem.innerHTML = "";
      let BtnVolver = document.createElement("button");
      BtnVolver.innerText = "Volver a la portada";
      BtnVolver.addEventListener("click", () => {
        window.location.href = "../portada/index.html";
      });
      validationListElem.appendChild(BtnVolver);
    });

    let backButton = document.createElement("button");
    backButton.innerText = "No, no estoy seguro, quiero volver al formulario";
    backButton.addEventListener("click", () => {
      // Mostrar el formulario nuevamente
      myForm.style.display = "block";
      validationBox.hidden = true;
    });

    validationListElem.appendChild(submitButton);
    validationListElem.appendChild(backButton);

    // hacer visible el mensaje de validación
    validationBox.hidden = false;
  }

};


let submitBtn = document.getElementById("submit-btn").addEventListener("click", (event) => {
  event.preventDefault(); 
  validateForm();        
});