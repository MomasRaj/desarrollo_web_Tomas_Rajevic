const animal1Btn = document.getElementById('animal1');
const animal2Btn = document.getElementById('animal2');
const animal3Btn = document.getElementById('animal3');
const animal4Btn = document.getElementById('animal4');
const animal5Btn = document.getElementById('animal5');

const animal1=()=>{
  window.location.href = "animal1.html";
};


const animal2=()=>{
  window.location.href = "animal2.html";
};

const animal3=()=>{
  window.location.href = "animal3.html";
};

const animal4=()=>{
  window.location.href = "animal4.html";
};

const animal5=()=>{
  window.location.href = "animal5.html";
};

animal1Btn.addEventListener('click', animal1)
animal2Btn.addEventListener('click', animal2)
animal3Btn.addEventListener('click', animal3)
animal4Btn.addEventListener('click', animal4)
animal5Btn.addEventListener('click', animal5)