/* eslint-disable no-unused-vars */
import { Server } from 'socket.io';
import schedule from 'node-schedule'
import day_changed from '../utils/helpers.js';
import * as dh from '../utils/datahandler.js';

let io = new Server();
const socketApi = {
    io: io
};

let devices = []

io.on('connection', async (socket) => {
    let today = new Date()
    let tomorrow = new Date(today)
    tomorrow.setDate(tomorrow.getDate() + 1)

    console.log(`${socket.id} connected`)
    await dh.fetch_all_devices();
    io.emit("INIT", JSON.stringify(devices));
    
    const job = schedule.scheduleJob('*/1 * * * * *', async() => {
        if (day_changed(today, tomorrow)) {
            await dh.fetch_all_devices();
        }
        await dh.fetch_rt()
        io.emit("UPDATE", JSON.stringify(devices))
    });

    socket.on('send', async data => {
        console.log(data);
        socket.broadcast.emit("UPDATE", data);
    });

    socket.on('disconnect', async data => {
        devices = []
        console.log(`${socket.id} disconnected`)
        schedule.gracefulShutdown()
    })
});


export { socketApi, devices };