//IGNORE THIS FOR NOW

//this will be all of our non-API js code
function refresh() {
  window.location.reload();
}

function addFavorite() {
  alert("Schedule added to your favorites...a new schedule has been generated for you!")
  refresh()
}


window.addEventListener('load', () => {
  document.querySelector('#getAnother').addEventListener("click", refresh)
  document.querySelector('#addFavorite').addEventListener("click", addFavorite)
});
