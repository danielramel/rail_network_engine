from models.geometry.position import Position
from ui.components.base import BaseUIComponent
import pygame
from domain.rail_map import RailMap
from models.train import TrainRepository
from config.colors import BLUE, WHITE, BLACK, GREY, GREEN, RED, YELLOW

class TimetableView(BaseUIComponent):
    def __init__(self, map: RailMap, train_repository: TrainRepository, screen: pygame.Surface):
        self._surface = screen
        self._map = map
        self._train_repository = train_repository
        
        # Fonts - all bigger
        self.title_font = pygame.font.SysFont('Arial', 36, bold=True)
        self.header_font = pygame.font.SysFont('Arial', 24, bold=True)
        self.text_font = pygame.font.SysFont('Arial', 20)
                
        # Table dimensions
        self.table_width = 800
        
        # Add train button
        self.add_button_rect = None
        self.is_hovering_button = False
       
    def render(self, screen_pos: Position | None):
       import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QTableWidget, QTableWidgetItem, 
                              QPushButton, QDialog, QFormLayout, QComboBox, 
                              QTimeEdit, QListWidget, QLabel, QDialogButtonBox,
                              QMenu)
from PyQt6.QtCore import Qt, QTime, QPoint
from PyQt6.QtGui import QColor, QCursor

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
            time = QTime.fromString(train_data['start_time'], "HH:mm")
            self.time_edit.setTime(time)
            self.freq_combo.setCurrentText(train_data['frequency'])
            # Select stations in the list
            for station in train_data['stations']:
                items = self.station_list.findItems(station, Qt.MatchFlag.MatchExactly)
                if items:
                    items[0].setSelected(True)
        
        self.setLayout(layout)
    
    def get_data(self):
        selected_stations = [item.text() for item in self.station_list.selectedItems()]
        return {
            'type': self.type_combo.currentText(),
            'stations': selected_stations,
            'start_time': self.time_edit.time().toString("HH:mm"),
            'frequency': self.freq_combo.currentText()
        }


class TimetableWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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
        
        # Mock data with ~20 stations each
        self.trains = [
            {"type": "S70", "stations": [
                "Hauptbahnhof", "Königsplatz", "Stadtmitte", "Rathaus", "Marienplatz",
                "Sendlinger Tor", "Goetheplatz", "Poccistraße", "Implerstraße",
                "Harras", "Partnachplatz", "Aidenbachstraße", "Machtlfinger Straße",
                "Forstenrieder Allee", "Basler Straße", "Holzapfelkreuth", "Großhadern",
                "Klinikum Großhadern", "Westpark", "Ostbahnhof"
            ], "start_time": "05:12", "frequency": "20 min"},
            {"type": "S71", "stations": [
                "Flughafen", "Besucherpark", "Nordallee", "Feldmoching", "Hasenbergl",
                "Dülferstraße", "Dietlindenstraße", "Studentenstadt", "Alte Heide",
                "Nordfriedhof", "Münchner Freiheit", "Giselastraße", "Universität",
                "Odeonsplatz", "Karlsplatz", "Messegelände", "Theresienwiese",
                "Schwanthalerhöhe", "Donnersberger Brücke", "Hauptbahnhof"
            ], "start_time": "05:25", "frequency": "20 min"},
            {"type": "Z72", "stations": [
                "Nordstadt", "Petuelring", "Scheidplatz", "Bonner Platz", "Ackermannstraße",
                "Hohenzollernplatz", "Josephsplatz", "Theresienstraße", "Zentrum",
                "Stiglmaierplatz", "Königsplatz", "Lenbachplatz", "Marktplatz",
                "Isartor", "Rosenheimer Platz", "Ostbahnhof", "Berg am Laim",
                "Trudering", "Moosach", "Südbahnhof"
            ], "start_time": "06:00", "frequency": "30 min"},
        ]
        
        self.refresh_table()
        layout.addWidget(self.table)
        
        central_widget.setLayout(layout)
    
    def refresh_table(self):
        self.table.setRowCount(len(self.trains))
        
        type_colors = {
            "S70": QColor(100, 150, 255),
            "S71": QColor(255, 150, 100),
            "Z72": QColor(150, 255, 150)
        }
        
        for row, train in enumerate(self.trains):
            # Type
            type_item = QTableWidgetItem(train['type'])
            type_item.setBackground(type_colors.get(train['type'], QColor(200, 200, 200)))
            type_item.setForeground(QColor(0, 0, 0))
            type_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 0, type_item)
            
            # Route - only show first and last station
            if train['stations']:
                first = train['stations'][0]
                last = train['stations'][-1]
                route = f"{first} → ... → {last}"
            else:
                route = "No stations"
            route_item = QTableWidgetItem(route)
            route_item.setData(Qt.ItemDataRole.UserRole, row)  # Store row index
            self.table.setItem(row, 1, route_item)
            
            # Start time
            self.table.setItem(row, 2, QTableWidgetItem(train['start_time']))
            
            # Frequency
            self.table.setItem(row, 3, QTableWidgetItem(train['frequency']))
            
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
        train = self.trains[row]
        
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
        title_action = menu.addAction(f"📍 All Stations ({len(train['stations'])})")
        title_action.setEnabled(False)
        menu.addSeparator()
        
        # Add all stations
        for i, station in enumerate(train['stations'], 1):
            prefix = "🚉" if i == 1 or i == len(train['stations']) else "  "
            menu.addAction(f"{prefix} {i}. {station}")
        
        # Show menu at cursor position
        menu.exec(QCursor.pos())
    
    def add_train(self):
        dialog = AddTrainDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            if data['stations']:
                self.trains.append(data)
                self.refresh_table()
    
    def edit_train(self, row):
        dialog = AddTrainDialog(self, self.trains[row])
        if dialog.exec():
            data = dialog.get_data()
            if data['stations']:
                self.trains[row] = data
                self.refresh_table()
    
    def delete_train(self, row):
        del self.trains[row]
        self.refresh_table()



    