import axios from "axios";
import MockAdapter from 'axios-mock-adapter';

var mock = new MockAdapter(axios);

mock.onGet('/states').reply(200 , 
    {
        "entity_id": "sensor.test_one_today_s_consumption",
        "state": "0.055",
        "attributes": {
          "state_class": "total_increasing",
          "unit_of_measurement": "kWh",
          "device_class": "energy",
          "friendly_name": "Test One Today's consumption"
        },
        "last_changed": "2024-09-25T15:09:34.476790+00:00",
        "last_reported": "2024-09-25T15:09:34.476790+00:00",
        "last_updated": "2024-09-25T15:09:34.476790+00:00",
        "context": {
          "id": "",
          "parent_id": null,
          "user_id": null
        }
      },
      {
        "entity_id": "sensor.test_two_today_s_consumption",
        "state": "0.055",
        "attributes": {
          "state_class": "total_increasing",
          "unit_of_measurement": "kWh",
          "device_class": "energy",
          "friendly_name": "Test Two Today's consumption"
        },
        "last_changed": "2024-09-25T15:09:34.476790+00:00",
        "last_reported": "2024-09-25T15:09:34.476790+00:00",
        "last_updated": "2024-09-25T15:09:34.476790+00:00",
        "context": {
          "id": "",
          "parent_id": null,
          "user_id": null
        }
      }
);