from shiny import reactive, render
from shiny.express import ui

import random
from datetime import datetime
from collections import deque

from faicons import icon_svg
import pandas as pd

UPDATE_INTERVAL_SECS: int = 1

DEQUE_SIZE: int = 5
reactive_value_wrapper = reactive.value(deque(maxlen=DEQUE_SIZE))

@reactive.calc()
def reactive_calc_combined():
    reactive.invalidate_later(UPDATE_INTERVAL_SECS)
    temp = round(random.uniform(-20, -15), 2)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_dictionary_entry = {"temp": temp, "timestamp": timestamp}
    reactive_value_wrapper.get().append(new_dictionary_entry)
    deque_snapshot = reactive_value_wrapper.get()
    df = pd.DataFrame(deque_snapshot)
    latest_dictionary_entry = new_dictionary_entry
    return deque_snapshot, df, latest_dictionary_entry

ui.page_opts(title="Sarah's Antartic Data: Live Data (Basic)", fillable=True)

with ui.sidebar(open="open"):
    ui.h2("Antarctic Explorer", class_="text-center")
    icon_svg("cube")
    ui.p(
        "A demonstration of real-time temperature readings in Antarctica.",
        class_="text-center",
    )

    ui.hr()

    ui.h6("Links:")

    ui.a(
        "GitHub Source",
        href="https://https://github.com/sapapesh/cintel-05-cintel/tree/main",
        target="_blank",
    )

with ui.layout_columns():
    with ui.value_box(
        showcase=icon_svg("sun"),
        theme="bg-gradient-blue-purple",
    ):
    
        "Current Temperature"
    
        @render.text
        def display_temp():
            """Get the latest reading and return a temperature string"""
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['temp']} C"

        "still too cold"

with ui.layout_columns():
    with ui.value_box(
        showcase=icon_svg("moon"),
        theme="bg-gradient-green-yellow",
    ):
        
        "Current Date and Time"
        
        
        @render.text
        def display_time():
            """Get the latest reading and return a timestamp string"""
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['timestamp']}"

ui.hr()



with ui.layout_columns():
    with ui.card():
        ui.card_header("Current Data (placeholder only)")

with ui.layout_columns():
    with ui.card():
        ui.card_header("Current Chart (placeholder only)")
