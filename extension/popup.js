function func(){	
	var url;
	chrome.tabs.getSelected(null,function(tab) {
	   	url = tab.url;
		var req = new XMLHttpRequest();
		var content = "url="+url;
		req.open("POST","http://127.0.0.1/clientServer.php", false);
		req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
		req.send(content);
		// alert(req.responseText);
		$("#div1").text(req.responseText);
		return req.responseText;
	});
}


$(document).ready(function(){
    $("button").click(function(){	
		var val = func();
    });
});
