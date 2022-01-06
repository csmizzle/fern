let color = "#3AA757";

chrome.runtime.onInstalled.addListener(() => {
    chrome.storage.sync.set({ color });
    console.log(`Default background set to ${color}`);
})

function getOuterHTML() {
    console.log('Getting outer HTML ...')
    const data = document.body.innerText;
    console.log(data);
    return data
}

chrome.runtime.onMessage.addListener(
    (request, sender, sendResponse) => {
        if (request.name === "put_doc") {
            chrome.tabs.query({
                active: true,
                windowId: chrome.windows.WINDOW_ID_CURRENT,
                lastFocusedWindow: true
            }, tabs => {
                let url = tabs[0].url;
                let id_ = tabs[0].id;
                console.log('ID', id_)
                data = chrome.scripting.executeScript({
                    target: { tabId: id_ , allFrames: true },
                    func: getOuterHTML
                }).then(function(result) {
                    console.log(url);
                    const payload = JSON.stringify({
                        file_type: ".html",
                        file_name: url,
                        page_data: result[0].result
                    })
                    console.log(payload);
                    fetch('http://localhost:1337/doc_raw', {
                        method: "PUT",
                        body: JSON.stringify(payload),
                        headers: {
                            'Content-Type': 'application/json',
                        }
                    }).then((resp) => {
                        console.log(resp);
                    }).catch((error) => {
                        console.log(error);
                    });
                });
            })
        }
    });