function httpGetParallel(urls, callback) {
    const responseBodies = Array(urls.length); // Pre-size the response array.

    let numOutstanding = 0;
    for (const [i, url] of urls.entries()) {
        numOutstanding++;
        httpGet(url, responseBody => {
            // As we get each response, save it in the appropriate array slot.
            responseBodies[i] = responseBody;
            numOutstanding--;
            // If this was the last outstanding request, we're done.
            if (numOutstanding === 0) {
                callback(responseBodies);
            }
        });
    }
}

function httpGetSerial(urls, callback) {
    const responseBodies = [];

    const startRequest = i => {
        if (i < urls.length) {
            httpGet(urls[i], responseBody => {
                responseBodies.push(responseBody);
                startRequest(i + 1);
            });
        } else {
            callback(responseBodies);
        }
    };

    startRequest(0);
}
