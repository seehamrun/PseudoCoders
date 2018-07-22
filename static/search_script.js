// contacts our server, and asks it to add gifUrl to the list of favorite GIFs.
// doneCallback should be a function, which addGifToFavorites will invoke when
// the gifUrl is saved successfully.
function addToFavorites(scheduleID, doneCallback) {
  jQuery.post("/favorites", {ID: scheduleID}, doneCallback);
}

function submitClick() {
  //var inputBox = document.querySelector('#queryBox')
  //var userInput = inputBox.value
  //queryGiphy(userInput, displayResult)
  console.log("SUBMIT CLICKED")
}

function addFavoriteClick() {
  addToFavorites(currentGifUrl, () => {
    alert("saved!")
  })
}

window.addEventListener('load', () => {
  document.querySelector('#submit').addEventListener("click", submitClick)
  //document.querySelector('#addFavorite').addEventListener('click', addFavoriteClick)
});
