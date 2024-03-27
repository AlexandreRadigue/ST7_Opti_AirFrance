
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded');
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
            seat.textContent = j + values[i];
            seat.addEventListener('click', submitSelectedSeat);
            row.appendChild(seat);
            if (availableSeats.includes(j + values[i])) {
                seat.classList.add('available');
            } else {
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
            seat.textContent = j + values[i];
            row.appendChild(seat);
            seat.addEventListener('click', submitSelectedSeat)
            if (availableSeats.includes(j + values[i])) {
                seat.classList.add('available');
            }
            else {
                seat.classList.add('seat');
            }
        }
        seatsContainer.appendChild(row);
    }
    seatMapContainer.appendChild(seatsContainer);
    document.body.appendChild(seatMapContainer);
}

function submitSelectedSeat(event) {
    const seat = event.target;
    console.log(seat.textContent);
    fetch('/update_seats', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ seat: seat.textContent })
    }).then(response => response.json())
        .then(data => {
            console.log(data.message);
            if (data.message === 'success') {
                window.alert('Seat selected successfully');
                window.location.href = '/';
            }
        });
}