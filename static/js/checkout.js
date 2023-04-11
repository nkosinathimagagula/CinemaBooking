const modal = document.getElementById('modal');
const button = document.getElementById('button');
const count = document.getElementsByClassName('heading')[0].getAttribute('data-value');

let details = {};

button.onclick = function() {
    let element_count = 0;          // for counting inputs elements that are not empty

    for (let index = 0; index < count; index++) {
        let element = document.getElementById('name_' + index);
        if ( element.value === '' ) {
            element.style.border = "2px solid red";
        } else {
            details[index] = element.value;
            element_count++;
        }
    }

    if (element_count === Number(count)) {
        modal.style.display = "none";

        for (let index = 0; index < count; index++) {
            let element = document.getElementById('c_' + index).value = details[index];
        }
    }
}
