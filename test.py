# save as trains_pygame_gui.py
import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UILabel, UIWindow, UITextEntryLine, UIDropDownMenu, UISelectionList
from pygame_gui.core import ObjectID

pygame.init()
WINDOW_SIZE = (800, 480)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Trains - pygame_gui example")
clock = pygame.time.Clock()

manager = pygame_gui.UIManager(WINDOW_SIZE)

# sample stations
STATIONS = ['Central', 'North', 'East', 'South', 'West']

# data storage
trains = [
    {"code": "T001", "station": "Central", "frequency": "30", "start_time": "06:00"},
    {"code": "T002", "station": "North",   "frequency": "45", "start_time": "07:15"},
]   

# header label
header = UILabel(relative_rect=pygame.Rect(10, 10, 780, 30),
                 text="Code    | Station    | Frequency(min) | Start Time",
                 manager=manager,
                 object_id=ObjectID(class_id="@header"))

# selection list used as a simple table (rows are strings with columns)
def format_row(item):
    return f"{item['code']:<7} | {item['station']:<10} | {item['frequency']:<14} | {item['start_time']}"

selection_list = UISelectionList(relative_rect=pygame.Rect(10, 50, 780, 300),
                                 item_list=[format_row(t) for t in trains],
                                 manager=manager)

# Add Train button
add_button = UIButton(relative_rect=pygame.Rect(10, 370, 140, 40),
                      text="Add Train",
                      manager=manager)

# status label
status = UILabel(relative_rect=pygame.Rect(160, 370, 630, 40),
                 text="Select a train from the list or add a new one.",
                 manager=manager)

add_window = None  # will hold the add-train UIWindow instance

def open_add_window():
    global add_window
    if add_window is not None:
        return  # already open

    add_window = UIWindow(rect=pygame.Rect(200, 80, 400, 260),
                          manager=manager,
                          window_display_title="Add Train",
                          object_id=ObjectID(class_id="@add_window"))

    # labels and inputs
    LABEL_W = 120
    INPUT_W = 220
    y = 10
    gap = 45

    UILabel(relative_rect=pygame.Rect(10, y, LABEL_W, 30), text="Code:", manager=manager, container=add_window)
    code_input = UITextEntryLine(relative_rect=pygame.Rect(140, y, INPUT_W, 30), manager=manager, container=add_window)
    y += gap

    UILabel(relative_rect=pygame.Rect(10, y, LABEL_W, 30), text="Station:", manager=manager, container=add_window)
    station_dd = UIDropDownMenu(options_list=STATIONS,
                                starting_option=STATIONS[0],
                                relative_rect=pygame.Rect(140, y, INPUT_W, 30),
                                manager=manager,
                                container=add_window)
    y += gap

    UILabel(relative_rect=pygame.Rect(10, y, LABEL_W, 30), text="Frequency (min):", manager=manager, container=add_window)
    freq_input = UITextEntryLine(relative_rect=pygame.Rect(140, y, INPUT_W, 30), manager=manager, container=add_window)
    y += gap

    UILabel(relative_rect=pygame.Rect(10, y, LABEL_W, 30), text="Start Time (HH:MM):", manager=manager, container=add_window)
    start_input = UITextEntryLine(relative_rect=pygame.Rect(140, y, INPUT_W, 30), manager=manager, container=add_window)
    y += gap

    # submit and cancel
    submit = UIButton(relative_rect=pygame.Rect(70, y, 100, 32), text="Add", manager=manager, container=add_window)
    cancel = UIButton(relative_rect=pygame.Rect(230, y, 100, 32), text="Cancel", manager=manager, container=add_window)

    # attach references so we can find them in events
    add_window.metadata = {
        "code_input": code_input,
        "station_dd": station_dd,
        "freq_input": freq_input,
        "start_input": start_input,
        "submit": submit,
        "cancel": cancel
    }

def close_add_window():
    global add_window
    if add_window:
        add_window.kill()
    add_window = None

def add_train_from_window():
    global trains, selection_list, add_window
    meta = add_window.metadata
    code = meta["code_input"].get_text().strip()
    station = meta["station_dd"].selected_option
    frequency = meta["freq_input"].get_text().strip()
    start_time = meta["start_input"].get_text().strip()

    # basic validation
    if not code:
        status.set_text("Error: Code is required.")
        return
    if not frequency.isdigit():
        status.set_text("Error: Frequency must be an integer (minutes).")
        return
    # simple time format check HH:MM
    parts = start_time.split(":")
    if len(parts) != 2 or not all(p.isdigit() for p in parts):
        status.set_text("Error: Start time must be HH:MM.")
        return
    hh, mm = int(parts[0]), int(parts[1])
    if not (0 <= hh <= 23 and 0 <= mm <= 59):
        status.set_text("Error: Start time out of range.")
        return

    trains.append({"code": code, "station": station, "frequency": frequency, "start_time": start_time})
    selection_list.set_item_list([format_row(t) for t in trains])
    status.set_text(f"Added train {code} -> {station} at {start_time}.")
    close_add_window()

running = True
while running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # button clicks and UI events
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == add_button:
                    open_add_window()
                # if add_window exists, check its submit/cancel
                if add_window:
                    meta = add_window.metadata
                    if event.ui_element == meta["submit"]:
                        add_train_from_window()
                    if event.ui_element == meta["cancel"]:
                        close_add_window()

            # selection list item clicked
            if event.user_type == pygame_gui.UI_SELECTION_LIST_DOUBLE_CLICKED_SELECTION:
                if event.ui_element == selection_list:
                    idx = event.text  # text is the clicked row string
                    status.set_text(f"Row selected: {idx}")

        manager.process_events(event)

    manager.update(time_delta)

    screen.fill((30, 30, 30))
    manager.draw_ui(screen)

    pygame.display.flip()

pygame.quit()
