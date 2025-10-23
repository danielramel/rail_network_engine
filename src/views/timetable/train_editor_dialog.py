from PyQt6.QtWidgets import (QDialog, QFormLayout, QComboBox, 
                              QTimeEdit, QListWidget, QLabel, QDialogButtonBox,
                              QVBoxLayout, QHBoxLayout, QPushButton, QWidget,
                              QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt, QTime
from domain.rail_map import RailMap
from models.train import Train
from PyQt6.QtWidgets import QLineEdit
from views.timetable.train_editor_stylesheet import (
    TABLE_STYLE, MOVE_UP_BUTTON_STYLE, MOVE_DOWN_BUTTON_STYLE,
    ADD_BUTTON_STYLE, REMOVE_BUTTON_STYLE
)
from PyQt6.QtGui import QBrush

class TrainEditorDialog(QDialog):
    def __init__(self, parent, map: RailMap, train_to_edit: Train = None):
        self.train_to_edit = train_to_edit
        self.selected_row = None  # Custom selection tracking
        self._map = map
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
        self.last_train_time_edit.setTime(QTime(6, 0))
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
        self.move_up_button.setAutoDefault(False)
        self.move_up_button.clicked.connect(self.move_selected_up)
        control_layout.addWidget(self.move_up_button)
        
        # Blue Down button
        self.move_down_button = QPushButton("↓")
        self.move_down_button.setStyleSheet(MOVE_DOWN_BUTTON_STYLE)
        self.move_down_button.setToolTip("Move selected station down")
        self.move_down_button.setAutoDefault(False)
        self.move_down_button.clicked.connect(self.move_selected_down)
        control_layout.addWidget(self.move_down_button)
        
        
        control_layout.addSpacing(10)
        
        # Green Add button
        self.add_row_button = QPushButton("＋")
        self.add_row_button.setStyleSheet(ADD_BUTTON_STYLE)
        self.add_row_button.setToolTip("Add station")
        self.add_row_button.setAutoDefault(False)
        self.add_row_button.clicked.connect(self.add_empty_station_row)
        control_layout.addWidget(self.add_row_button)
                
        # Red Delete button
        self.remove_button = QPushButton("✕")
        self.remove_button.setStyleSheet(REMOVE_BUTTON_STYLE)
        self.remove_button.setToolTip("Remove selected station")
        self.remove_button.setAutoDefault(False)
        self.remove_button.clicked.connect(self.remove_selected_station)
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
        
        # Load existing train data if editing
        if train_to_edit:
            self.code_edit.setText(train_to_edit.code)
            self.first_train_time_edit.setTime(QTime.fromMSecsSinceStartOfDay(train_to_edit.first_train * 60 * 1000))
            self.freq_combo.setCurrentText(f"{train_to_edit.frequency}")
            
            # Set last train time
            self.last_train_time_edit.setTime(QTime.fromMSecsSinceStartOfDay(train_to_edit.last_train * 60 * 1000))

            self.add_station_rows_from_schedule(train_to_edit.schedule)
        else:
            # Add two empty rows by default for new trains
            self.add_empty_station_row()
            # self.add_station_row()
            
    def add_station_rows_from_schedule(self, schedule: list[dict]):
        """Populate the stations table from an existing schedule"""
        for _ in range(len(schedule)):
            self.add_empty_station_row()
            
        for row, entry in enumerate(schedule):
            station_combo = self.stations_table.cellWidget(row, 1)
            station_combo.setCurrentText(entry['station'].name)
            
            arrival_edit = self.stations_table.item(row, 2)
            if row != 0:
                arrival_edit.setTime(QTime.fromMSecsSinceStartOfDay(entry['arrival_time'] * 60 * 1000))
            if row != len(schedule) - 1:
                departure_edit = self.stations_table.item(row, 3)
                departure_edit.setTime(QTime.fromMSecsSinceStartOfDay(entry['departure_time'] * 60 * 1000))
    
    
    def add_empty_station_row(self, station_info : dict = None):
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
        station_combo.addItems(station.name for station in self._map.stations)
        if station_info:
            station_combo.setCurrentText(station_info['station'].name)
        self.stations_table.setCellWidget(row, 1, station_combo)
    
        
        self.update_first_last_station_cells()

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
            station_text = self.stations_table.cellWidget(row, 1).currentText()
            arrival_widget = self.stations_table.cellWidget(row, 2)
            arrival_time = arrival_widget.time() if arrival_widget else None

            departure_widget = self.stations_table.cellWidget(row, 3)
            departure_time = departure_widget.time() if departure_widget else None

            return (station_text, arrival_time, departure_time)

        def set_row_data(row: int, data):
            self.stations_table.cellWidget(row, 1).setCurrentText(data[0])
            self.stations_table.setCellWidget(row, 2, self.new_time_table_widget(data[1] if data[1] else data[2].addSecs(-60)))
            self.stations_table.setCellWidget(row, 3, self.new_time_table_widget(data[2] if data[2] else data[1].addSecs(60)))

        
        data1 = get_row_data(row1)
        data2 = get_row_data(row2)
        
        set_row_data(row1, data2)
        set_row_data(row2, data1)

        # Update custom selection
        self.select_row(row2)
        
        self.update_first_last_station_cells()
        
    
    def remove_selected_station(self):
        """Remove the selected station row from the table"""
        if self.selected_row is not None and self.selected_row >= 0:
            self.stations_table.removeRow(self.selected_row)
            # Clear the selection since the row is removed
            self.selected_row = None
            # Renumber all rows
            for row in range(self.stations_table.rowCount()):
                self.stations_table.item(row, 0).setText(str(row + 1))
            
            # Update first/last station cells after removal
            self.update_first_last_station_cells()
    
    def get_data(self):
        """Extract all train data from the dialog"""
        schedule = []
        row_count = self.stations_table.rowCount()
        
        for row in range(row_count):
            station_name = self.stations_table.cellWidget(row, 1).currentText()
            arrival_time_widget = self.stations_table.cellWidget(row, 2)
            departure_time_widget = self.stations_table.cellWidget(row, 3)
            
            # First station has no arrival time
            if row == 0:
                arrival_minutes = None
            else:
                arrival_time = arrival_time_widget.time()
                arrival_minutes = arrival_time.hour() * 60 + arrival_time.minute()
            
            # Last station has no departure time
            if row == row_count - 1:
                departure_minutes = None
            else:
                departure_time = departure_time_widget.time()
                departure_minutes = departure_time.hour() * 60 + departure_time.minute()

            schedule.append({
                'station': self._map.get_station_by_name(station_name),
                'arrival_time': arrival_minutes,
                'departure_time': departure_minutes
            })
        
        time = self.first_train_time_edit.time()
        first_train_minutes = time.hour() * 60 + time.minute()
        
        last_train = self.last_train_time_edit.time()
        last_train_minutes = last_train.hour() * 60 + last_train.minute()
        
        frequency = int(self.freq_combo.currentText())
        
        return {
            'code': self.code_edit.text(),
            'schedule': schedule,
            'first_train': first_train_minutes,
            'last_train': last_train_minutes,
            'frequency': frequency
        }
        
        
    def update_first_last_station_cells(self):
        """Update cells so first station has no arrival time and last station has no departure time"""
        
        row_count = self.stations_table.rowCount()
        if row_count == 0:
            return

        if row_count == 1:
            self.stations_table.setItem(0, 2, self.new_empty_table_widget())
            self.stations_table.setItem(0, 3, self.new_empty_table_widget())
            return
            
        
        # first row - remove arrival widget, make it empty
        self.stations_table.removeCellWidget(0, 2)
        self.stations_table.setItem(0, 2, self.new_empty_table_widget())
        
        # first row - ensure departure widget exists
        if self.stations_table.cellWidget(0, 3) is None:
            self.stations_table.setCellWidget(0, 3, self.new_time_table_widget(QTime(6, 0)))

        # second row
        if self.stations_table.cellWidget(1, 2) is None:
            arrival_time = self.stations_table.cellWidget(0, 3).time().addSecs(5*60)
            self.stations_table.setCellWidget(1, 2, self.new_time_table_widget(arrival_time))
        
        # second last row
        row = row_count - 2
        if self.stations_table.cellWidget(row, 3) is None:
            departure_time = self.stations_table.cellWidget(row, 2).time().addSecs(60)
            self.stations_table.setCellWidget(row, 3, self.new_time_table_widget(departure_time))

        # last row - remove departure widget, make it empty
        row = row_count - 1
        self.stations_table.removeCellWidget(row, 3)
        self.stations_table.setItem(row, 3, self.new_empty_table_widget())
        if self.stations_table.cellWidget(row, 2) is None:
            arrival_time = self.stations_table.cellWidget(row-1, 3).time().addSecs(5*60)
            self.stations_table.setCellWidget(row, 2, self.new_time_table_widget(arrival_time))

    @staticmethod
    def new_empty_table_widget():
        # Create new because reusing the same QTableWidgetItem causes ownership issues
        item = QTableWidgetItem("")
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEnabled)
        return item
    
    @staticmethod
    def new_time_table_widget(time: QTime):
        time_widget = QTimeEdit()
        time_widget.setDisplayFormat("HH:mm")
        time_widget.setTime(time)
        return time_widget