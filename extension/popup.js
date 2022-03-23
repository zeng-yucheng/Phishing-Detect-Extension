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
		var rsp = req.responseText.replace(/'/g, '"');
		var j = JSON.parse(rsp);
		$("#tres").text(j.result);
		$("#tprob").text(j.probability);
		return req.responseText;
	});
}


$(document).ready(function(){
    $("button").click(function(){	
		var val = func();
    });
});
