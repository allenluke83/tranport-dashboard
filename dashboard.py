#%%
import os, sys, time, requests
from PIL import Image, ImageDraw, ImageFont, ImageOps


# Set up stop and screen details
STOP_ID = "490006080N"  # Replace with your stop ID
API_URL = f"https://api.tfl.gov.uk/StopPoint/{STOP_ID}/Arrivals"

# Train details
TRAIN_STOP_ID = "910GHERNEH"
TRAIN_API_URL = f"https://api.tfl.gov.uk/StopPoint/{TRAIN_STOP_ID}/Arrivals"
# 1. Setup paths
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

# %%

def get_bus_arrivals():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        # Sort buses by arrival time (timeToStation is in seconds)
        buses = sorted(data, key=lambda x: x["timeToStation"])

        formatted_arrivals = []
        for bus in buses[:6]:  # Grab top 4 upcoming buses
            line = bus.get("lineName")
            destination = bus.get("destinationName")
            mins_left = round(bus.get("timeToStation") / 60)
            formatted_arrivals.append(f"{line} to {destination}: {mins_left}m")
        return formatted_arrivals
    return ["Error fetching data"]


def get_train_arrivals():
    response = requests.get(TRAIN_API_URL)
    if response.status_code == 200:
        data = response.json()
        # Sort trains by arrival time (timeToStation is in seconds)
        trains = sorted(data, key=lambda x: x.get("timeToStation", 0))

        formatted_arrivals = []
        for train in trains[:6]:  # Grab top upcoming trains
            line = train.get("lineName")
            destination = train.get("destinationName")
            mins_left = round(train.get("timeToStation", 0) / 60)
            formatted_arrivals.append(f"{line} to {destination}: {mins_left}m")
        return formatted_arrivals
    return ["Error fetching data"]

# %%
bus_times = get_bus_arrivals()

train_times = get_train_arrivals()

# %%
