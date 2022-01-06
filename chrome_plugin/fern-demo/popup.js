const changeColor = document.getElementById("colorChange")

chrome.storage.sync.get('color', ({ color }) => {
    changeColor.style.backgroundColor = color;
})


function sendHtml() {
    chrome.runtime.sendMessage({
        name: "put_doc",
    })
}

document.getElementById('printPage').addEventListener('click', sendHtml);