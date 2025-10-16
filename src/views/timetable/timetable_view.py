from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                              QTableWidget, QTableWidgetItem, 
                              QPushButton)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from config.colors import BLACK, LIGHTBLUE, RED, YELLOW
from models.station import Station
from models.train import TrainRepository
from views.timetable.train_editor_dialog import TrainEditorDialog
from views.timetable.timetable_stylesheet import TIMETABLE_STYLESHEET
from PyQt6.QtCore import pyqtSignal

class TimetableWindow(QMainWindow):
    window_closed = pyqtSignal()
    def __init__(self, train_repository: TrainRepository):
        super().__init__()
        self.train_repository = train_repository
        self.setWindowTitle("Train Timetable")
        self.setMinimumSize(1000, 600)
        
        self.setStyleSheet(TIMETABLE_STYLESHEET)
        
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
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Code", "Route", "Start", "Frequency", "Edit", "Delete"])
        self.table.horizontalHeader().setStretchLastSection(False)
        column_widths = [100, 400, 100, 120]
        for i, width in enumerate(column_widths):
            self.table.setColumnWidth(i, width)
        
        # Disable editing and selection
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.table.cellClicked.connect(self.handle_cell_click)
        
        self.refresh_table()
        layout.addWidget(self.table)
        
        central_widget.setLayout(layout)
    
    
    def refresh_table(self):
        trains = self.train_repository.all()
        total_rows = 0
        for train_idx, train in enumerate(trains):
            total_rows += 1
            if train_idx in self.expanded_rows:
                total_rows += len(train.stations)
        
        self.table.setRowCount(total_rows)
        
        row_idx = 0
        for train_idx, train in enumerate(trains):
            # Prepare items for columns 0-3
            items = [
                QTableWidgetItem(train.code),
                QTableWidgetItem(self._format_route(train.stations)),
                QTableWidgetItem(self._format_time(train.start_time)),
                QTableWidgetItem(f"{train.frequency} min"),
            ]

            # Set up code item color and alignment
            items[0].setBackground(self._get_code_color(train.code))
            items[0].setForeground(QColor(*BLACK))
            items[0].setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            # Route item: store train index, alignment, tooltip
            items[1].setData(Qt.ItemDataRole.UserRole, train_idx)
            items[1].setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            items[1].setToolTip("Click to expand/collapse stations")

            # Start time and frequency alignment
            items[2].setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            items[3].setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            # Set items in table
            for col, item in enumerate(items):
                self.table.setItem(row_idx, col, item)

            # Edit button
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda checked, idx=train_idx: self.edit_train(idx))
            self.table.setCellWidget(row_idx, 4, edit_btn)

            # Delete button
            delete_btn = QPushButton("Delete")
            delete_btn.setStyleSheet("background-color: RED;")
            delete_btn.clicked.connect(lambda checked, idx=train_idx: self.delete_train(idx))
            self.table.setCellWidget(row_idx, 5, delete_btn)


            # If expanded, set spans and add station rows
            if train_idx in self.expanded_rows:
                span = len(train.stations) + 1
                for col in (0, 2, 3, 4, 5):
                    self.table.setSpan(row_idx, col, span, 1)
                for i, station in enumerate(train.stations, 1):
                    self._add_station_row(row_idx + i, station)
                row_idx += span
            else:
                for col in (0, 2, 3, 4, 5):
                    self.table.setSpan(row_idx - 1, col, 1, 1)
                    
                row_idx += 1
                    

    def _add_station_row(self, row_idx: int, station: Station):
        station_item = QTableWidgetItem(f"{station.name}")
        station_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.table.setItem(row_idx, 1, station_item)
        

    def handle_cell_click(self, row, col):
        if col != 1:
            return
        item = self.table.item(row, 1)
        train_idx = item.data(Qt.ItemDataRole.UserRole)
        
        if train_idx is None: # Clicked on an expanded station row
            return
        
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
                    code=data['code'],
                    stations=station_objects,
                    start_time=data['start_time'],
                    frequency=data['frequency']
                )
                self.expanded_rows.clear()  # Clear expanded state on refresh
                self.refresh_table()

    def edit_train(self, train_idx):
        train = self.train_repository.get_by_index(train_idx)
        train_data = {
            'code': train.code,
            'stations': train.stations,
            'start_time': train.start_time,
            'frequency': train.frequency
        }
        
        dialog = TrainEditorDialog(self, train_data)
        if dialog.exec():
            data = dialog.get_data()
            if data['stations']:
                # Remove old train and add updated one
                self.train_repository.remove(train)
                station_objects = [Station(name) for name in data['stations']]
                self.train_repository.add(
                    code=data['code'],
                    stations=station_objects,
                    start_time=data['start_time'],
                    frequency=data['frequency']
                )
                self.expanded_rows.clear()  # Clear expanded state on refresh
                self.refresh_table()

    def delete_train(self, train_idx):
        train = self.train_repository.get_by_index(train_idx)
        self.train_repository.remove(train)
        self.expanded_rows.discard(train_idx)  # Remove from expanded if it was expanded
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

    def closeEvent(self, event):
        """Override closeEvent to emit signal when window is closed"""
        self.window_closed.emit()
        super().closeEvent(event)