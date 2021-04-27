// 1. 'httpGet' is provided for you.
// 2. You have to implement 'httpGetParallel' and 'httpGetSerial'
//    using 'httpGet'.  See signatures below.
// 3. 'testAsync' will try running your 'httpGetParallel' and
//    'httpGetSerial' with some test URLs.  The expected output
//    is shown at the very bottom of this file.
//
// You can run this on your computer with Node.js or use an online Node.js
// environment, e.g. https://www.anyfiddle.com/templates/nodejs/

// A callback-style function to make an HTTP GET request.
// When the request is complete, 'callback' will be called with
// the response body text.  For simplicity, we're ignoring errors.
//
// Example usage:
//     httpGet('https://example.org/', responseBody => {
//         console.log(`Got first page: ${JSON.stringify(responseBody)}`);
//     
//         const targetUrl = extractFirstLink(responseBody);
//         if (targetUrl !== null) {
//             httpGet(targetUrl, responseBody => {
//                 console.log(`Got second page: ${JSON.stringify(responseBody)}`);
//             });
//         }
//     });
function httpGet(url, callback) {
    log(`GET ${JSON.stringify(url)}...`);
    const https = require('https');
    https.get(url, res => {
        const responseChunks = [];
        res.on('data', chunk => {
            responseChunks.push(chunk);
        });
        res.on('end', () => {
            const responseText = Buffer.concat(responseChunks).toString('utf8');
            callback(responseText);
        });
    }).on('error', err => {
        throw err;
    });
}

// This function should initiate parallel HTTP GET requests for all URLs in
// the 'urls' array.  After all requests are complete, call 'callback' with
// an array of response bodies, matching the order of the `urls` array.
function httpGetParallel(urls, callback) {
    // You have to write this code.
    // You can use 'httpGet', but don't use promises.
    throw new Error('unimplemented');
}

// This function should make HTTP GET requests for the URLs in the 'urls'
// array one at a time.  After the last request is complete, call 'callback'
// with an array of response bodies, matching the order of the `urls` array.
function httpGetSerial(urls, callback) {
    // You have to write this code.
    // You can use 'httpGet', but don't use promises.
    throw new Error('unimplemented');
}

function log(message) {
    const now = new Date();
    const dateTime = new Date(now.getTime() - (now.getTimezoneOffset() * 60000)).toISOString();
    const time = dateTime.substring(11, 21); // Just the time, with 1/10th of a second precision
    console.log(`[${time}] ${message}`);
}

async function testAsync() {
    // httpbin.org provides several convenient test endpoints.  We're using
    // httpbin.org/delay/N, which just waits N seconds before responding.
    const urls = [
        'https://httpbin.org/delay/1',
        'https://httpbin.org/delay/2',
        'https://httpbin.org/delay/1',
    ];

    log('Trying httpGetParallel...');
    await new Promise(resolve => {
        httpGetParallel(urls, responseBodies => {
            const truncated = responseBodies.map(s => s.substring(0, 20));
            log(`Got responses: ${JSON.stringify(truncated, null, 4)}`);
            resolve();
        });
    });

    log('Trying httpGetSerial...');
    await new Promise(resolve => {
        httpGetSerial(urls, responseBodies => {
            const truncated = responseBodies.map(s => s.substring(0, 20));
            log(`Got responses: ${JSON.stringify(truncated, null, 4)}`);
            resolve();
        });
    });
}

testAsync().catch(console.error);

/*
Expected output:

    [20:07:12.4] Trying httpGetParallel...
    [20:07:12.4] GET "https://httpbin.org/delay/1"...
    [20:07:12.4] GET "https://httpbin.org/delay/2"...
    [20:07:12.4] GET "https://httpbin.org/delay/1"...
    [20:07:14.8] Got responses: [
        "{\n  \"args\": {}, \n  \"",
        "{\n  \"args\": {}, \n  \"",
        "{\n  \"args\": {}, \n  \""
    ]
    [20:07:14.8] Trying httpGetSerial...
    [20:07:14.8] GET "https://httpbin.org/delay/1"...
    [20:07:15.9] GET "https://httpbin.org/delay/2"...
    [20:07:18.0] GET "https://httpbin.org/delay/1"...
    [20:07:19.1] Got responses: [
        "{\n  \"args\": {}, \n  \"",
        "{\n  \"args\": {}, \n  \"",
        "{\n  \"args\": {}, \n  \""
    ]

(Your timestamps might be different.)
*/
