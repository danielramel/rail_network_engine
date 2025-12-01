ICON_CATEGORIES = {
    "": {
        "CONSTRUCTION": "construction.png",
        "SIMULATION": "simulation.png",
        "TRAIN_PLACEMENT": "train_placement.png",
        "timetable": "timetable.png",
        "SAVE": "save.png",
        "SAVED": "saved.png",
        "UNSAVED": "unsaved.png",
        "OPEN": "open.png",
        "EXIT": "exit.png"
    },
    "construction/": {
        "RAIL": "rail.png",
        "TUNNEL": "tunnel.png",
        "SIGNAL": "signal.png",
        "STATION": "station.png",
        "BULLDOZE": "bulldoze.png",
        "PLATFORM": "platform.png",
    },
    "simulation/": {
        "PLAY": "play.png",
        "PAUSE": "pause.png",
        "FAST_FORWARD": "fast.png",
        "SUPER_FAST_FORWARD": "super_fast.png",
    },
    "train_placement/": {
        "PLACE_TRAIN": "place_train.png",
        "REMOVE_TRAIN": "remove_train.png",
    }
}

ICON_PATHS = {
    key: f"src/assets/icons/{prefix}{filename}"
    for prefix, mapping in ICON_CATEGORIES.items()
    for key, filename in mapping.items()
}
