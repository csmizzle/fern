const changeColor = document.getElementById("colorChange")

chrome.storage.sync.get('color', ({ color }) => {
    changeColor.style.backgroundColor = color;
})