function setup() {
    return {
        input: [{
            bands: ["B11", "B08", "B04"]
        }],
        output: {
            bands: 1
        }
    };
}

function evaluatePixel(sample) {
    var luminance = ((sample.B11 - sample.B08) / (sample.B11 + sample.B08))
    return [luminance];
}