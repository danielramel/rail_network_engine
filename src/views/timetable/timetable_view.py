from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QTableWidget, QTableWidgetItem, 
                              QPushButton, QDialog, QFormLayout, QComboBox, 
                              QTimeEdit, QListWidget, QLabel, QDialogButtonBox,
                              QMenu)
from PyQt6.QtCore import Qt, QTime, QPoint
from PyQt6.QtGui import QColor, QCursor
from models.station import Station
from models.train import TrainRepository


class AddTrainDialog(QDialog):
    def __init__(self, parent=None, train_data=None):
        super().__init__(parent)
        self.setWindowTitle("Add Train" if train_data is None else "Edit Train")
        self.setMinimumWidth(500)
        self.setMinimumHeight(600)
        
        layout = QFormLayout()
        
        # Train Type
        self.type_combo = QComboBox()
        self.type_combo.addItems(["S70", "S71", "Z72"])
        layout.addRow("Train Type:", self.type_combo)
        
        # Start Time
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setTime(QTime(6, 0))
        layout.addRow("Start Time:", self.time_edit)
        
        # Frequency
        self.freq_combo = QComboBox()
        self.freq_combo.addItems(["10 min", "15 min", "20 min", "30 min", "60 min"])
        layout.addRow("Frequency:", self.freq_combo)
        
        # Stations
        stations_label = QLabel("Stations (select in order, use Ctrl+Click):")
        layout.addRow(stations_label)
        
        self.station_list = QListWidget()
        self.station_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        available_stations = [
            "Hauptbahnhof", "Stadtmitte", "Ostbahnhof", "Flughafen",
            "Messegelände", "Nordstadt", "Zentrum", "Marktplatz",
            "Südbahnhof", "Westend", "Universitätsplatz", "Endstation Ost",
            "Bahnhof Nord", "Altstadt", "Industriegebiet", "Parkstraße",
            "Schillerplatz", "Goethestraße", "Kantplatz", "Mozartweg",
            "Beethovenallee", "Bachstraße", "Händelplatz", "Schubertallee"
        ]
        self.station_list.addItems(available_stations)
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
        if train_data:
            self.type_combo.setCurrentText(train_data['type'])
            # Convert minutes to QTime
            hours = train_data['start_time'] // 60
            minutes = train_data['start_time'] % 60
            self.time_edit.setTime(QTime(hours, minutes))
            self.freq_combo.setCurrentText(f"{train_data['frequency']} min")
            # Select stations in the list
            for station in train_data['stations']:
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
            'type': self.type_combo.currentText(),
            'stations': selected_stations,
            'start_time': start_time_minutes,
            'frequency': frequency
        }


class TimetableWindow(QMainWindow):
    def __init__(self, train_repository: TrainRepository):
        super().__init__()
        self.train_repo = train_repository
        self.setWindowTitle("Train Timetable")
        self.setMinimumSize(1000, 600)
        
        # Set dark theme
        self.setStyleSheet("""
            QMainWindow { background-color: #1a1a1a; }
            QTableWidget { 
                background-color: #2d2d2d; 
                color: #e0e0e0;
                gridline-color: #404040;
                border: none;
            }
            QTableWidget::item { 
                padding: 10px;
            }
            QTableWidget::item:hover {
                background-color: #3d3d3d;
            }
            QHeaderView::section { 
                background-color: #404040; 
                color: white; 
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QPushButton {
                background-color: #0066cc;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #0052a3; }
            QMenu {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #404040;
            }
            QMenu::item {
                padding: 8px 20px;
            }
            QMenu::item:selected {
                background-color: #0066cc;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # Add button
        add_btn = QPushButton("+ Add Train")
        add_btn.clicked.connect(self.add_train)
        layout.addWidget(add_btn, alignment=Qt.AlignmentFlag.AlignRight)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Type", "Route", "Start", "Frequency", "Edit", "Delete"])
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 400)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 120)
        
        # Connect cell click event
        self.table.cellClicked.connect(self.handle_cell_click)
        
        self.refresh_table()
        layout.addWidget(self.table)
        
        central_widget.setLayout(layout)
    
    def _format_time(self, minutes: int) -> str:
        """Convert minutes since midnight to HH:mm string."""
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours:02d}:{mins:02d}"
    
    def refresh_table(self):
        trains = self.train_repo.all()
        self.table.setRowCount(len(trains))
        
        type_colors = {
            "S70": QColor(100, 150, 255),
            "S71": QColor(255, 150, 100),
            "Z72": QColor(150, 255, 150)
        }
        
        for row, train in enumerate(trains):
            # Type
            type_item = QTableWidgetItem(train.code)
            type_item.setBackground(type_colors.get(train.code, QColor(200, 200, 200)))
            type_item.setForeground(QColor(0, 0, 0))
            type_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 0, type_item)
            
            # Route - only show first and last station
            if train.stations:
                first = train.stations[0].name
                last = train.stations[-1].name
                route = f"{first} → ... → {last}"
            else:
                route = "No stations"
            route_item = QTableWidgetItem(route)
            route_item.setData(Qt.ItemDataRole.UserRole, row)
            self.table.setItem(row, 1, route_item)
            
            # Start time
            time_str = self._format_time(train.start_time)
            self.table.setItem(row, 2, QTableWidgetItem(time_str))
            
            # Frequency
            self.table.setItem(row, 3, QTableWidgetItem(f"{train.frequency} min"))
            
            # Edit button
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda checked, r=row: self.edit_train(r))
            self.table.setCellWidget(row, 4, edit_btn)
            
            # Delete button
            delete_btn = QPushButton("Delete")
            delete_btn.setStyleSheet("background-color: #cc0000;")
            delete_btn.clicked.connect(lambda checked, r=row: self.delete_train(r))
            self.table.setCellWidget(row, 5, delete_btn)
    
    def handle_cell_click(self, row, col):
        # Only show menu when clicking on Route column (column 1)
        if col == 1:
            self.show_stations_menu(row)
    
    def show_stations_menu(self, row):
        train = self.train_repo.get_by_index(row)
        
        # Create menu
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 2px solid #404040;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 30px;
                border-radius: 3px;
            }
            QMenu::item:selected {
                background-color: #0066cc;
            }
        """)
        
        # Add title
        title_action = menu.addAction(f"📍 All Stations ({len(train.stations)})")
        title_action.setEnabled(False)
        menu.addSeparator()
        
        # Add all stations
        for i, station in enumerate(train.stations, 1):
            prefix = "🚉" if i == 1 or i == len(train.stations) else "  "
            station_name = station.name if isinstance(station, Station) else str(station)
            menu.addAction(f"{prefix} {i}. {station_name}")
        
        # Show menu at cursor position
        menu.exec(QCursor.pos())
    
    def add_train(self):
        dialog = AddTrainDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            if data['stations']:
                # Convert station names to Station objects
                station_objects = [Station(name) for name in data['stations']]
                self.train_repo.add(
                    code=data['type'],
                    stations=station_objects,
                    start_time=data['start_time'],
                    frequency=data['frequency']
                )
                self.refresh_table()
    
    def edit_train(self, row):
        train = self.train_repo.get_by_index(row)
        train_data = {
            'type': train.code,
            'stations': train.stations,
            'start_time': train.start_time,
            'frequency': train.frequency
        }
        
        dialog = AddTrainDialog(self, train_data)
        if dialog.exec():
            data = dialog.get_data()
            if data['stations']:
                # Remove old train and add updated one
                self.train_repo.remove(train)
                station_objects = [Station(name) for name in data['stations']]
                self.train_repo.add(
                    code=data['type'],
                    stations=station_objects,
                    start_time=data['start_time'],
                    frequency=data['frequency']
                )
                self.refresh_table()
    
    def delete_train(self, row):
        train = self.train_repo.get_by_index(row)
        self.train_repo.remove(train)
        self.refresh_table()


# Example usage:
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    
    # Create repository and window
    train_repo = TrainRepository()
    window = TimetableWindow(train_repo)
    window.show()
    
    sys.exit(app.exec())