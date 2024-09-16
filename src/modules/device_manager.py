"""TODO: Move elsewhere"""
import os
from kasa import Discover
from dotenv import load_dotenv

load_dotenv()

async def fetch_devices():
    """Load all devices from kasa"""
    username = os.getenv('UNAME')
    password = os.getenv('PWORD')
    devices = await Discover.discover(username=username, password=password)
    return devices
