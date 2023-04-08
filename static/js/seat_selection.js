const container = document.querySelector('.container');
var seats = []

container.addEventListener('click', (event) => {
    if ( event.target.classList.contains('available_seat') ) {
        event.target.classList.toggle('selected_seat');
        //
        console.log(event.target.classList.contains('available_seat'));

        if ( seats.includes(event.target.getAttribute('data-value')) ) {
            seats = seats.filter( (element) => element !== event.target.getAttribute('data-value') );
        } else {
            seats.push(event.target.getAttribute('data-value'));
        }
        //
        console.log(seats);
    }
});
