//true colors

function setup() {
    return {
        input: [{
            bands: ["B08", "B04"]
        }],
        output: {
            bands: 3
        }
    };
}

function evaluatePixel(sample) {
    return [sample.B08, sample.B04, 0];
}