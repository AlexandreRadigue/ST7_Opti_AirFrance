// Create a function to generate the seat map
function generateSeatMap() {
    var seatMapContainer = document.createElement('div');
    seatMapContainer.classList.add('seatmap');

    var seatsContainer = document.createElement('div');
    seatsContainer.classList.add('seats');

    // Loop to create rows
    for (var i = 0; i < 3; i++) {
        var row = document.createElement('div');
        row.classList.add('row');

        // Loop to create seats in each row
        for (var j = 1; j <= 29; j++) {
            var seat = document.createElement('div');
            seat.classList.add('seat');
            seat.textContent = (i * 29) + j;
            row.appendChild(seat);
        }

        seatsContainer.appendChild(row);
    }

    // Creating screen/aisle
    var screenAisle = document.createElement('div');
    screenAisle.classList.add('screen');
    screenAisle.textContent = 'aisle';

    // Appending everything to the seatMapContainer
    seatMapContainer.appendChild(seatsContainer);
    seatMapContainer.appendChild(screenAisle);

    // Appending the seatMapContainer to the body or any other parent element
    document.body.appendChild(seatMapContainer);
}

// Call the function to generate the seat map
generateSeatMap();
