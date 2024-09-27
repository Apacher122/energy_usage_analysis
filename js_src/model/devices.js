import { History } from './history.js';

const Device = class {
    constructor(entity_id = "", state) {
        this.entity_id = entity_id;
        this.state = parseFloat(state);
        this.history = new History();
        this.current_wattage = 0.0;
        this.power_status = "";
        this.friendly_name = entity_id
            .replace("sensor.", "")
            .replace("_today_s_consumption", "")
            .replace(/_/g, ' ')
    }
};

export default Device;
