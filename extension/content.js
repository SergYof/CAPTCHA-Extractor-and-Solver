 /* 
This script is intended to be run in the inner context (the CAPTCHA iframe).
It recognizes the type of CAPTCHA on the page (dynamic / static tiles), 
and then gets the list of all the images in the iframe, and extracts the needed ones.
*/

function extractImage() {    
    // פונקציית עזר להורדת קבצים למחשב
    const sendToServer = async (url, isSpecial3x3) => { 
        // TODO: it would be nice to trasfer the instruction text too, with the request.

        console.log(`CAPTCHA image URL: ${url}`);

        const encoded_url = encodeURIComponent(url); // encode the URL as a component so there will be no symbols like & = ?
        
        // Send request to extension backend
        chrome.runtime.sendMessage(
          // message body
          {
            type: "SUBMIT_PICTURE",
            picURL: encoded_url,
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

    // 1. חילוץ פרטי האתגר והתמונה הראשית [cite: 258-265]
    const descriptionsContainer = document.querySelector('div.rc-imageselect-desc, div.rc-imageselect-desc-no-canonical');
    const instructionText = descriptionsContainer ? descriptionsContainer.innerText.replace(/\s+/g, '_') : "captcha_image";
    
    // השגת ה-URL של תמונת האתגר הראשית (ה-Sprite) [cite: 264]
    const mainImageUrl = document.getElementsByTagName('img')[0].src;
    
    console.log("Main Challenge Image Found. Checking for the challenge type...");
    console.log(`Instruction text detected: ${instructionText}`); // TODO: send it together with the URL
    
    // 2. זיהוי האם מדובר באתגר עם תמונות מתחלפות (Fading) [cite: 268-274]
    const isSpecial3x3 = descriptionsContainer && descriptionsContainer.childNodes.length === 3;
    if (isSpecial3x3) {
        console.log("Detected: Special 3x3 with fading tiles.");
    } else {
        console.log("Detected: Static grid (No fading expected)."); 
    }
    console.log("Sending the URL to the server...");
    sendToServer(mainImageUrl, isSpecial3x3);
    

    if (isSpecial3x3) {
        console.log("Monitoring dynamic grid for changes..."); 
        // [cite: 356]
        
        // 3. מנגנון מעקב אחרי תמונות מתחלפות [cite: 388-389]
        // הקוד מאזין לשינויים ב-src של כל תגיות ה-img ב-iframe
        const images = document.querySelectorAll('.rc-image-tile-wrapper img');
        
        images.forEach((img, index) => {
            let lastSrc = img.src;
            
            // שימוש ב-MutationObserver כדי לזהות שינוי ב-Attribute של ה-src
            const observer = new MutationObserver(() => {
                if (img.src !== lastSrc) {
                    console.log(`Tile ${index} changed! Downloading new tile...`); 
                    // [cite: 372]
                    lastSrc = img.src;
                    sendToServer(img.src, true); // this can only happen in dynamic grid
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
    if (!document.URL.startsWith("https://www.google.com/recaptcha/api")) {
        console.log("Script not on reCAPTCHA page!");
        return; // ensures the function runs only in reCAPTCHA pages
    }

    // wait for the CAPTCHA picture to load
    // that's the case only when that CAPTCHA window is opened
    console.log("Waiting for CAPTCHA image...");
    new MutationObserver(() => {
        const images = document.getElementsByTagName("img");
        if(images.length != 0) {
            // if there are images detected after a change
            console.log("Image added!");
            extractImage();
        }
    }).observe(document.getRootNode(), {childList: true, subtree: true}); // monitor the entire document because why not
}) ();
