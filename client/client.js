//Tugas Besar II Jarkom
const WebSocket = require('ws')

// const PORT = 600;

var ws = new WebSocket(`ws://localhost:${process.env.PORT}/`);

ws.on('open', function open() {
    ws.send("Hello")
})