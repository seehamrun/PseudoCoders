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
    $.get("/deleteCurrentItemFromFavoritesList", refresh)
}
}


function postGallery() {
  $.post("/post")
}


window.addEventListener('load', () => {
  document.querySelector('#seeNext').addEventListener("click", refresh)
  document.querySelector('#deleteFav').addEventListener("click", deleteCall)
  document.querySelector('#postGallery').addEventListener("click", postGallery)

});
