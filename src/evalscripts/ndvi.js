function setup() {
    return {
        input: [{
            bands: ["B08", "B04"]
        }],
        output: {
            bands: 1
        }
    };
}

function evaluatePixel(sample) {
    let v = (sample.B08 - sample.B04) / (sample.B08 + sample.B04);
    return [v];
}