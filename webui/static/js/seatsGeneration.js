
document.addEventListener('DOMContentLoaded', () => {
    generateSeatMap();
});

const values = ['A', 'B', 'C', 'D', 'E', 'F'];



function generateSeatMap() {
    const seatMapContainer = document.createElement('div');
    seatMapContainer.classList.add('seatmap');

    const seatsContainer = document.createElement('div');
    seatsContainer.classList.add('seats');

    for (var i = 0; i < 3; i++) {
        var row = document.createElement('div');
        row.classList.add('row');

        for (var j = 1; j <= 29; j++) {
            var seat = document.createElement('div');
            seat.classList.add('seat');
            seat.textContent = j + values[i];
            row.appendChild(seat);
        }

        seatsContainer.appendChild(row);
    }


    var screenAisle = document.createElement('div');
    screenAisle.classList.add('screen');
    screenAisle.textContent = 'aisle';
    seatsContainer.appendChild(screenAisle);

    for (var i = 3; i < 6; i++) {
        var row = document.createElement('div');
        row.classList.add('row');

        for (var j = 1; j <= 29; j++) {
            var seat = document.createElement('div');
            seat.classList.add('seat');
            seat.textContent = j + values[i];
            row.appendChild(seat);
        }

        seatsContainer.appendChild(row);
    }


    seatMapContainer.appendChild(seatsContainer);
    //seatMapContainer.appendChild(screenAisle);


    document.body.appendChild(seatMapContainer);
}


