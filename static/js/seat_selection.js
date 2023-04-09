const container = document.querySelector('.container');
const num_of_seats_selected = document.getElementById('num_of_seats_selected');
const seats_selected = document.getElementById('seats_selected');
const total_price = document.getElementById('total_price');

const ticket_price = document.getElementById('movie_price').getAttribute('data-value');

var seats = []

container.addEventListener('click', (event) => {
    if ( event.target.classList.contains('available_seat') ) {
        event.target.classList.toggle('selected_seat');

        if ( seats.includes(event.target.getAttribute('data-value')) ) {
            seats = seats.filter( (element) => element !== event.target.getAttribute('data-value') );

            updateVars()
        } else {
            seats.push(event.target.getAttribute('data-value'));

            updateVars()
        }
    }
});

function updateVars() {
    num_of_seats_selected.innerHTML = seats.length;
    total_price.innerHTML = ticket_price * seats.length;
    seats_selected.innerHTML = seats;
}
