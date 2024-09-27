import { devices } from "../socket/socket_handler.js";
import { ax_inst } from '../axiom_config.js';
import moment from 'moment';
import Device from '../model/devices.js';

async function fetch_all_devices() {
    console.log("Fetching Devices")
    try {
        await ax_inst
            .get('/states')
            .then(async function (response) {
                const data = response.data;
                console.log("Getting Historical Data");
                for (const idx in data) {
                    const info = data[idx];
                    if (
                        info.entity_id.includes('_today_s_consumption') &&
                        !info.entity_id.includes('_cost')
                    ) {
                        let device = 
                            new Device(info.entity_id, info.state);
                        await get_device_history(device);
                        devices.push(device);
                    }
                }
                console.log("Historical Data Loaded");
            });
    } catch (err) {
        console.log(`DEBUG: ${arguments.callee.name} -> ${err}`);
    }
    console.log("Devices Loaded");
}

async function fetch_rt() {
    for (const idx in devices) {
        try {
            await ax_inst
                .get(`/states/${devices[idx].entity_id}`)
                .then(function (response) {
                    let current_val = parseFloat(response.data.state);
                    let start_val = devices[idx].state;
                    devices[idx].history.set_stats(current_val - start_val)
                })
        } catch (err) {
            console.log(`DEBUG: -> ${err}`);
        }

        try {
            let device_wattage = devices[idx].entity_id
            device_wattage = device_wattage.replace(
                "_today_s_consumption",
                "_current_consumption"
            )
            await ax_inst
                .get(`/states/${device_wattage}`)
                .then(function (response) {
                    devices[idx].current_wattage =
                        parseFloat(response.data.state);
                })
        } catch (err) {
            console.log(`DEBUG: ${arguments.callee.name} -> ${err}`);
        }

        try {
            let power_status = devices[idx].entity_id
            power_status = power_status
                .replace("_today_s_consumption", "")
                .replace("sensor.", "switch.")
            await ax_inst
                .get(`/states/${power_status}`)
                .then(function (response) {
                    devices[idx].power_status = response.data.state;
                })
        } catch (err) {
            console.log(`DEBUG: ${arguments.callee.name} -> ${err}`);
        }
    }
}

async function get_device_history(device) {
    const fmt = "YYYY-MM-DDTHH:mm:ssZ";
    const past = moment("2024-07-01T00:00:00-05:00");
    const present = moment(new Date(), fmt);
    for (
        let start = moment(past);
        start.diff(present, 'days') <= 0;
        start.add(1, 'days')
    ) {
        let day_start = moment(start);
        let day_end = moment(start);
        day_start.set({hour:6,minute:0,second:0,millisecond:0});
        day_end.set({hour:19,minute:59,second:0,millisecond:0});
        try {
            await ax_inst
                .get(`/history/period/${day_start.format(fmt)}`, {
                    params: {
                        filter_entity_id: `${device.entity_id}`,
                        end_time: `${day_end.format(fmt)}`
                    }
                })
                .then(function (response) {
                    let data = response.data[0];
                    if (data != undefined) {
                        try {
                            let last = (data.length - 1);
                            let start_kwh = parseFloat(data[0].state);
                            let end_kwh = parseFloat(data[last].state);
                            let last_changed = data[0].last_changed;
                            if (moment(last_changed).isSame(present, 'day') &&
                                data[0].state != undefined
                            ) {
                                device.state = start_kwh;
                            }
                            
                            if (!isNaN(start_kwh) && !isNaN(end_kwh)) {
                                device.history.start_total += 
                                    (end_kwh - start_kwh);
                            }
                        } catch (err) {
                            console.log(`DEBUG -> ${err}`);
                        }
                    }
                });
        } catch (err) {
            console.log(`DEBUG: -> ${err}`);
        }
    }
}

export { 
    fetch_all_devices,
    fetch_rt
}