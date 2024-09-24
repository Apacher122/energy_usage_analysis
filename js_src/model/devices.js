import moment from 'moment';

const Device = class {
    constructor(entity_id = "", state) {
        this.entity_id = entity_id;
        this.state = parseFloat(state);
        this.kwh_total = 0.0;
        this.kwh_today = 0.0;
        this.cost = 0.0;
        this.cost_all_time = 0.0;
        this.kwh_historical = 0.0;
        this.current_wattage = 0.0;
        this.power_status = "";
        this.friendly_name = entity_id
            .replace("sensor.", "")
            .replace("_today_s_consumption", "")
            .replace(/_/g, ' ')
    }

    calculate_kwh_today(kwh_end) {
        var date_today = moment();
        var day_start = moment(date_today)
        var day_end = moment(date_today)

        day_start.set({hour:6,minute:0,second:0,millisecond:0})
        day_end.set({hour:19,minute:59,second:0,millisecond:0})

        if (date_today.isBetween(day_start,day_end))
        {
            this.kwh_today = (kwh_end - this.state);
            this.kwh_historical = (kwh_end - this.state) + this.kwh_total;
        }
        this.kwh_historical = this.kwh_total;
    }

    calculate_running_cost() {
        var date_today = moment();
        var day_start = moment(date_today)
        var day_end = moment(date_today)

        day_start.set({hour:6,minute:0,second:0,millisecond:0})
        day_end.set({hour:19,minute:59,second:0,millisecond:0})

        if (date_today.isBetween(day_start,day_end))
        {
            this.cost = this.kwh_today * 0.23381;
        }
        this.cost_all_time = this.kwh_historical * 0.23381;
    }
};

export default Device;
