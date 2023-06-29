// visualization.js

// Function to create a bar graph for player attributes
function createPlayerAttributesGraph(playerAttributes) {
    var playerFeatures = {{ player_features|tojson }};
    
    // Convert the player attributes from strings to numbers
    var attributes = playerAttributes.map(parseFloat);
    
    // Create the bar graph
    Plotly.newPlot('player_attributes_graph', [{
        x: playerFeatures,
        y: attributes,
        type: 'bar',
        marker: { color: 'pink' }
    }], {
        title: 'Player Attributes',
        xaxis: { title: 'Attribute' },
        yaxis: { title: 'Value' }
    });
}

// Function to create a bar graph for the predicted overall rating
function createOverallRatingGraph(prediction) {
    Plotly.newPlot('overall_rating_graph', [{
        x: ['Predicted Overall Rating'],
        y: [prediction],
        type: 'bar',
        marker: { color: 'green' }
    }], {
        title: 'Predicted Overall Rating',
        xaxis: { title: 'Attribute' },
        yaxis: { title: 'Value' }
    });
}
