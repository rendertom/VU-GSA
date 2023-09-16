const btnSubmit = document.getElementById("btnSubmit");
btnSubmit.onclick = function () {
  const fileSelector = document.getElementById('fileSelector');
  console.log(fileSelector.files)
  
  var path = (window.URL || window.webkitURL).createObjectURL(fileSelector.files[0]);
  console.log('path', path);

  console.log(fileSelector.files)

  const filePath = fileSelector.value;
  console.log(filePath)
  // alertPath(filePath);
}

function alertPath(path) {
  alert(path)
}