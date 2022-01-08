let color = "#3AA757";

chrome.runtime.onInstalled.addListener(() => {
    chrome.storage.sync.set({ color });
    console.log(`Default background set to ${color}`);
})

function getOuterHTML() {
    return document.body.innerText;
}

// listen for event triggered by chrome plugin
chrome.runtime.onMessage.addListener(
    (request, sender, sendResponse) => {
        if (request.name === "put_doc") {
            chrome.tabs.query({
                active: true,
                windowId: chrome.windows.WINDOW_ID_CURRENT,
                lastFocusedWindow: true
            }, tabs => {
                // get url and tab id to send docs to Fern server-side
                let url = tabs[0].url;
                let id_ = tabs[0].id;
                data = chrome.scripting.executeScript({
                    target: { tabId: id_ , allFrames: true },
                    func: getOuterHTML
                }).then(function(result) {
                    const payload = JSON.stringify({
                        file_type: ".html",
                        file_name: url,
                        page_data: result[0].result
                    })
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