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
	  
	  var canvas = document.createElement("canvas");
	  var img = document.createElement("img");
	  resizeImage = function(file, callback) {
		 //document.createElement("canvas");
		/*document.body.appendChild(img);*/;
		/*document.body.appendChild(canvas);*/
	  	img.onload = function () {
		  	canvas.width = 200;
		  	canvas.height = 200;
			/*canvas.style.position = "fixed";
		  	canvas.left = -canvas.width;*/
		  	var ctx = canvas.getContext("2d");
		  	ctx.drawImage(img,0,0,canvas.width,canvas.height);
	  		canvas.toBlob(callback, "image/jpeg", 0.7);
	  	}
	  	img.src = window.URL.createObjectURL(file);
	  };
	  
	  submitFiles = function(files) {
	  	var ajaxData = new FormData(form);
	  	
	  	var send = function(){
	  		xhr.send(ajaxData);
	  	};
	  	
	  	var xhr = new XMLHttpRequest();
	  	xhr.onloadend = function(evt){location.reload(true);};
	  	xhr.open('POST', document.URL);

	  	var addfile = function(i) {
	  		if (i==files.length){
		  		xhr.send(ajaxData);
		  	}
		  	resizeImage(files[i], function(blob) {
		  		ajaxData.append('images', blob, files[i].name);
		  		addfile(i+1);
		  	});
	  	};
	  	
	  	addfile(0);
	  }
	}
}