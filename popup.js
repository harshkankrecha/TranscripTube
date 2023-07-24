const btn = document.getElementById("summarize");
btn.addEventListener("click", function() {
    btn.disabled = true;
    btn.innerHTML = "Loading...";
    chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
        var url = tabs[0].url;
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "http://127.0.0.1:5000/summarize?url=" + url, true);
        xhr.onload = function() {
            var textresponse = xhr.responseText;
            const p = document.getElementById("result");
            p.innerHTML = textresponse;
            btn.disabled = false;
            btn.innerHTML = "Summarize";
        }
        xhr.send();
    });
});