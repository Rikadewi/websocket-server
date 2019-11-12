//Tugas Besar II Jarkom
const WebSocket = require('ws')
const fs = require('fs')

// const PORT = 600;

var ws = new WebSocket(`ws://localhost:${process.env.PORT}/`);
// var ws = new WebSocket(`ws://3da3273a.ngrok.io`);

console.log("starting")

var udah = true

ws.on('open', function open() {
    console.log("socket opened")
    ws.ping("hello")
    // ws.send('!submission')
    // ws.close(1000, 'hello')
    // ws.send("harusnya udh bener dan bisa di baca semuanya......... titik titik ini udh g bakal kebaca harusnya udh bener dan bisa di baca semuanya......... titik titik ini udh g bakal kebaca harusnya udh bener dan bisa di baca semuanya......... titik titik ini udh g bakal kebaca harusnya udh bener dan bisa di baca semuanya......... titik titik ini udh g bakal kebaca harusnya udh bener dan bisa di baca semuanya......... titik titik ini udh g bakal kebaca harusnya udh bener dan bisa di baca semuanya......... titik titik ini udh g bakal kebaca harusnya udh bener dan bisa di baca semuanya......... titik titik ini udh g bakal kebaca test test ")
    ws.on('message', function incoming(data) {
        console.log("message msk")
        console.log(data)
        // if (udah) {
        //     console.log("buat file")
        //     fs.writeFileSync('a.zip', data)
        //     ws.send(data)
        //     udah = false
        // }

        console.log("message mau keluar")
    })
})

ws.on('pong', data => {
    console.log(data)
    console.log("pong terima")
})
ws.on('error', err => {
    console.log('errr')
    console.log(err)
})

ws.on('close', function close(data) {
    console.log(data)
    console.log("byee")
})


