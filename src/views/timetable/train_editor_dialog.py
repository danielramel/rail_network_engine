from PyQt6.QtWidgets import (QDialog, QFormLayout, QComboBox, 
                              QTimeEdit, QListWidget, QLabel, QDialogButtonBox,
                              QVBoxLayout, QHBoxLayout, QPushButton, QWidget,
                              QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt, QTime
from models.train import Train
from PyQt6.QtWidgets import QLineEdit
from views.timetable.train_editor_stylesheet import (
    TABLE_STYLE, MOVE_UP_BUTTON_STYLE, MOVE_DOWN_BUTTON_STYLE,
    ADD_BUTTON_STYLE, REMOVE_BUTTON_STYLE
)
from PyQt6.QtGui import QBrush

class TrainEditorDialog(QDialog):
    def __init__(self, parent, stations: list[str], train_to_edit: Train = None):
        self.train_to_edit = train_to_edit
        self.available_stations = stations
        self.selected_row = None  # Custom selection tracking
        super().__init__(parent)
        self.setWindowTitle("Add Train" if train_to_edit is None else "Edit Train")
        self.setMinimumWidth(750)
        self.setMinimumHeight(700)
        
        layout = QFormLayout()
        
        self.code_edit = QLineEdit()
        self.code_edit.setPlaceholderText("Enter train code")
        layout.addRow("Train code:", self.code_edit)
        
        self.first_train_time_edit = QTimeEdit()
        self.first_train_time_edit.setDisplayFormat("HH:mm")
        self.first_train_time_edit.setTime(QTime(6, 0))
        layout.addRow("First Train:", self.first_train_time_edit)
        
        self.last_train_time_edit = QTimeEdit()
        self.last_train_time_edit.setDisplayFormat("HH:mm")
        self.last_train_time_edit.setTime(QTime(22, 0))
        layout.addRow("Last Train:", self.last_train_time_edit)
        
        self.freq_combo = QComboBox()
        self.freq_combo.setEditable(True)
        self.freq_combo.addItems([str(item) for item in [10, 15, 20, 30, 60, 120, 180, 240]])
        layout.addRow("Frequency (minutes):", self.freq_combo)
        
        # Station selection section
        stations_widget = QWidget()
        stations_layout = QVBoxLayout()
        
        self.stations_table = QTableWidget()
        self.stations_table.setColumnCount(4)  # Added one column for selection indicator
        self.stations_table.setHorizontalHeaderLabels(["#", "Station", "Arrival Time", "Departure Time"])
        
        # Hide the default vertical header
        self.stations_table.verticalHeader().setVisible(False)
        
        # Set column resize modes
        self.stations_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.stations_table.horizontalHeader().resizeSection(0, 40)  # Width for row number (supports 2-digit numbers)
        self.stations_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.stations_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.stations_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.stations_table.verticalHeader().setDefaultSectionSize(50)  # Set row height
        
        # Disable built-in selection
        self.stations_table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        
        # Enable scrolling without requiring focus
        self.stations_table.setFocusPolicy(Qt.FocusPolicy.WheelFocus)
        
        # Connect click event for custom selection
        self.stations_table.cellClicked.connect(self.on_cell_clicked)
        
        self.stations_table.setStyleSheet(TABLE_STYLE)
        stations_layout.addWidget(self.stations_table)
        
        # Control buttons layout (single row with icons)
        control_layout = QHBoxLayout()
        control_layout.addStretch()
        
        # Blue Up button
        self.move_up_button = QPushButton("↑")
        self.move_up_button.setStyleSheet(MOVE_UP_BUTTON_STYLE)
        self.move_up_button.setToolTip("Move selected station up")
        self.move_up_button.clicked.connect(self.move_selected_up)
        control_layout.addWidget(self.move_up_button)
        
        # Blue Down button
        self.move_down_button = QPushButton("↓")
        self.move_down_button.setStyleSheet(MOVE_DOWN_BUTTON_STYLE)
        self.move_down_button.setToolTip("Move selected station down")
        self.move_down_button.clicked.connect(self.move_selected_down)
        control_layout.addWidget(self.move_down_button)
        
        
        control_layout.addSpacing(10)
        
        # Green Add button
        self.add_row_button = QPushButton("＋")
        self.add_row_button.setStyleSheet(ADD_BUTTON_STYLE)
        self.add_row_button.setToolTip("Add station")
        self.add_row_button.clicked.connect(self.add_station_row)
        control_layout.addWidget(self.add_row_button)
                
        # Red Delete button
        self.remove_button = QPushButton("✕")
        self.remove_button.setStyleSheet(REMOVE_BUTTON_STYLE)
        self.remove_button.setToolTip("Remove selected station")
        self.remove_button.clicked.connect(self.remove_selected_station)
        control_layout.addWidget(self.remove_button)
        
        control_layout.addStretch()
        stations_layout.addLayout(control_layout)
        
        stations_widget.setLayout(stations_layout)
        layout.addRow(stations_widget)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        
        # Load existing train data if editing
        if train_to_edit:
            self.code_edit.setText(train_to_edit.code)
            self.first_train_time_edit.setTime(QTime(train_to_edit.start_time // 60, train_to_edit.start_time % 60))
            self.freq_combo.setCurrentText(f"{train_to_edit.frequency}")
            
            # Set end time if available
            if hasattr(train_to_edit, 'end_time'):
                self.last_train_time_edit.setTime(QTime(train_to_edit.end_time // 60, train_to_edit.end_time % 60))
            
            # Add stations with their times
            for station in train_to_edit.stations:
                self.add_station_row(station.name, station.arrival_time, station.departure_time)
        else:
            # Add one empty row by default
            self.add_station_row()
    
        self.setLayout(layout)
    
    def add_station_row(self, station_name: str = None, arrival_minutes: int = None, departure_minutes: int = None):
        """Add a new row to the stations table"""
        row = self.stations_table.rowCount()
        self.stations_table.insertRow(row)
        
        # Row number indicator (column 0)
        row_num_item = QTableWidgetItem(str(row + 1))
        row_num_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        row_num_item.setFlags(row_num_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Make it read-only
        self.stations_table.setItem(row, 0, row_num_item)
        
        # Station name combobox (column 1)
        station_combo = QComboBox()
        station_combo.addItems(self.available_stations)
        if station_name:
            station_combo.setCurrentText(station_name)
        self.stations_table.setCellWidget(row, 1, station_combo)
        
        # Arrival time (column 2)
        arrival_time_edit = QTimeEdit()
        arrival_time_edit.setDisplayFormat("HH:mm")
        if arrival_minutes is not None:
            arrival_time_edit.setTime(QTime(arrival_minutes // 60, arrival_minutes % 60))
        else:
            arrival_time_edit.setTime(QTime(6, 0))
        self.stations_table.setCellWidget(row, 2, arrival_time_edit)
        
        # Departure time (column 3)
        departure_time_edit = QTimeEdit()
        departure_time_edit.setDisplayFormat("HH:mm")
        if departure_minutes is not None:
            departure_time_edit.setTime(QTime(departure_minutes // 60, departure_minutes % 60))
        else:
            departure_time_edit.setTime(QTime(6, 5))
        self.stations_table.setCellWidget(row, 3, departure_time_edit)
        
    def on_cell_clicked(self, row: int, column: int):
        if column != 0:
            return
        self.select_row(row)

    def select_row(self, row: int):
        """Manually select a row with custom styling"""
        # Clear previous selection
        if self.selected_row is not None:
            item = self.stations_table.item(self.selected_row, 0)
            item.setText(str(self.selected_row + 1))
            item.setForeground(QBrush(Qt.GlobalColor.white))

        # Set new selection
        self.selected_row = row
        item = self.stations_table.item(row, 0)
        item.setText("▶")
        item.setForeground(QBrush(Qt.GlobalColor.red))
        

    def move_selected_up(self):
        """Move the selected row up one position"""
        if self.selected_row is not None and self.selected_row > 0:
            self.swap_rows(self.selected_row, self.selected_row - 1)
    
    def move_selected_down(self):
        """Move the selected row down one position"""
        if self.selected_row is not None and self.selected_row < self.stations_table.rowCount() - 1:
            self.swap_rows(self.selected_row, self.selected_row + 1)

    
    def swap_rows(self, row1: int, row2: int):
        def get_row_data(row: int):
            station_combo = self.stations_table.cellWidget(row, 1)  # Column 1 for station
            arrival_time_widget = self.stations_table.cellWidget(row, 2)  # Column 2 for arrival
            departure_time_widget = self.stations_table.cellWidget(row, 3)  # Column 3 for departure
            
            return {
                'station': station_combo.currentText(),
                'arrival': arrival_time_widget.time(),
                'departure': departure_time_widget.time()
            }
            
        def set_row_data(row: int, data: dict):
            station_combo = self.stations_table.cellWidget(row, 1)  # Column 1 for station
            arrival_time_widget = self.stations_table.cellWidget(row, 2)  # Column 2 for arrival
            departure_time_widget = self.stations_table.cellWidget(row, 3)  # Column 3 for departure
            
            station_combo.setCurrentText(data['station'])
            arrival_time_widget.setTime(data['arrival'])
            departure_time_widget.setTime(data['departure'])

        
        data1 = get_row_data(row1)
        data2 = get_row_data(row2)
        
        set_row_data(row1, data2)
        set_row_data(row2, data1)

        # Update custom selection
        self.select_row(row2)
        
    
    def remove_selected_station(self):
        """Remove the selected station row from the table"""
        if self.selected_row is not None and self.selected_row >= 0:
            self.stations_table.removeRow(self.selected_row)
            # Clear the selection since the row is removed
            self.selected_row = None
            # Renumber all rows
            for row in range(self.stations_table.rowCount()):
                self.stations_table.item(row, 0).setText(str(row + 1))
    
    def get_data(self):
        """Extract all train data from the dialog"""
        stations_data = []
        for row in range(self.stations_table.rowCount()):
            station_combo = self.stations_table.cellWidget(row, 1)  # Column 1 for station
            arrival_time_widget = self.stations_table.cellWidget(row, 2)  # Column 2 for arrival
            departure_time_widget = self.stations_table.cellWidget(row, 3)  # Column 3 for departure
            
            station_name = station_combo.currentText()
            arrival_time = arrival_time_widget.time()
            departure_time = departure_time_widget.time()
            
            stations_data.append({
                'name': station_name,
                'arrival_time': arrival_time.hour() * 60 + arrival_time.minute(),
                'departure_time': departure_time.hour() * 60 + departure_time.minute()
            })
        
        time = self.first_train_time_edit.time()
        start_time_minutes = time.hour() * 60 + time.minute()
        
        end_time = self.last_train_time_edit.time()
        end_time_minutes = end_time.hour() * 60 + end_time.minute()
        
        frequency = int(self.freq_combo.currentText())
        
        return {
            'code': self.code_edit.text(),
            'stations': stations_data,
            'start_time': start_time_minutes,
            'end_time': end_time_minutes,
            'frequency': frequency
        }