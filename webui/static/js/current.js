
window.onload = () => {
    console.log('DOM loaded');
    generateSeatMap();
}

const values = ['A', 'B', 'C', 'D', 'E', 'F'];

function generateSeatMap() {

    const disp = JSON.parse(disposition)

    const seatMapContainer = document.createElement('div');
    seatMapContainer.classList.add('seatmap');

    const seatsContainer = document.createElement('div');
    seatsContainer.classList.add('seats');

    for (var i = 0; i < 3; i++) {
        var row = document.createElement('div');
        row.classList.add('row');
        for (var j = 1; j <= 29; j++) {
            var seat = document.createElement('div');
            row.appendChild(seat);
            if (disp.hasOwnProperty(j + values[i])) {
                seat.textContent = disp[j + values[i]];
                seat.classList.add('taken');
            } else {
                seat.textContent = "X"
                seat.classList.add('seat');
            }
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
            row.appendChild(seat);
            seat.classList.add('seat');
            if (disp.hasOwnProperty(j + values[i])) {
                seat.textContent = disp[j + values[i]];
                seat.classList.add('taken');
            } else {
                seat.textContent = "X"
                seat.classList.add('seat');
            }
        }
        seatsContainer.appendChild(row);
    }
    seatMapContainer.appendChild(seatsContainer);
    document.body.appendChild(seatMapContainer);
}