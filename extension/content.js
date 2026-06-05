 /* 
This script is intended to be run in the inner context (the CAPTCHA iframe).
It recognizes the type of CAPTCHA on the page (dynamic / static tiles), 
and then gets the list of all the images in the iframe, and extracts the needed ones.
*/

function extractImage() {    
    // פונקציית עזר להורדת קבצים למחשב
    const sendToServer = async (instructionText, url, isSpecial3x3) => { 
        console.log(`CAPTCHA image URL: ${url}`);

        // Send request to extension backend
        chrome.runtime.sendMessage(
          // message body
          {
            type: "SUBMIT_PICTURE",
            instructionText: instructionText,
            picURL: JSON.stringify(url), // escape any character that needs escaping
            isSpecial3x3: isSpecial3x3,
          },
          // callback
          (response) => {
            console.log("Server says:", response);
          }
        );
        console.log("URL sent to the extension backend!");
    };

    // start execution
    console.log("Starting CAPTCHA Image Extractor...");

    // extract CAPTCHA container div and instruction text
    const descriptionsContainer = document.querySelector('div.rc-imageselect-desc, div.rc-imageselect-desc-no-canonical');
    const instructionText = descriptionsContainer ? descriptionsContainer.innerText.replace(/\s+/g, '_') : "captcha_image";
    
    // extract CAPTCHA main image url 
    const mainImageUrl = document.getElementsByTagName('img')[0].src;
    
    console.log("Main Challenge Image Found. Checking for the challenge type...");
    console.log(`Instruction text detected: ${instructionText}`); // TODO: send it together with the URL
    
    // fading tiles CAPTCHA identification
    const isSpecial3x3 = descriptionsContainer && descriptionsContainer.childNodes.length === 3;

    console.log( isSpecial3x3 ? 
        "Detected: Special 3x3 with fading tiles." : 
        "Detected: Static grid (No fading expected)."
    );
    
    console.log("Sending the main image URL to the server...");
    sendToServer(instructionText, mainImageUrl, isSpecial3x3);

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
    }).observe(document.getRootNode(), {childList: true, subtree: true}); // monitor the entire document because why not
}) ();
