from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QTableWidget, QTableWidgetItem, 
                              QPushButton, QLabel, QHBoxLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QCursor
from config.colors import LIGHTBLUE, RED, YELLOW
from models.station import Station
from models.train import TrainRepository
from views.timetable.train_editor_dialog import TrainEditorDialog
from views.timetable.timetable_stylesheet import timetable_stylesheet

class TimetableWindow(QMainWindow):
    def __init__(self, train_repository: TrainRepository):
        super().__init__()
        self.train_repository = train_repository
        self.setWindowTitle("Train Timetable")
        self.setMinimumSize(1000, 600)
        
        self.setStyleSheet(timetable_stylesheet)
        
        # Track which rows are expanded
        self.expanded_rows = set()
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        add_btn = QPushButton("+ Add Train")
        add_btn.clicked.connect(self.add_train)
        layout.addWidget(add_btn, alignment=Qt.AlignmentFlag.AlignRight)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Type", "Route", "Start", "Frequency"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 500)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 120)
        
        # Connect cell click event
        self.table.cellClicked.connect(self.handle_cell_click)
        
        self.refresh_table()
        layout.addWidget(self.table)
        
        central_widget.setLayout(layout)
    
    
    def refresh_table(self):
        trains = self.train_repository.all()
        
        # Calculate total rows needed (trains + expanded station rows)
        total_rows = 0
        for train_idx, train in enumerate(trains):
            total_rows += 1  # Main train row
            if train_idx in self.expanded_rows:
                total_rows += len(train.stations)  # One row per station
        
        self.table.setRowCount(total_rows)
        
        actual_row = 0
        for train_idx, train in enumerate(trains):
            # Main train row
            is_expanded = train_idx in self.expanded_rows
            
            # Type
            type_item = QTableWidgetItem(train.code)
            type_item.setBackground(self._get_code_color(train.code))
            type_item.setForeground(QColor(0, 0, 0))
            type_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if is_expanded:
                self.table.setSpan(actual_row, 0, len(train.stations) + 1, 1)
            self.table.setItem(actual_row, 0, type_item)
            
            # Route with expand/collapse indicator
            arrow = "▼" if is_expanded else "▶"
            route = self._format_route(train.stations)
            
            route_item = QTableWidgetItem(f"{arrow} {route}")
            route_item.setData(Qt.ItemDataRole.UserRole, train_idx)  # Store train index
            route_item.setToolTip("Click to expand/collapse stations")
            route_item.setFlags(route_item.flags() ^ Qt.ItemFlag.ItemIsEditable)
            route_item.setForeground(QColor(255, 255, 255))
            route_item.setBackground(QColor(45, 45, 45))
            route_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(actual_row, 1, route_item)

            time_str = self._format_time(train.start_time)
            time_item = QTableWidgetItem(time_str)
            time_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if is_expanded:
                self.table.setSpan(actual_row, 2, len(train.stations) + 1, 1)
            self.table.setItem(actual_row, 2, time_item)
            
            # Frequency
            freq_item = QTableWidgetItem(f"{train.frequency} min")
            freq_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if is_expanded:
                self.table.setSpan(actual_row, 3, len(train.stations) + 1, 1)
            self.table.setItem(actual_row, 3, freq_item)
            
            actual_row += 1
            
            # If expanded, add individual station rows
            if is_expanded:
                for i, station in enumerate(train.stations, 1):
                    self._add_station_row(actual_row, station, i, len(train.stations))
                    actual_row += 1
    
    def _add_station_row(self, row, station, station_num, total_stations):
        """Add a row for an individual station"""
        # Type column is spanned from parent row - skip
        
        # Station row in route column
        prefix = "🚉" if station_num == 1 or station_num == total_stations else "  "
        station_name = station.name if isinstance(station, Station) else str(station)
        
        station_item = QTableWidgetItem(f"    {prefix} {station_num}. {station_name}")
        station_item.setBackground(QColor(35, 35, 35))
        station_item.setForeground(QColor(200, 200, 200))
        station_item.setFlags(station_item.flags() ^ Qt.ItemFlag.ItemIsEditable)
        station_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.table.setItem(row, 1, station_item)
        
        # Start and Frequency columns are spanned from parent row - skip
    
    def handle_cell_click(self, row, col):
        # Only toggle expansion when clicking on Route column (column 1)
        if col == 1:
            item = self.table.item(row, 1)
            if item:
                train_idx = item.data(Qt.ItemDataRole.UserRole)
                if train_idx is not None:  # Make sure it's a train row, not station row
                    self.toggle_row_expansion(train_idx)
    
    def toggle_row_expansion(self, train_idx):
        """Toggle the expansion state of a train row"""
        if train_idx in self.expanded_rows:
            self.expanded_rows.remove(train_idx)
        else:
            self.expanded_rows.add(train_idx)
        
        self.refresh_table()
    
    def add_train(self):
        dialog = TrainEditorDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            if data['stations']:
                # Convert station names to Station objects
                station_objects = [Station(name) for name in data['stations']]
                self.train_repository.add(
                    code=data['type'],
                    stations=station_objects,
                    start_time=data['start_time'],
                    frequency=data['frequency']
                )
                self.expanded_rows.clear()  # Clear expanded state on refresh
                self.refresh_table()
    
    def _format_time(self, minutes: int) -> str:
        """Convert minutes since midnight to HH:mm string."""
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours:02d}:{mins:02d}"
    
    def _get_code_color(self, code: str) -> QColor:
        if code.startswith("S"):
            return QColor(*LIGHTBLUE)
        elif code.startswith("Z"):
            return QColor(*YELLOW)
        
        return QColor(*RED)
    
    def _format_route(self, stations: list[Station]) -> str:
        if not stations:
            return "No stations"
        elif len(stations) == 1:
            return stations[0].name
        elif len(stations) == 2:
            return f"{stations[0].name} → {stations[1].name}"
        else:
            return f"{stations[0].name} → ... → {stations[-1].name}"