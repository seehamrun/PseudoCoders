//IGNORE THIS FOR NOW

//this will be all of our non-API js code
function submitClick() {
  var loader = document.querySelector('#futureLoader')
  loader.classList.add("loader")
}

window.addEventListener('load', () => {
  document.querySelector('#submit').addEventListener("click", submitClick)
});
