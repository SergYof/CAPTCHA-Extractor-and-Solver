/* This is the background script of the extension. It runs in the backend of the extension and exchanges
information with content script (content.js) which runs in the context of a loaded web page. 
The information is transferred via Chrome runtime, which includes functions such as 
onMessage.addListener() for listening, and sendResponse() callback.

This script accepts a message with the CAPTCHA challenge data, and queries a local API (Flask),
bypassing PNA (Private Network Access) restrictions. */


async function handleSubmit(msg, sendResponse) {
  console.log("Picture submit message received.");
  try {

    // make sure the request is full before proceeding
    if (!(msg.instructionText && msg.picURL && msg.isSpecial3x3 != null))
      throw new Error(
        "One or more parameters absent in message JSON.",
        {
          cause: {
            response: null,
            error: "Malformed request: one or more of the fields is absent.",
          },
        }
      );


    // encode the picture URL so there are no symbols like &=/?: since they would break the outer URL
    // instruction text should be encoded too, because spaces break the URL as well
    const encoded_url = encodeURIComponent(msg.picURL); 
    const encoded_instructions = encodeURIComponent(msg.instructionText);

    console.log("Fetching response from local API...");
    const response = await fetch(
      "https://127.0.0.1:5000/submit_picture" +
      `?instructionText=${encoded_instructions}` +
      `&picURL=${encoded_url}` +
      `&isSpecial3x3=${msg.isSpecial3x3}`
    );

    // make sure the fetch is successful (200-299 status codes)
    if (!response.ok)
      throw new Error(
        "HTTP Error",
        {
          cause: await response.json(),
        }
      );


    console.log("Sending response to the content script...");
    sendResponse(await response.json());
    console.log("Response successfuly sent to the content script.")

  } catch(e) {
    console.error(e.toString());
    sendResponse(e.cause);  // response is sent anyway
  }
}


chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  console.log("Received message", msg);
  if (msg.type === "SUBMIT_PICTURE")
    handleSubmit(msg, sendResponse);

  return true; // required for async response
});