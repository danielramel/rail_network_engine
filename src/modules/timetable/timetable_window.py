from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QTableWidget, QTableWidgetItem,
    QPushButton, QDialog, QHBoxLayout, QLabel,
    QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from core.config.color import Color
from core.models.station import Station
from core.models.timetable import Timetable
from modules.timetable.timetable_editor_dialog import TimetableEditorDialog
from modules.timetable.stylesheets.timetable_window_stylesheet import TIMETABLE_STYLESHEET
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QHeaderView
from core.models.railway.railway_system import RailwaySystem

class TimeTableWindow(QMainWindow):
    window_closed = pyqtSignal()
    def __init__(self, railway: RailwaySystem):
        super().__init__()
        self._railway = railway
        self.expanded_rows: set[int] = set()
        self._init_layout()
        self.refresh_table()

    def _init_layout(self):
        self.setWindowTitle("Timetables")
        self.setStyleSheet(TIMETABLE_STYLESHEET)
        self.setMinimumSize(1150, 400)


        central = QWidget(self)
        root = QVBoxLayout(central)

        # Top bar with actions
        top_bar = QHBoxLayout()
        top_bar.addWidget(QLabel("Timetables"))
        top_bar.addStretch()
        add_btn = QPushButton("Add Timetable")
        add_btn.clicked.connect(self.add_timetable)
        top_bar.addWidget(add_btn)
        root.addLayout(top_bar)

        # Table
        table = QTableWidget()
        table.setColumnCount(11)
        table.setHorizontalHeaderLabels([
            "Code", "timetable", "", "", "", "", "First", "Last", "Freq", "Edit", "Delete"
        ])

        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setMinimumSectionSize(100)

            
        table.verticalHeader().setVisible(False)
        table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.cellClicked.connect(self.handle_cell_click)

        self.table = table
        root.addWidget(self.table)

        self.setCentralWidget(central)
            
    def refresh_table(self):
        """Rebuild timetable view based on repository contents."""
        timetables = self._railway.timetables.all()
        total_rows = 0
        for index, timetable in enumerate(timetables):
            total_rows += 1
            if index in self.expanded_rows:
                total_rows += len(timetable.stops)+1  # +1 for header row

        self.table.setRowCount(total_rows)
        self.table.clearSpans()

        current_row = 0
        for idx, timetable in enumerate(timetables):
            timetable_text = self._format_timetable(timetable)
            row_items = [
                QTableWidgetItem(timetable.code),
                QTableWidgetItem(timetable_text),
                QTableWidgetItem(""),  # arrival placeholder
                QTableWidgetItem(""),  # departure placeholder
                QTableWidgetItem(""),  # travel placeholder
                QTableWidgetItem(""),  # stop placeholder
                QTableWidgetItem(self._format_time(timetable.first_train)),
                QTableWidgetItem(self._format_time(timetable.last_train)),
                QTableWidgetItem(f"{timetable.frequency} min"),
            ]

            # Styling for code cell using timetable color if provided
            row_items[0].setBackground(self._get_code_color(timetable.color))
            row_items[0].setForeground(QColor(*Color.BLACK))
            row_items[0].setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            # timetable item metadata
            row_items[1].setData(Qt.ItemDataRole.UserRole, idx)
            row_items[1].setToolTip("Click to expand/collapse stations")
            row_items[1].setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

            for cell in row_items[2:]:
                cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            for col, item in enumerate(row_items):
                self.table.setItem(current_row, col, item)

            self.table.setSpan(current_row, 1, 1, 5)

            # Action buttons
            edit_btn = QPushButton()
            edit_btn.clicked.connect(lambda _=False, i=idx: self.edit_timetable(i))
            self.table.setCellWidget(current_row, 9, edit_btn)

            delete_btn = QPushButton()
            delete_btn.setStyleSheet("background-color:#802020;color:white;")
            delete_btn.clicked.connect(lambda _=False, i=idx: self.delete_timetable(i))
            self.table.setCellWidget(current_row, 10, delete_btn)

            if idx in self.expanded_rows:
                span = len(timetable.stops) + 2
                for col in (0, 6, 7, 8, 9, 10):
                    self.table.setSpan(current_row, col, span, 1)
                # Pre-compute arrival/departure times from travel/stop chain
                self._set_table_widget_item(current_row+1, 1, "Station", bold=True)
                self._set_table_widget_item(current_row+1, 2, "Arrival", bold=True)
                self._set_table_widget_item(current_row+1, 3, "Departure", bold=True)
                self._set_table_widget_item(current_row+1, 4, "Travel", bold=True)
                self._set_table_widget_item(current_row+1, 5, "Stop", bold=True)
                arrivals, departures = self._compute_times(timetable)
                for i, stop in enumerate(timetable.stops):
                    self._set_table_widget_item(current_row + i+2, 1, stop['station'].name, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

                    self._set_table_widget_item(current_row + i+2, 2, self._format_time(arrivals[i]))
                    self._set_table_widget_item(current_row + i+2, 3, self._format_time(departures[i]))

                    travel = stop.get('travel_time')
                    stop = stop.get('stop_time')
                    self._set_table_widget_item(current_row + i+2, 4, "" if travel is None else f"{travel} min")
                    self._set_table_widget_item(current_row + i+2, 5, "" if stop is None else f"{stop} min")

                current_row += span
            else:
                current_row += 1
        

    def handle_cell_click(self, row, col):
        if col != 1:
            return
        item = self.table.item(row, 1)
        timetable_idx = item.data(Qt.ItemDataRole.UserRole)
        
        if timetable_idx is None: # Clicked on an expanded station row
            return
        
        if timetable_idx in self.expanded_rows:
            self.expanded_rows.remove(timetable_idx)
        else:
            self.expanded_rows.add(timetable_idx)
        
        self.refresh_table()
        

    def add_timetable(self):
        dialog = TimetableEditorDialog(self, self._railway)

        def _on_finished(res: int):
            if res == QDialog.DialogCode.Rejected:
                return
            data = dialog.get_data()
            timetable = self._build_timetable_from_dialog(data)
            self._railway.timetables.add(timetable)
            self.refresh_table()

        dialog.finished.connect(_on_finished)
        dialog.setModal(False)
        dialog.show()

    def edit_timetable(self, timetable_idx):
        timetable = self._railway.timetables.get(timetable_idx)
        dialog = TimetableEditorDialog(self, self._railway, timetable)

        def _on_finished(res: int):
            if res == QDialog.DialogCode.Rejected:
                return
            data = dialog.get_data()
            updated = self._build_timetable_from_dialog(data)
            # Replace timetable in repository (preserve index ordering)
            self._railway.timetables.remove(timetable)
            self._railway.timetables.add(updated)
            if timetable_idx in self.expanded_rows:
                self.expanded_rows.remove(timetable_idx)
            self.refresh_table()

        dialog.finished.connect(_on_finished)
        dialog.setModal(False)
        dialog.show()

    def delete_timetable(self, timetable_idx):
        timetable = self._railway.timetables.get(timetable_idx)
        
        reply = QMessageBox.warning(
            self,
            "Delete timetable",
            f"Are you sure you want to delete timetable '{timetable.code}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
            
        self._railway.timetables.remove(timetable)
        self.expanded_rows.discard(timetable_idx)  # Remove from expanded if it was expanded
        self.refresh_table()

    def _format_time(self, minutes: int | None) -> str:
        if minutes is None:
            return ""
        return f"{minutes // 60:02d}:{minutes % 60:02d}"

    def _get_code_color(self, color: str) -> QColor:
        return QColor(*Color.get(color))

    def _format_timetable(self, timetable: Timetable) -> str:
        stops = timetable.stops
        if not stops:
            return 'No stations'
        names = [stop['station'].name for stop in stops[:3]]  # take first 3 stations
        if len(stops) > 3:
            return ' → '.join(names) + ' → ...' + ' → ' + stops[-1]['station'].name + f" ({timetable.get_full_travel_time()} min)"
        return ' → '.join(names) + f" ({timetable.get_full_travel_time()} min)"


    # ------------------------ Dialog data conversion ---------------------
    def _build_timetable_from_dialog(self, data: dict) -> Timetable:
        first_dep = self._hhmm_to_minutes(data['first_train_time'])
        last_dep = self._hhmm_to_minutes(data['last_train_time'])

        computed_stops: list[dict[str, Station | int]] = []
        for i, stop in enumerate(data['stops']):
            station = self._railway.stations.get(stop['id'])
            travel = stop.get('travel_time')
            stop = stop.get('stop_time')
            computed_stops.append({
                'station': station,
                'travel_time': travel if travel is not None else None,
                'stop_time': stop if stop is not None else None
            })
        timetable = Timetable(
            code=data['code'],
            color=data.get('color', 'RED'),
            first_train=first_dep,
            last_train=last_dep,
            frequency=data['frequency'],
            stops=computed_stops
        )
        return timetable
    def _compute_times(self, timetable: Timetable) -> tuple[list[int | None], list[int | None]]:
        arrivals: list[int | None] = []
        departures: list[int | None] = []
        current_dep = timetable.first_train
        for i, stop in enumerate(timetable.stops):
            if i == 0:
                arrivals.append(None)
                departures.append(current_dep)
                continue
            travel = int(stop['travel_time']) if stop['travel_time'] is not None else 0
            arr = current_dep + travel
            arrivals.append(arr)
            stop = int(stop['stop_time']) if stop['stop_time'] is not None else 0
            if i == len(timetable.stops) - 1:
                departures.append(None)
            else:
                current_dep = arr + stop
                departures.append(current_dep)
        return arrivals, departures

    def _hhmm_to_minutes(self, hhmm: str) -> int:
        h, m = hhmm.split(':')
        return int(h) * 60 + int(m)

    def closeEvent(self, event):
        """Override closeEvent to emit signal when window is closed"""
        self.window_closed.emit()
        super().closeEvent(event)
        
        
    def _set_table_widget_item(self, row: int, column: int, text: str, alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter, bold: bool = False) -> None:
        item = QTableWidgetItem(text)
        item.setTextAlignment(alignment)
        if bold:
            font = item.font()
            font.setBold(True)
            item.setFont(font)
        self.table.setItem(row, column, item)
