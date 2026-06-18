 /* This script is intended to be run in the inner context (the CAPTCHA iframe).
It recognizes the type of CAPTCHA on the page (dynamic / static tiles), then
gets the list of all the images in the iframe, and extracts the URL addresses
of needed ones. The addresses are sent to extension backend for processing.
The response is then processed by clicking the images present in the list, and
clicking the submit button. */


async function clickTiles(tilesList) {
    tilesList.forEach((index) => {
        const td = document.getElementById(index);
        td.click();
    });
    console.log(`Tiles ${tilesList} clicked succesfully`);
}


async function submitCaptcha() {
    const submitButton = document.getElementById("recaptcha-verify-button");
    submitButton.click();
    console.log("Submit button clicked successfully");
}


async function processResponse(response) {
    console.log("Response from server:", response);

    if (!("response" in response && "error" in response)) {
        console.error("Malformed response - not all fields are present!");
        return;
    }

    
    let error = [];

    if (response.response == null)
        error.push("No response field present in response JSON");
    
    if(response.error != null)
        error.push("Error in response:", response.error);

    if (error != []) {
        console.error(...error);
        return;
    }

    clickTiles(response.response);
    // demonstrate the solved CAPTCHA for a second
    setTimeout(
        submitCaptcha,
        1000,
    );
}


async function sendToServer(instructionText, url, isSpecial3x3) {
    // Helper function for sending challenge information to the extension backend
    chrome.runtime.sendMessage(
        // message body
        {
            type: "SUBMIT_PICTURE",
            instructionText: instructionText,
            picURL: url,
            isSpecial3x3: isSpecial3x3,
        },
        processResponse // callback function
    );
};


function extractImage() {
    // start execution
    console.log("Starting CAPTCHA Image Extractor...");

    // extract CAPTCHA container div and instruction text
    const descriptionsContainer = document.querySelector('div.rc-imageselect-desc, div.rc-imageselect-desc-no-canonical');
    const instructionText = descriptionsContainer
        ? descriptionsContainer.innerText.replace(/\s+/g, " ") // replace any amount of whitespaces with one space
        : "captcha_image";
    
    // extract CAPTCHA main image url
    const mainImageUrl = document.getElementsByTagName('img')[0].src;
    
    // fading tiles CAPTCHA identification
    const isSpecial3x3 = descriptionsContainer && descriptionsContainer.childNodes.length === 3;
    
    console.log(`Instruction text detected: ${instructionText}`);
    console.log(`Main challenge image found. URL: ${mainImageUrl}`);
    console.log( isSpecial3x3 ? 
        "Detected: Special 3x3 with fading tiles." : 
        "Detected: Static grid (No fading expected)."
    );
    
    sendToServer(instructionText, mainImageUrl, isSpecial3x3);
    console.log("Challenge info sent to the extension backend!");

    if (isSpecial3x3) {
        console.log("Monitoring dynamic grid for changes..."); 
        
        // A mechanism to observe changes in the src property of images
        const images = document.querySelectorAll('.rc-image-tile-wrapper img');
        
        images.forEach((img, index) => {
            let lastSrc = img.src;
            
            // Using MutationObserver in order to identify changes in src attrbute
            const observer = new MutationObserver(() => {
                if (img.src !== lastSrc) {
                    console.log(`Tile ${index} changed! Downloading new tile...`); 
                    
                    lastSrc = img.src;
                    sendToServer(instructionText, img.src, true); // this can only happen in dynamic grid
                }
            });

            observer.observe(img, { attributes: true, attributeFilter: ['src'] });
        });
    }
}

(() => {
    if (window == window.top) {
        console.log("Content script not in an iframe!");
        return; // ensures the function runs only in an iframe
    }
    if (location.pathname !== "/recaptcha/api2/bframe") {
        console.log("Script not on reCAPTCHA bframe page!");
        return; // ensures the function runs only in reCAPTCHA pages
    }

    // wait for the CAPTCHA picture to load
    // that's the case only when that CAPTCHA window is opened
    console.log("Waiting for CAPTCHA image...");
    new MutationObserver((_, obs) => {
        const images = document.getElementsByTagName("img");
        if(images.length != 0) { // if there are images detected after a change
            console.log("Image added!");
            obs.disconnect(); // The MutationObserver works only one time
            extractImage(); // TODO: (if the previous line is removed) in case of fading tiles, this MutationObserver may trigger when it shouldn't
        }
    }).observe(
        document.getRootNode(), // monitor the entire document because why not
        {   
            childList: true,
            subtree: true
        });
}) ();
