const socket = io();
console.log("TEST")
const today = new Date();
var datetime = today.toLocaleString();

socket.on("INIT", (response) => {
    const data = JSON.parse(response)
    var table = document.getElementById('device_data')
    var console = document.getElementById('console')
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
    var datetime = today.toLocaleString();
    var table = document.getElementById('device_data');
    var console = document.getElementById('console');
    var date = document.getElementById('date');
    var power_table = document.getElementById('current_wattage')

    date.innerText = today;
    for (const idx in data) {
        let cost = parseFloat(data[idx].cost)
        let kwh = parseFloat(data[idx].kwh_today)
        let historical = parseFloat(data[idx].kwh_historical)
        let overall_cost = parseFloat(data[idx].cost_all_time)
        let wattage = parseFloat(data[idx].current_wattage)
        let wat_string = ""
        let power_status = data[idx].power_status
        historical = historical.toFixed(3)
        kwh = kwh.toFixed(3)
        cost = cost.toFixed(3)
        overall_cost = overall_cost.toFixed(3)
        if (wattage > 1000) {
            wat_string = `${(wattage / 1000).toFixed(3)} KWH`
        } else {
            wat_string = `${wattage} W`
        }
        var row = `<tr class="item-id-${data[idx].entity_id}">
                        <td>${data[idx].friendly_name}</td>
                        <td>${kwh}</td>
                        <td>${historical}</td>
                        <td>${cost}</td>
                        <td>${overall_cost}</td>
                    </tr>`;

        var row_2 = `<tr class="item-id-power-${data[idx].entity_id}">
                        <td>${data[idx].friendly_name}</td>
                        <td>${power_status}</td>
                        <td>${wat_string}</td>
                    </tr>`;

        try {
            var dev = document.getElementById("item-id-" + data[idx].entity_id)
            var pow = document.getElementById(`item-id-power-${data[idx].entity_id}`)
        } catch (err) {
            console.innerText += err
        }
        
        try {
            dev.innerHTML = (`
                    <td>${data[idx].friendly_name}</td>
                    <td>${kwh} kwh</td>
                    <td>${historical}</td>
                    <td>$ ${cost}</td>
                    <td>$ ${overall_cost}</td>
            `)
            
            pow.innerHTML = (`
                <td>${data[idx].friendly_name}</td>
                <td>${power_status}</td>
                <td>${wat_string}</td>
            `)

        }catch (err) {
            console.innerText += err + wattage
        }
        
    }
});
