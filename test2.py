# Requires: pip install dearpygui
import dearpygui.dearpygui as dpg

stations = ["Central", "North", "East", "South", "West", "Airport"]

dpg.create_context()

TABLE_TAG = "train_table"

def open_add_window(sender, app_data, user_data):
    dpg.configure_item("add_window", show=True)

def add_train_callback(sender, app_data, user_data):
    code = dpg.get_value("inp_code").strip()
    station = dpg.get_value("inp_station")
    freq = dpg.get_value("inp_freq")
    start_time = dpg.get_value("inp_start")

    if not code:
        dpg.configure_item("msg", default_value="Error: code required")
        return

    # Basic validation
    try:
        freq_int = int(freq)
    except Exception:
        dpg.configure_item("msg", default_value="Error: frequency must be integer")
        return

    # Add a row to the table
    row = dpg.add_table_row(parent=TABLE_TAG)
    dpg.add_text(code, parent=row)
    dpg.add_text(station if station else "-", parent=row)
    dpg.add_text(str(freq_int), parent=row)
    dpg.add_text(start_time if start_time else "-", parent=row)

    # clear inputs and hide window
    dpg.set_value("inp_code", "")
    dpg.set_value("inp_freq", 60)
    dpg.set_value("inp_start", "06:00")
    dpg.set_value("msg", "Added")
    dpg.configure_item("add_window", show=False)


with dpg.window(label="Train Manager", width=700, height=400):
    dpg.add_text("Trains")
    # Table
    with dpg.table(tag=TABLE_TAG, header_row=True, resizable=True, row_background=True):
        dpg.add_table_column(label="Code")
        dpg.add_table_column(label="Station List")
        dpg.add_table_column(label="Frequency (min)")
        dpg.add_table_column(label="Start Time")

    # Bottom controls
    with dpg.group(horizontal=True):
        dpg.add_spacer(width=1)  # small spacing
        dpg.add_button(label="Add Train", callback=open_add_window)

# Add Train window (modal)
with dpg.window(label="Add Train", modal=True, show=False, tag="add_window", width=400, height=220):
    dpg.add_text("Create new train")
    dpg.add_input_text(label="Code", tag="inp_code", width=300)
    dpg.add_combo(items=stations, label="Station list", tag="inp_station", width=300)
    dpg.add_input_int(label="Frequency (min)", tag="inp_freq", width=150, default_value=60, min_value=1)
    dpg.add_input_text(label="Start time (HH:MM)", tag="inp_start", width=150, default_value="06:00")
    dpg.add_spacing(count=1)
    with dpg.group(horizontal=True):
        dpg.add_button(label="Add", callback=add_train_callback)
        dpg.add_button(label="Cancel", callback=lambda s,a,u: dpg.configure_item("add_window", show=False))
    dpg.add_text("", tag="msg")

# Start DearPyGui
dpg.create_viewport(title='Trains table', width=800, height=480)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
