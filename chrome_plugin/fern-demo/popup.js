const changeColor = document.getElementById("colorChange")

chrome.storage.sync.get('color', ({ color }) => {
    changeColor.style.backgroundColor = color;
})


function sendHtml() {
    chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
        let url =  tabs[0].url;
        const pageHtml = document.body.innerHTML;
        const payload = JSON.stringify({
            file_type: ".html",
            doc_raw: pageHtml,
            file_name: url,
        })
        alert(payload)
        fetch('http://localhost:1337/doc_raw', {
            method: "PUT",
            body: JSON.stringify(payload),
            credentials: 'same-origin',
            headers: {
                'Accept': 'application/json',
            }
        }).then((resp) => {
            console.log(resp);
        }).catch((error) => {
            console.log(error);
        });
    })
}

document.getElementById('printPage').addEventListener('click', sendHtml);