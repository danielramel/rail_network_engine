from PyQt6.QtWidgets import (QDialog, QFormLayout, QComboBox, 
                              QTimeEdit, QSpinBox, QLabel, QDialogButtonBox,
                              QVBoxLayout, QHBoxLayout, QPushButton, QWidget,
                              QTableWidget, QTableWidgetItem, QHeaderView,
                              QMessageBox)
from PyQt6.QtCore import Qt, QTime
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtGui import QIcon, QColor, QBrush
from modules.route.stylesheets.route_editor_stylesheet import (
    TABLE_STYLE, MOVE_BUTTON_STYLE,
    ADD_BUTTON_STYLE, REMOVE_BUTTON_STYLE
)
from core.models.railway.railway_system import RailwaySystem
from core.models.route import Route
from core.config.color import Color

class RouteEditorDialog(QDialog):
    def __init__(self, parent, railway: RailwaySystem, route: Route = None):
        self.selected_row = None
        self._railway = railway
        self._editing_route = route
        super().__init__(parent)
        self._init_layout()
        
        # If editing an existing route, populate the fields
        if route is not None:
            self.set_data(route)
        
    def accept(self):
        """Override accept to validate before closing."""
        if not self.code_edit.text().strip():
            QMessageBox.warning(self, "Invalid input", "Route code cannot be empty.")
            return
        if self.code_edit.text().strip() != self._editing_route.code if self._editing_route else True:
            for existing_route in self._railway.routes.all():
                if existing_route.code == self.code_edit.text().strip():
                    QMessageBox.warning(self, "Invalid input", "Route code must be unique.")
                    return
        super().accept()

    def get_data(self) -> dict:
        """Collect route data from the dialog, ignoring arrival and departure times."""
        route_data = {
            "code": self.code_edit.text().strip(),
            "color": self.color_combo.currentText(),
            "first_train_time": self.first_train_time_edit.time().toString("HH:mm"),
            "last_train_time": self.last_train_time_edit.time().toString("HH:mm"),
            "frequency": int(self.freq_combo.currentText()),
            "stops" : [{
                    "id": self.stations_table.cellWidget(0, 1).currentData(),
                    "travel_time": None,
                    "stop_time": None
                    }
                ] + [
                    {
                    "id": self.stations_table.cellWidget(row, 1).currentData(),
                    "travel_time": (tw := self.stations_table.cellWidget(row, 2)) and tw.value() or 0,
                    "stop_time": (dw := self.stations_table.cellWidget(row, 3)) and dw.value() or 0
                    }
                    for row in range(1, self.stations_table.rowCount() - 1)
                ] + [
                    {
                    "id": self.stations_table.cellWidget(self.stations_table.rowCount() - 1, 1).currentData(),
                    "travel_time": self.stations_table.cellWidget(self.stations_table.rowCount() - 1, 2).value(),
                    "stop_time": None
                    }
                ] if self.stations_table.rowCount() > 1 else []
                    }

        return route_data

    def set_data(self, route: Route):
        """Populate the dialog fields from an existing route."""
        # Set basic fields
        self.code_edit.setText(route.code)
        color_index = self.color_combo.findText(route.color)
        if color_index >= 0:
            self.color_combo.setCurrentIndex(color_index)
        
        # Set time fields
        first_hours = route.first_train // 60
        first_mins = route.first_train % 60
        self.first_train_time_edit.setTime(QTime(first_hours, first_mins))
        
        last_hours = route.last_train // 60
        last_mins = route.last_train % 60
        self.last_train_time_edit.setTime(QTime(last_hours, last_mins))
        
        # Set frequency
        freq_index = self.freq_combo.findText(str(route.frequency))
        if freq_index >= 0:
            self.freq_combo.setCurrentIndex(freq_index)
        
        # Clear existing rows (the 2 default rows)
        while self.stations_table.rowCount() > 0:
            self.stations_table.removeRow(0)
        
        # Add rows for each stop in the route
        for i, stop in enumerate(route.stops):
            self.add_empty_station_row(i)
        for i, stop in enumerate(route.stops):
            # Set the station
            station_combo = self.stations_table.cellWidget(i, 1)
            station_index = station_combo.findData(stop['station'].id)
            if station_index >= 0:
                station_combo.setCurrentIndex(station_index)
            
            # Set travel time (skip first station)
            if i > 0 and stop.get('travel_time') is not None:
                travel_spinbox = self.stations_table.cellWidget(i, 2)
                if travel_spinbox:
                    travel_spinbox.setValue(stop['travel_time'])
            
            # Set stop time (skip last station)
            if i < len(route.stops) - 1 and stop.get('stop_time') is not None:
                stop_spinbox = self.stations_table.cellWidget(i, 3)
                if stop_spinbox:
                    stop_spinbox.setValue(stop['stop_time'])
        
        self.refresh_table()
        
    def add_row_clicked(self):
        row = self.stations_table.rowCount()-1 if self.selected_row is None else self.selected_row
        self.add_empty_station_row(row+1)
        self.refresh_table()
        
    def add_empty_station_row(self, row: int):
        """Add a new row to the stations table"""
        if row == self.stations_table.rowCount() and row > 1:
            self._set_spin_box_item(row-1, 3, 1)  # Previous stop time (column 3)
        self.stations_table.insertRow(row)
        
        # Row number indicator (column 0)
        row_num_item = QTableWidgetItem(str(row + 1))
        row_num_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        row_num_item.setFlags(row_num_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Make it read-only
        self.stations_table.setItem(row, 0, row_num_item)
        
        # Station name combobox (column 1)
        station_combo = QComboBox()
        for station in self._railway.stations.all():
            station_combo.addItem(station.name, station.id)  # store ID as userData

        self.stations_table.setCellWidget(row, 1, station_combo)
        
        self._set_spin_box_item(row, 2, 5)  # Travel time (column 2)
        self._set_spin_box_item(row, 3, 1)  # Stop time (column 3)
        self._set_empty_item(row, 4)  # Arrival time (column 4)
        self._set_empty_item(row, 5)  # Departure time (column 5)
        
    def refresh_table(self):
        row_count = self.stations_table.rowCount()
        def _set_time_item(row: int, col: int, qtime: QTime):
            self.stations_table.removeCellWidget(row, col)
            text = qtime.toString("HH:mm")
            item = QTableWidgetItem(text)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEnabled)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.stations_table.setItem(row, col, item)

        departure = self.first_train_time_edit.time()
        self._set_empty_item(0, 2)  # Travel time (column 2)
        self._set_empty_item(0, 3)  # Stop time (column 3)
        self._set_empty_item(0, 4)
        _set_time_item(0, 5, departure)

        for row in range(1, row_count):
            if row != self.selected_row:
                nr_item = self.stations_table.item(row, 0)
                nr_item.setText(str(row + 1))
                nr_item.setForeground(QBrush(Qt.GlobalColor.white))
            
            travel_min = int(self.stations_table.cellWidget(row, 2).value())

            arrival = departure.addSecs(travel_min * 60)
            _set_time_item(row, 4, arrival)
            
            if row == row_count - 1:
                self._set_empty_item(row, 3)  # Stop time (column 3)
                self._set_empty_item(row, 5)  # Departure time (column 5)
                continue
            stop_min = int(self.stations_table.cellWidget(row, 3).value())

            departure = arrival.addSecs(stop_min * 60)
            _set_time_item(row, 5, departure) 
    

    def on_cell_clicked(self, row: int, column: int):
        if column != 0:
            return
        
        if self.selected_row is not None:
            item = self.stations_table.item(self.selected_row, 0)
            item.setText(str(self.selected_row + 1))
            item.setForeground(QBrush(Qt.GlobalColor.white))
            
        # if self.stations_table.rowCount() <= 2:
        #     return  # Do not allow selecting when less than 2 rows
        if self.selected_row == row:
            self.selected_row = None
            item = self.stations_table.item(row, 0)
            item.setText(str(row + 1))
            item.setForeground(QBrush(Qt.GlobalColor.white))
            return
        self.selected_row = row
        item = self.stations_table.item(row, 0)
        item.setText("▶")
        item.setForeground(QBrush(Qt.GlobalColor.red))
        
    
    def remove_selected_row(self):
        """Remove the selected station row from the table"""
        if self.selected_row is None:
            QMessageBox.warning(self, "No selection", "Please select a station row to remove.")
            return
        
        if self.stations_table.rowCount() <= 2:
            QMessageBox.warning(self, "Cannot remove", "At least two station rows are required.")
            return  # Do not allow removing to less than 2 rows
        
        self.stations_table.removeRow(self.selected_row)
        self.selected_row = None
        for row in range(self.stations_table.rowCount()):
            self.stations_table.item(row, 0).setText(str(row + 1))
            
        self.refresh_table()
        
        
        
    # Layout and UI initialization

    def _init_layout(self):
        title = "Edit route" if self._editing_route else "Add route"
        self.setWindowTitle(title)
        self.setMinimumSize(600, 800)
        
        layout = QFormLayout()
        
        # Code and Color on same row
        self.code_edit = QLineEdit()
        self.code_edit.setPlaceholderText("Enter route code")
        self.color_combo = self._create_combo_box(Color.all())
        
        code_color_layout = QHBoxLayout()
        code_color_layout.addWidget(self.code_edit)
        code_color_layout.addWidget(self.color_combo)
        layout.addRow("Code / Color:", code_color_layout)
        
        # First train, Last train, Frequency on same row with separate label for frequency
        self.first_train_time_edit = self._create_time_edit()
        self.last_train_time_edit = self._create_time_edit()
        self.freq_combo = self._create_combo_box((5, 10, 15, 20, 30, 60, 90, 120))
        
        train_layout = QHBoxLayout()
        train_layout.addWidget(QLabel("First Train:"))
        train_layout.addWidget(self.first_train_time_edit)
        train_layout.addWidget(QLabel("Last Train:"))
        train_layout.addWidget(self.last_train_time_edit)
        train_layout.addWidget(QLabel("Frequency:"))
        train_layout.addWidget(self.freq_combo)
        layout.addRow(train_layout)
        
        self.setLayout(layout)
        
        # Station selection section
        stations_widget = QWidget()
        stations_layout = QVBoxLayout()
        
        self.stations_table = self._create_stations_table()
        stations_layout.addWidget(self.stations_table)
        
        # Control buttons layout (single row with icons)
        control_layout = QHBoxLayout()
        control_layout.addStretch()
        
        self.add_row_button = self._create_push_button("＋", "Add station row below", ADD_BUTTON_STYLE, self.add_row_clicked)
        control_layout.addWidget(self.add_row_button)
        
        self.remove_button = self._create_push_button(QIcon.fromTheme("edit-delete"), "Remove selected station", REMOVE_BUTTON_STYLE, self.remove_selected_row)
        control_layout.addWidget(self.remove_button)
        
        control_layout.addStretch()
        stations_layout.addLayout(control_layout)
        
        stations_widget.setLayout(stations_layout)
        layout.addRow(stations_widget)
        
        self.setLayout(layout)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        layout.addRow(buttons)

        self.add_empty_station_row(0)
        self._set_empty_item(0, 2)  # Travel time (column 2)
        self._set_empty_item(0, 3)  # Stop time (column 3)
        self._set_empty_item(0, 4)  # Arrival time (column 4)
        self._set_empty_item(0, 5)  # Departure time (column 5)
        self.add_empty_station_row(1)
        self.refresh_table()

    def _set_empty_item(self, row, col):
        # Create new because reusing the same QTableWidgetItem causes ownership issues
        self.stations_table.removeCellWidget(row, col)
        item = QTableWidgetItem("")
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEnabled)
        self.stations_table.setItem(row, col, item)
        
        
    def _create_stations_table(self):
        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(["#", "Station", "Travel time", "Stop time", "Arrival Time", "Departure Time"])
        table.verticalHeader().setVisible(False)
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(0, 40)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        for col in range(2, 6):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
        table.verticalHeader().setDefaultSectionSize(50)
        table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        table.setFocusPolicy(Qt.FocusPolicy.WheelFocus)
        table.cellClicked.connect(self.on_cell_clicked)
        table.setStyleSheet(TABLE_STYLE)
        return table
    
    def _set_spin_box_item(self, row, col, default_value: int = 0):
        self.stations_table.removeCellWidget(row, col)
        spin_box = QSpinBox()
        spin_box.setMinimum(0)
        spin_box.setMaximum(999)
        spin_box.setValue(default_value)
        spin_box.valueChanged.connect(self.refresh_table)
        self.stations_table.setCellWidget(row, col, spin_box)
    
    def _create_time_edit(self):
        time_edit = QTimeEdit()
        time_edit.setDisplayFormat("HH:mm")
        time_edit.setTime(QTime(6, 0))
        time_edit.timeChanged.connect(self.refresh_table)
        return time_edit
    
    def _create_combo_box(self, items: list[object]) -> QComboBox:
        combo = QComboBox()
        combo.addItems([str(item) for item in items])
        return combo
    
    def _create_push_button(self, icon_or_text, tooltip: str, style: str, callback) -> QPushButton:
        if isinstance(icon_or_text, QIcon):
            button = QPushButton()
            button.setIcon(icon_or_text)
        else:
            button = QPushButton(icon_or_text)
        button.setStyleSheet(style)
        button.setToolTip(tooltip)
        button.setAutoDefault(False)
        button.clicked.connect(callback)
        return button