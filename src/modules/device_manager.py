from kasa import Discover
from dotenv import load_dotenv
import os

load_dotenv()

async def fetch_devices():
    username = os.getenv('UNAME')
    password = os.getenv('PWORD')
    devices = await Discover.discover(username=username, password=password)
    return devices
