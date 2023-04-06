//true colors

function setup() {
    return {
        input: [{
            bands: ["B02", "B03", "B04"]
        }],
        output: {
            bands: 3
        }
    };
}

function evaluatePixel(sample) {
    return [2.5*sample.B04, 2.5*sample.B03, 2.5*sample.B02];
}