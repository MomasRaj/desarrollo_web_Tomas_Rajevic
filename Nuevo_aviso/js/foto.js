const maxFotos = 5;
const container = document.getElementById('fotos-container');
const btnFoto = document.getElementById('agregar-foto');
let contadorFotos = 1; 
const foto = () => {
  const numFotos = container.querySelectorAll('.foto-item').length;
  if (numFotos < maxFotos) {
    contadorFotos++;
    
    const div = document.createElement('div');
    div.className = 'foto-item';
   
    const label = document.createElement('label');
    label.setAttribute('for', 'foto' + contadorFotos);
    label.textContent = 'Foto';
    
    const input = document.createElement('input');
    input.type = 'file';
    input.name = 'foto[]';
    input.id = 'foto' + contadorFotos;
    input.accept = 'image/*';
    input.required = true;
    
    div.appendChild(label);
    div.appendChild(input);
   
    container.appendChild(div);
  } 
};

btnFoto.addEventListener('click', foto)