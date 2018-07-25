//IGNORE THIS FOR NOW

//this will be all of our non-API js code
function submitClick() {
  console.log("CLICK CLICK CLICK")

  var loader1 = document.querySelector('#futureLoader')
  loader1.classList.add("cssload-cube")
  loader1.innerHTML = "<div class='cssload-face cssload-x'></div><div class='cssload-face cssload-y'></div><div class='cssload-face cssload-z'></div>"

  var loader2 = document.querySelector('#loadingMessage')
  loader2.style.display = "Block"

  // var text = document.querySelector('#loaderText')
  // text.style.display = "Block"
  //
  // var videoWrapper = document.querySelector('#wrapper')
  // videoWrapper.style.display = "Block"
  // var video = document.querySelector('#loaderVideo')
  // video.src = "https://www.youtube.com/embed/D-nE_HXjnZw?autoplay=1"

  var everythingElse = document.querySelector(".regular")
  everythingElse.style.display = "None"
}


window.addEventListener('load', () => {
  document.querySelector('#submit').addEventListener("click", submitClick)
});
