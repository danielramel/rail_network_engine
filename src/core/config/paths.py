ICON_CATEGORIES = {
    "": {
        "CONSTRUCTION": "construction.png",
        "SIMULATION": "simulation.png",
        "SETUP": "setup.png",
        "ROUTE": "route.png",
        "SAVE": "save.png",
        "SAVED": "saved.png",
        "LOAD": "load.png",
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
        "TRAIN_PLACEMENT": "train_placement.png",
        "PLAY": "play.png",
        "PAUSE": "pause.png",
        "FAST_FORWARD": "3x.png",
        "SUPER_FAST_FORWARD": "10x.png",
    },
    "setup/": {
        "PLACE_TRAIN": "place_train.png",
        "REMOVE_TRAIN": "remove_train.png",
    }
}

ICON_PATHS = {
    key: f"src/assets/icons/{prefix}{filename}"
    for prefix, mapping in ICON_CATEGORIES.items()
    for key, filename in mapping.items()
}
