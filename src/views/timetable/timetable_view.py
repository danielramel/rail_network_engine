from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                              QTableWidget, QTableWidgetItem, 
                              QPushButton, QDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from config.colors import BLACK, LIGHTBLUE, RED, YELLOW
from models.station import Station
from models.train import Train, TrainRepository
from views.timetable.train_editor_dialog import TrainEditorDialog
from views.timetable.timetable_stylesheet import TIMETABLE_STYLESHEET
from PyQt6.QtCore import pyqtSignal
from domain.rail_map import RailMap

class TimetableWindow(QMainWindow):
    window_closed = pyqtSignal()
    def __init__(self, map: RailMap):
        super().__init__()
        self._map = map
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
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(["Code", "Station", "Arrival", "Departure", "First Train", "Last Train", "Frequency", "Edit", "Delete"])
        self.table.horizontalHeader().setStretchLastSection(False)
        # Station, Arrival, Departure together = 390 (was Route column width)
        column_widths = [80, 200, 95, 95, 90, 90, 100, 60, 60]
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
        trains = self._map.train_repository.all()
        total_rows = 0
        for train_idx, train in enumerate(trains):
            total_rows += 1
            if train_idx in self.expanded_rows:
                total_rows += len(train.schedule)
        
        self.table.setRowCount(total_rows)
        self.table.clearSpans()
        
        row_idx = 0
        for train_idx, train in enumerate(trains):
            # Prepare items for columns 0-6
            items = [
                QTableWidgetItem(train.code),
                QTableWidgetItem(self._format_route(train.schedule, train_idx in self.expanded_rows)),
                QTableWidgetItem(""),  # Arrival - empty for main row
                QTableWidgetItem(""),  # Departure - empty for main row
                QTableWidgetItem(self._format_time(train.first_train)),
                QTableWidgetItem(self._format_time(train.last_train)),
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

            # Time and frequency alignment
            items[2].setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            items[3].setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            items[4].setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            items[5].setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            items[6].setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            # Set items in table
            for col, item in enumerate(items):
                self.table.setItem(row_idx, col, item)

            self.table.setSpan(row_idx, 1, 1, 3)

            # Edit button
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda checked, idx=train_idx: self.edit_train(idx))
            self.table.setCellWidget(row_idx, 7, edit_btn)

            # Delete button
            delete_btn = QPushButton("Delete")
            delete_btn.setStyleSheet("background-color: RED;")
            delete_btn.clicked.connect(lambda checked, idx=train_idx: self.delete_train(idx))
            self.table.setCellWidget(row_idx, 8, delete_btn)


            # If expanded, set spans and add station rows
            if train_idx in self.expanded_rows:
                span = len(train.schedule) + 1
                for col in (0, 4, 5, 6, 7, 8):
                    self.table.setSpan(row_idx, col, span, 1)
                for i, station in enumerate(train.schedule, 1):
                    arrival_time = self._format_time(station['arrival_time'])
                    departure_time = self._format_time(station['departure_time'])
                    
                    # Station name
                    station_item = QTableWidgetItem(station['station'].name)
                    station_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                    self.table.setItem(row_idx + i, 1, station_item)
                    
                    # Arrival time
                    arrival_item = QTableWidgetItem(arrival_time)
                    arrival_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.table.setItem(row_idx + i, 2, arrival_item)
                    
                    # Departure time
                    departure_item = QTableWidgetItem(departure_time)
                    departure_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.table.setItem(row_idx + i, 3, departure_item)
                row_idx += span
            else:
                row_idx += 1
        

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
        dialog = TrainEditorDialog(self, self._map)
        res = dialog.exec()
        if res == QDialog.DialogCode.Rejected:
            return
        
        data = dialog.get_data()

        train = Train(code=data['code'], schedule=data['schedule'], first_train=data['first_train'], last_train=data['last_train'], frequency=data['frequency'])
        self._map.train_repository.add(train)
        # self.expanded_rows.clear()  # Clear expanded state on refresh
        self.refresh_table()

    def edit_train(self, train_idx):
        train = self._map.train_repository.get(train_idx)

        dialog = TrainEditorDialog(self, self._map, train)
        res = dialog.exec()
        if res == QDialog.DialogCode.Rejected:
            return
        data = dialog.get_data()
    
        # Remove old train and add updated one
        self._map.train_repository.remove(train)
        
        updated_train = Train(
            code=data['code'],
            schedule=data['schedule'],
            first_train=data['first_train'],
            last_train=data['last_train'],
            frequency=data['frequency']
        )
        self._map.train_repository.add(updated_train)
        # self.expanded_rows.clear()  # Clear expanded state on refresh
        self.refresh_table()

    def delete_train(self, train_idx):
        train = self._map.train_repository.get(train_idx)
        self._map.train_repository.remove(train)
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

    def _format_route(self, schedule: list[dict[str, Station | int]], is_expanded: bool = False) -> str:
        if not len(schedule):
            return "No stations"
        elif len(schedule) == 1:
            station_name = schedule[0]['station'].name
            if is_expanded:
                return station_name
            dep_time = self._format_time(schedule[0]['departure_time'])
            return f"{station_name} (dep: {dep_time})"
        elif len(schedule) == 2:
            first_station = schedule[0]['station'].name
            last_station = schedule[1]['station'].name
            if is_expanded:
                return f"{first_station} → {last_station}"
            first_dep = self._format_time(schedule[0]['departure_time'])
            last_arr = self._format_time(schedule[1]['arrival_time'])
            return f"{first_station} ({first_dep}) → {last_station} ({last_arr})"
        else:
            first_station = schedule[0]['station'].name
            last_station = schedule[-1]['station'].name
            if is_expanded:
                return f"{first_station} → ... → {last_station}"
            first_dep = self._format_time(schedule[0]['departure_time'])
            last_arr = self._format_time(schedule[-1]['arrival_time'])
            return f"{first_station} ({first_dep}) → ... → {last_station} ({last_arr})"

    def closeEvent(self, event):
        """Override closeEvent to emit signal when window is closed"""
        self.window_closed.emit()
        super().closeEvent(event)