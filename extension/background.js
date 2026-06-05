async function handleSubmit(msg, sendResponse) {
  console.log("Picture submit message received.");
  try {
    // make sure the request is full
    console.assert(msg.instructionText && msg.picURL && msg.isSpecial3x3 != null, "One or more parameters absent in message JSON");
    
    // encode the picture URL so there are no symbols like &=/?: since they would break the outer URL
    const encoded_url = encodeURIComponent(msg.picURL); 
    const encoded_instructions = encodeURIComponent(msg.instructionText);

    console.log("Fetching response...");
    const response = await fetch(
      "https://127.0.0.1:5000/submit_picture" +
      `?instructionText=${encoded_instructions}` +
      `&picURL=${encoded_url}` +
      `&isSpecial3x3=${msg.isSpecial3x3}`
    );
    
    console.log("Sending response...");
    sendResponse(await response.text()); // for now, response.text() works out. Better to make a JSON response later.
  } catch(e) {
    console.error(e.toString());
    sendResponse({error: "Extension backend error!"})
  }
}

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  console.log("Received message", msg);
  if (msg.type === "SUBMIT_PICTURE")
    handleSubmit(msg, sendResponse);

  return true; // required for async response
});