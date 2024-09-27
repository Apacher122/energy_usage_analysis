// eslint-disable-next-line no-undef
const socket = io();

socket.on("INIT", (response) => {
    const data = JSON.parse(response)
    var table = document.getElementById('device_data')
    var power_table = document.getElementById('current_wattage')
    for (const idx in data) {
        var row = `<tr class="device" id="item-id-${data[idx].entity_id}">
                    </tr>`
        table.innerHTML += row;

        var row_2 = `<tr class="device" id="item-id-power-${data[idx].entity_id}">
                    </tr>`
        
        power_table.innerHTML += row_2;
    }
});

socket.on("UPDATE", (response) => {
    const data = JSON.parse(response)
    const today = new Date();
    var console = document.getElementById('console');
    var date = document.getElementById('date');

    date.innerText = today;
    for (const idx in data) {
        let info = data[idx];
        let history = data[idx].history;
        let cost_daily = parseFloat(history.cost_daily);
        let cost_total = parseFloat(history.cost_total);
        let kwh_daily = parseFloat(history.kwh_daily);
        let kwh_total = parseFloat(history.kwh_total);
        let wattage = parseFloat(info.current_wattage);
        let wat_string = "";
        let power_status = info.power_status;
        kwh_daily = kwh_daily.toFixed(3)
        kwh_total = kwh_total.toFixed(3)
        cost_daily = cost_daily.toFixed(3)
        cost_total = cost_total.toFixed(3)
        if (wattage > 1000) {
            wat_string = `${(wattage / 1000).toFixed(3)} KWH`
        } else {
            wat_string = `${wattage} W`
        }

        try {
            var dev = 
                document.getElementById("item-id-" + info.entity_id)
            var pow = 
                document.getElementById(`item-id-power-${info.entity_id}`)
        } catch (err) {
            console.innerText += err
        }
        
        try {
            dev.innerHTML = (`
                    <td>${info.friendly_name}</td>
                    <td>${kwh_daily} kwh</td>
                    <td>${kwh_total}</td>
                    <td>$ ${cost_daily}</td>
                    <td>$ ${cost_total}</td>
            `)
            
            pow.innerHTML = (`
                <td>${info.friendly_name}</td>
                <td>${power_status}</td>
                <td>${wat_string}</td>
            `)

        }catch (err) {
            console.innerText += err + wattage
        }
        
    }
});
