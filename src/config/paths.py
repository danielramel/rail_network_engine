GLOBAL_ICON_PATHS = {
    "CONSTRUCTION": "src/icons/construction.png",
    "SIMULATION": "src/icons/simulation.png",
    "TIMETABLE": "src/icons/timetable.png",
    "SAVE": "src/icons/save.png",
    "LOAD": "src/icons/load.png",
}

CONSTRUCTION_ICON_PATHS = {
    "RAIL": "src/icons/construction/rail.png",
    "SIGNAL": "src/icons/construction/signal.png",
    "STATION": "src/icons/construction/station.png",
    "BULLDOZE": "src/icons/construction/bulldoze.png",
    "PLATFORM": "src/icons/construction/platform.png",
}


SIMULATION_ICON_PATHS = {
    "TRAIN_PLACEMENT": "src/icons/simulation/train_placement.png",
    "PLAY": "src/icons/simulation/play.png",
    "PAUSE": "src/icons/simulation/pause.png",
    "FAST_FORWARD": "src/icons/simulation/3x.png",
    "SUPER_FAST_FORWARD": "src/icons/simulation/10x.png",
}


ICON_PATHS = {
    **GLOBAL_ICON_PATHS,
    **CONSTRUCTION_ICON_PATHS,
    **SIMULATION_ICON_PATHS
}