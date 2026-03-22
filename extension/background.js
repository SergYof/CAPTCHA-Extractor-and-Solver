chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  console.log("Received message", msg);
  if (msg.type != "PING_SERVER") {
    console.log("Message type mismatch!")
    return true;
  }
  
  fetch("https://127.0.0.1:5000/scripts/test.js")
    .then(r => {
      console.log("Fetch response", r);
      return r.json();
    })
    .then(data => {
      console.log("Data", data);
      sendResponse(data);
    })
    .catch(err => {
      console.error("Fetch failed", err);
      sendResponse({ error: err.toString() });
    });

  return true; // required for async response
});