//Tugas Besar II Jarkom
const WebSocket = require('ws')
const fs = require('fs')

// const PORT = 600;

var ws = new WebSocket(`ws://localhost:${process.env.PORT}/`);
// var ws = new WebSocket(`ws://3da3273a.ngrok.io`);

console.log("starting")

ws.on('open', function open() {
    console.log("wakgeng")
    ws.send('!submission')
    // ws.send("harusnya udh bener dan bisa di baca semuanya......... titik titik ini udh g bakal kebaca harusnya udh bener dan bisa di baca semuanya......... titik titik ini udh g bakal kebaca harusnya udh bener dan bisa di baca semuanya......... titik titik ini udh g bakal kebaca harusnya udh bener dan bisa di baca semuanya......... titik titik ini udh g bakal kebaca harusnya udh bener dan bisa di baca semuanya......... titik titik ini udh g bakal kebaca harusnya udh bener dan bisa di baca semuanya......... titik titik ini udh g bakal kebaca harusnya udh bener dan bisa di baca semuanya......... titik titik ini udh g bakal kebaca test test ")
    ws.on('message', function incoming(data) {
        console.log("message msk")
        console.log(data)
        fs.writeFileSync('a.zip', data)
        console.log("message mau keluar")
    })
})

ws.on('error', err => {
    console.log('errr')
    console.log(err)
})

ws.on('close', function close() {
    console.log("byee")
})