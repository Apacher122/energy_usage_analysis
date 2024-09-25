import { ax_inst } from '../axiom_config.js';
import Device from '../model/devices.js';
import { fileURLToPath } from 'url';
import path from 'path';


let devices = []

const __filename = fileURLToPath(import.meta.url); // get the resolved path to the file
const __dirname = path.dirname(__filename); // get the name of the director

const get_devices = async (_req, res) => {
    try {
        await ax_inst
            .get('/states')
            .then(function (response) {
                const data = response.data
                const substr = '_today_s_consumption'
                for (const idx in response.data) {
                    if (response.data[idx].entity_id.includes(substr)) {
                        let entity_id = response.data[idx].entity_id
                        let state = response.data[idx].state
                        let device = new Device(entity_id, state)
                        devices.push(device);
                    }
                }
                res.status(201).json({data})
            });
    } catch (err) {
        console.log(err)
    }
}

const get_real_time_today = async (_req, res) => {
    try {
        res.sendFile(path.join(__dirname, '../web_pages/realtime.html'))
    } catch (err) {
        console.log(err)
    }
};

export default { get_devices, get_real_time_today };