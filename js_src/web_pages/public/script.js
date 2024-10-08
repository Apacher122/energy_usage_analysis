const notify = document.querySelector("#notification")
const message = document.querySelector("#message")
const button = document.querySelector("button")
const header = document.querySelector("#header")

var socket = io();
var list = document.getElementById('data_inputs')

var entity_id = ""
var state = ""

function printMessage(e) {
    e.preventDefault()
    socket.emit('send', message.value)
}

socket.on('update', function(data) {
    console.log("RECEIVED")
    const devices = JSON.parse(data);
    console.log(data)
    notify.textContent = data;
    for (index in devices) {
        let li = document.createElement('li');
        li.innerHTML.text = devices[index].entity_id
        list.appendChild(li)
    }
});

button.addEventListener("click", printMessage)