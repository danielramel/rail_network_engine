from PyQt6.QtWidgets import (QDialog, QFormLayout, QComboBox, 
                              QTimeEdit, QListWidget, QLabel, QDialogButtonBox)
from PyQt6.QtCore import Qt, QTime
from models.station import Station
from models.train import Train


class TrainEditorDialog(QDialog):
    def __init__(self, parent, train_to_edit: Train = None):
        super().__init__(parent)
        self.setWindowTitle("Add Train" if train_to_edit is None else "Edit Train")
        self.setMinimumWidth(500)
        self.setMinimumHeight(600)
        
        layout = QFormLayout()
        
        # Train code (editable so user can enter any value)
        self.code_combo = QComboBox() #todo something else here?
        self.code_combo.setEditable(True)
        # Show a hint in the editable line
        if self.code_combo.lineEdit() is not None:
            self.code_combo.lineEdit().setPlaceholderText("Enter train code")
        layout.addRow("Train code:", self.code_combo)
        
        # Start Time
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setTime(QTime(6, 0))
        layout.addRow("Start Time:", self.time_edit)
        
        # Frequency
        self.freq_combo = QComboBox()
        self.freq_combo.setEditable(True)
        items = ['10 min', '15 min', '20 min', '30 min', '60 min', '120 min', '180 min', '240 min']
        self.freq_combo.addItems(items)
        if self.freq_combo.lineEdit() is not None:
            self.freq_combo.lineEdit().setPlaceholderText("Enter frequency")
        layout.addRow("Frequency:", self.freq_combo)
        
        # Stations
        stations_label = QLabel("Stations (select in order, use Ctrl+Click):")
        layout.addRow(stations_label)
        
        self.station_list = QListWidget()
        self.station_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.station_list.addItems(map(lambda s: s.name, parent._map.stations))
        layout.addRow(self.station_list)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        
        # Load existing data if editing
        if train_to_edit:
            self.code_combo.setCurrentText(train_to_edit.code)
            # Convert minutes to QTime
            hours = train_to_edit.start_time // 60
            minutes = train_to_edit.start_time % 60
            self.time_edit.setTime(QTime(hours, minutes))
            self.freq_combo.setCurrentText(f"{train_to_edit.frequency} min")
            # Select stations in the list
            for station in train_to_edit.stations:
                station_name = station.name if isinstance(station, Station) else station
                items = self.station_list.findItems(station_name, Qt.MatchFlag.MatchExactly)
                if items:
                    items[0].setSelected(True)
        
        self.setLayout(layout)
    
    def get_data(self):
        selected_stations = [item.text() for item in self.station_list.selectedItems()]
        time = self.time_edit.time()
        start_time_minutes = time.hour() * 60 + time.minute()
        # Extract just the number from frequency string (e.g., "20 min" -> 20)
        frequency = int(self.freq_combo.currentText().split()[0])
        
        return {
            'code': self.code_combo.currentText(),
            'stations': selected_stations,
            'start_time': start_time_minutes,
            'frequency': frequency
        }