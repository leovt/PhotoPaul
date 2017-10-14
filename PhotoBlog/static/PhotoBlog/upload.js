var isAdvancedUpload = function() {
  var div = document.createElement('div');
  return (('draggable' in div) || ('ondragstart' in div && 'ondrop' in div)) && 'FormData' in window && 'FileReader' in window;
}();

console.log("isAdvancedUpload:", isAdvancedUpload)

window.onload = function ()
{
	var form = document.getElementById("ulform");
	if (isAdvancedUpload) {
	  form.className = 'ulform has-advanced-upload';
	  
	  form.ondragover = form.ondragenter = function(e) {
	  	e.preventDefault();
    	e.stopPropagation();
	  	form.className = 'ulform has-advanced-upload isdragover';
	  }
	  
	  form.ondragleave = form.ondragend = function(e) {
	  	e.preventDefault();
    	e.stopPropagation();
	  	form.className = 'ulform has-advanced-upload';
	  }
	  
	  form.ondrag = form.ondragstart = function (e) {
	  	e.preventDefault();
    	e.stopPropagation();
	  }
	  
	  form.ondrop = function (e) {
	  	e.preventDefault();
    	e.stopPropagation();
	  	form.className = 'ulform has-advanced-upload';
	  	droppedFiles = e.dataTransfer.files;
	  	console.log("droppedFiles:", droppedFiles);
	  	submitFiles(droppedFiles);
	  }
	  
	  submitFiles = function(files) {
	  	var ajaxData = new FormData(form);
	  	
	  	for (i=0; i<files.length; ++i){
	  		ajaxData.append('images', files[i], files[i].name);
	  	}
	  	var xhr = new XMLHttpRequest();
	  	xhr.onloadend = function(evt){location.reload(true);};
	  	xhr.open('POST', document.URL);
	  	xhr.send(ajaxData);
	  }
	}
}