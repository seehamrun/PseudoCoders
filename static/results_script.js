//IGNORE THIS FOR NOW

//this will be all of our non-API js code
function refresh() {
  window.location.reload();
}


window.addEventListener('load', () => {
  document.querySelector('#getAnother').addEventListener("click", refresh)
});
