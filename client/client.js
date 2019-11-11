//Tugas Besar II Jarkom
const WebSocket = require('ws')
const fs = require('fs')

// const PORT = 600;

var ws = new WebSocket(`ws://localhost:${process.env.PORT}/`);
// var ws = new WebSocket(`ws://3da3273a.ngrok.io`);


ws.on('open', function open() {
    ws.send('!submission')
    // ws.send("harusnya udh bener dan bisa di baca semuanya......... titik titik ini udh g bakal kebaca harusnya udh bener dan bisa di baca semuanya......... titik titik ini udh g bakal kebaca harusnya udh bener dan bisa di baca semuanya......... titik titik ini udh g bakal kebaca harusnya udh bener dan bisa di baca semuanya......... titik titik ini udh g bakal kebaca harusnya udh bener dan bisa di baca semuanya......... titik titik ini udh g bakal kebaca harusnya udh bener dan bisa di baca semuanya......... titik titik ini udh g bakal kebaca harusnya udh bener dan bisa di baca semuanya......... titik titik ini udh g bakal kebaca test test ")
    // ws.on('message', function incoming(data) {
    //     fs.writeFileSync('a.zip', data)
    // })
})