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
                console.log("Getting Historical Data");
                for (const idx in response.data) {
                    if (
                        response.data[idx].entity_id.includes('_today_s_consumption') &&
                        !response.data[idx].entity_id.includes('_cost')
                    ) {
                        let device = new Device(
                            response.data[idx].entity_id,
                            response.data[idx].state
                        );
                        await get_device_history(device);
                        devices.push(device);
                    }
                }
                console.log("Historical Data Loaded");
            });
    } catch (err) {
        console.log(`DEBUG: ${arguments.callee.name} -> ${err}`)
    }
    console.log("Devices Loaded");
}

async function fetch_rt() {
    for (const idx in devices) {
        try {
            await ax_inst
                .get(`/states/${devices[idx].entity_id}`)
                .then(function (response) {
                    devices[idx].calculate_kwh_today(parseFloat(response.data.state))
                    devices[idx].calculate_running_cost()
                })
        } catch (err) {
            console.log(`DEBUG: ${arguments.callee.name} -> ${err}`)
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
                    devices[idx].current_wattage = parseFloat(response.data.state)
                })
        } catch (err) {
            console.log(`DEBUG: ${arguments.callee.name} -> ${err}`)
        }

        try {
            let power_status = devices[idx].entity_id
            power_status = power_status
                .replace("_today_s_consumption", "")
                .replace("sensor.", "switch.")
            await ax_inst
                .get(`/states/${power_status}`)
                .then(function (response) {
                    devices[idx].power_status = response.data.state
                })
        } catch (err) {
            console.log(`DEBUG: ${arguments.callee.name} -> ${err}`)
        }
    }
}

async function get_device_history(device) {
    var time_format = "YYYY-MM-DDTHH:mm:ssZ"
    var past_date = moment("2024-07-01T00:00:00-05:00")
    var date_today = moment(new Date(), time_format)
    var total = 0.0
    for (
        var start = moment(past_date);
        start.diff(date_today, 'days') <= 0;
        start.add(1, 'days')
    ) {
        var day_start = moment(start);
        var day_end = moment(start);
        day_start.set({hour:6,minute:0,second:0,millisecond:0});
        day_end.set({hour:19,minute:59,second:0,millisecond:0});
        try {
            await ax_inst
                .get(`/history/period/${day_start.format(time_format)}`, {
                    params: {
                        filter_entity_id: `${device.entity_id}`,
                        end_time: `${day_end.format(time_format)}`
                    }
                })
                .then(function (response) {
                    if (response.data[0] != undefined) {
                        try {
                            let start_kwh = parseFloat(response.data[0][0].state)
                            let end_kwh = parseFloat(response.data[0][response.data[0].length - 1].state);
                            if (moment(response.data[0][0].last_changed).isSame(date_today, 'day')) {
                                device.state = parseFloat(response.data[0][0].state)
                            }
                            
                            if (!isNaN(start_kwh) && !isNaN(end_kwh)) {
                                total += (end_kwh - start_kwh);
                            }
                        } catch (err) {
                            console.log(`DEBUG -> ${err}`)
                        }
                    }
                    device.kwh_total = total
                });
        } catch (err) {
            console.log(`DEBUG: ${arguments.callee.name} -> ${err}`)
        }
    }
}

export { 
    fetch_all_devices,
    fetch_rt
}