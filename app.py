from shiny import reactive, render
from shiny.express import ui

import random
from datetime import datetime
from collections import deque

from faicons import icon_svg
import pandas as pd
import plotly.express as px
from shinywidgets import render_plotly
from scipy import stats


ui.input_dark_mode(id="Dark", mode="dark")

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
        href="https://https://github.com/sapapesh/cintel-05-cintel",
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

    with ui.card(full_screen=True):
        ui.card_header("Current Date and Time")
        

    
        @render.text
        def display_time():
            """Get the latest reading and return a timestamp string"""
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['timestamp']}"

#with ui.card(full_screen=True, min_height="40%"):
with ui.card(full_screen=True):
    ui.card_header("Most Recent Readings")

    @render.data_frame
    def display_df():
        """Get the latest reading and return a dataframe with current readings"""
        deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
        pd.set_option('display.width', None)        # Use maximum width
        return render.DataGrid( df,width="100%")

with ui.card():
    ui.card_header("Chart with Current Trend")

    @render_plotly
    def display_plot():
        deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
        if not df.empty:
           df["timestamp"] = pd.to_datetime(df["timestamp"]) 

        fig = px.scatter(df,
            x="timestamp",
            y="temp",
            title="Temperature Readings with Regression Line",
            labels={"temp": "Temperature (°C)", "timestamp": "Time"},
            color_discrete_sequence=["blue"] )

        sequence = range(len(df))
        x_vals = list(sequence)
        y_vals = df["temp"]

        slope, intercept, r_value, p_value, std_err = stats.linregress(x_vals, y_vals)
        df['best_fit_line'] = [slope * x + intercept for x in x_vals]

        fig.add_scatter(x=df["timestamp"], y=df['best_fit_line'], mode='lines', name='Regression Line')
        fig.update_layout(xaxis_title="Time",yaxis_title="Temperature (°C)")
        fig.update_layout(font_color="black")
        return fig
        
        
        @render.text
        def display_time():
            """Get the latest reading and return a timestamp string"""
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['timestamp']}"
