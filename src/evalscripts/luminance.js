function setup() {
    return {
        input: [{
            bands: ["B02", "B03", "B04"]
        }],
        output: {
            bands: 1
        }
    };
}

function evaluatePixel(sample) {
    let luminance = 0.299 * sample.B04 + 0.587 * sample.B03 + 0.114 * sample.B02;
    return [luminance];
}
