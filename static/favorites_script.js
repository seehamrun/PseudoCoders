//IGNORE THIS FOR NOW

//this will be all of our non-API js code
function refresh() {
  window.location.reload();
}

// function addFavorite() {
//   window.alert("Schedule added to your favorites...a new schedule has been generated for you!")
//   refresh()
// }

function deleteCall() {
  var result = confirm("Want to delete?");
  if (result) {
    console.log("CALL TO DELETE")
}
}


window.addEventListener('load', () => {
  document.querySelector('#seeNext').addEventListener("click", refresh)
  document.querySelector('#delete').addEventListener("click", deleteCall)
  //document.querySelector('#addFavorite').addEventListener("click", addFavorite)
});
