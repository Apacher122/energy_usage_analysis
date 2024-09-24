import { response } from 'express';
import { ax_inst } from '../axiom_config.js';
import Device from '../model/devices.js';

async function get_devices() {
    const devices = []
    try {
        await ax_inst
            .get('/states')
            .then(function (response) {
                const data = JSON.stringify(response.data)
                const substr = '_today_s_consumption'
                for (const idx in response.data) {
                    if (response.data[idx].entity_id.includes(substr)) {
                        let entity_id = response.data[idx].entity_id
                        let state = response.data[idx].state
                        let device = new Device(entity_id, state)
                        devices.push(device);
                    }
                }
                return devices;
            });
    } catch (err) {
        console.log(err)
    }
}

async function get_real_time_today(device, entity_id) {
    let curr_consumption
    try {
        await ax_inst
            .get(`/state/${entity_id}`)
            .then(function (response)) {
                curr_consumption = response.state
                return device.calculate_kwh_today(curr_consumption)
            }
    }
}

export { get_devices, get_real_time_today };