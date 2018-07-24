//IGNORE THIS FOR NOW

//this will be all of our non-API js code
function submitClick() {
  var loader1 = document.querySelector('#futureLoader')
  //loader1.classList.add("loader")
  loader1.classList.add("cssload-cube")
  loader1.innerHTML = "<div class='cssload-face cssload-x'></div><div class='cssload-face cssload-y'></div><div class='cssload-face cssload-z'></div>"

  var everythingElse = document.querySelector(".regular")
  everythingElse.style.display = "None"

  var loader2 = document.querySelector('#loadingMessage')
  loader2.innerHTML = "Your results are loading...!"
}


window.addEventListener('load', () => {
  document.querySelector('#submit').addEventListener("click", submitClick)
});
