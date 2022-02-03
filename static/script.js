// Creates a function that, upon click, changes the color of the element with the id "one_header" to red
document.addEventListener("click", myFunction);

function myFunction() {
  document.getElementById("one_header").style.color = "red";
  document.getElementById("demo").innerHTML = "Brandon's gay";
}
