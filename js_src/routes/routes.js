import express from 'express';
import ha_controller from '../controller/ha_controller.js';
import { Router } from 'express';

const router = Router().use(express.json());
router.get("/get_devices", ha_controller.get_devices)
router.get("/real_time", ha_controller.get_real_time_today)

export default router;