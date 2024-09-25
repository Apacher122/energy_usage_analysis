import axios from "axios";
import * as dotenv from "dotenv";

dotenv.config({
    path: '../.env'
})

var ax_inst = axios.create({
    baseURL: 'http://homeassistant.local:8123/api'
});

// eslint-disable-next-line no-undef
var auth = "Bearer ".concat(process.env.HOMEASSISTANT_TOKEN)
ax_inst.defaults.headers.common['Authorization'] = auth
export { ax_inst };