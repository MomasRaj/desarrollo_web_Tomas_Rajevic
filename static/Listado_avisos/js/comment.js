
const validateName = (name) => {
  if(!name) return false;
  let lengthValid = name.trim().length >= 3 && name.trim().length <= 80;
  
  return lengthValid;
}

const validateComment = (comment) => {
  if(!comment) return false;
  let lengthValid = comment.trim().length >= 5;
  return lengthValid;
}

async function loadComments(aid) {
    try {
    const url=`/aviso/${aid}/comentarios`;
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error("Network response was not ok"); 
    }
    return await response.json();
    } catch(error){
    console.error("There has been a problem with your fetch operation:",
        error);
    } 
}

async function validateComment_form(aid) {
    const name = document.getElementById('nombre').value;
    const comment = document.getElementById('comentario_box').value;
    let nameValid = validateName(name);
    let commentValid = validateComment(comment);
      let invalidInputs = [];
  let isValid = true;
  const setInvalidInput = (inputName) => {
    invalidInputs.push(inputName);
    isValid &&= false;
  };
    if(!nameValid) {
        setInvalidInput('nombre');
    }
    if(!commentValid) {
        setInvalidInput('comentario_box');
    }
    if (!isValid) {
    validationListElem.textContent = "";
    for (input of invalidInputs) {
      let listElement = document.createElement("li");
      listElement.innerText = input;
      validationListElem.append(listElement);
    }

    validationMessageElem.innerText = "Los siguientes campos son inválidos:";

    validationBox.style.backgroundColor = "#ffdddd";
    validationBox.style.borderLeftColor = "#f44336";


    validationBox.hidden = false;
  } else {

    validationBox.hidden = true;
  }
    fetch(`/aviso/${aid}/comentarios`, {
    method: "POST",
    body: JSON.stringify({ nombre: name, comentario_box: comment }),
    credentials: "include",
    cache: "no-cache",
    headers: {
     "Content-Type": "application/json",
    },
  }).then(response => {
        if (!response.ok) {
            throw new Error("Comentario no pudo ser enviado.");
        }

        location.reload();
    })
    .catch(error => {
        console.error("There has been a problem with your fetch operation:", 
          error);
    });
}

