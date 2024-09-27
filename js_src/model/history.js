/* eslint-disable no-undef */
import moment from 'moment';
import * as dotenv from "dotenv";
dotenv.config({
    path: '../.env'
})

export const History = class {
    constructor() {
        this.kwh_daily = 0.0;
        this.kwh_monthly = 0.0;
        this.kwh_total = 0.0;
        this.cost_daily = 0.0;
        this.cost_monthly = 0.0;
        this.cost_total = 0.0;
    }

    set_stats(daily) {
        let monthly_cost = parseFloat(process.env.COST_PER_KWH);
        if (this.in_billing_window()) {
            this.kwh_daily = daily;
            this.kwh_total += this.kwh_daily;
            console.log(this.kwh_total)
        }
        this.cost_daily = this.kwh_daily * monthly_cost;
        this.cost_total = this.kwh_total * monthly_cost;
    }

    in_billing_window() {
        let today = moment();
        let start = moment(today);
        let end = moment(today);

        start.set({hour:6,minute:0,second:0,millisecond:0});
        end.set({hour:19,minute:59,second:0,millisecond:0});

        if (today.isBetween(start, end)) {
            return true;
        }

        return false;
    }
}