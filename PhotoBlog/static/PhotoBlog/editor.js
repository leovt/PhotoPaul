window.onload = function (){
	var txt = document.querySelectorAll("textarea");
	var i;
	var a = document.createElement('a');
	for(i=0; i<txt.length; ++i){
		(function(){
			var timeoutid;
			var form = txt[i].parentNode;
			var savebutton = form.querySelector(".text_update");
			txt[i].oninput = function(evt){
				clearTimeout(timeoutid);
				savebutton.className = "save_pending";
				timeoutid = setTimeout(function(){
					var ajaxData = new FormData(form);
					ajaxData.append('action', 'text_update_ajax');
	  				var xhr = new XMLHttpRequest();
				  	xhr.onload = function(evt){
				  		savebutton.className = "";
				  	};
				  	a.href = form.getAttribute('action');
				  	xhr.open('POST', a.href);
				  	xhr.send(ajaxData);
				}, 1500);
			};	
		})();
	}
}