from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QTableWidget, QTableWidgetItem,
    QPushButton, QDialog, QHBoxLayout, QLabel
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from core.config.color import Color
from core.models.station import Station
from core.models.schedule import Schedule
from modules.timetable.views.schedule_editor_dialog import ScheduleEditorDialog
from modules.timetable.views.timetable_stylesheet import TIMETABLE_STYLESHEET
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QHeaderView
from core.models.railway.railway_system import RailwaySystem

class TimetableWindow(QMainWindow):
    window_closed = pyqtSignal()
    def __init__(self, railway: RailwaySystem):
        super().__init__()
        self._railway = railway
        self.expanded_rows: set[int] = set()
        self._init_layout()
        self.refresh_table()

    # ------------------------------ UI setup ------------------------------
    def _init_layout(self):
        self.setWindowTitle("Timetable")
        self.setStyleSheet(TIMETABLE_STYLESHEET)

        central = QWidget(self)
        root = QVBoxLayout(central)

        # Top bar with actions
        top_bar = QHBoxLayout()
        top_bar.addWidget(QLabel("Schedules"))
        top_bar.addStretch()
        add_btn = QPushButton("Add schedule")
        add_btn.clicked.connect(self.add_schedule)
        top_bar.addWidget(add_btn)
        root.addLayout(top_bar)

        # Table
        table = QTableWidget()
        table.setColumnCount(11)
        table.setHorizontalHeaderLabels([
            "Code", "Route", "Arrival", "Departure", "Travel (min)", "Dwell (min)",
            "First", "Last", "Freq", "Edit", "Delete"
        ])
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        for c in (2, 3, 4, 5, 6, 7, 8, 9, 10):
            header.setSectionResizeMode(c, QHeaderView.ResizeMode.ResizeToContents)
        table.verticalHeader().setVisible(False)
        table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        table.cellClicked.connect(self.handle_cell_click)

        self.table = table
        root.addWidget(self.table)

        self.setCentralWidget(central)
            
    def refresh_table(self):
        """Rebuild timetable view based on repository contents."""
        schedules = self._railway.schedules.all()
        total_rows = 0
        for index, schedule in enumerate(schedules):
            total_rows += 1
            if index in self.expanded_rows:
                total_rows += len(schedule.stops)

        self.table.setRowCount(total_rows)
        self.table.clearSpans()

        current_row = 0
        for idx, schedule in enumerate(schedules):
            route_text = self._format_route(schedule.stops)
            row_items = [
                QTableWidgetItem(schedule.code),
                QTableWidgetItem(route_text),
                QTableWidgetItem(""),  # arrival placeholder
                QTableWidgetItem(""),  # departure placeholder
                QTableWidgetItem(""),  # travel placeholder
                QTableWidgetItem(""),  # dwell placeholder
                QTableWidgetItem(self._format_time(schedule.first_train)),
                QTableWidgetItem(self._format_time(schedule.last_train)),
                QTableWidgetItem(f"{schedule.frequency} min"),
            ]

            # Styling for code cell using schedule color if provided
            row_items[0].setBackground(self._get_code_color(schedule.color))
            row_items[0].setForeground(QColor(*Color.BLACK))
            row_items[0].setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            # Route item metadata
            row_items[1].setData(Qt.ItemDataRole.UserRole, idx)
            row_items[1].setToolTip("Click to expand/collapse stations")
            row_items[1].setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

            for cell in row_items[2:]:
                cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            for col, item in enumerate(row_items):
                self.table.setItem(current_row, col, item)

            # Span route across arrival/departure columns for collapsed main row
            self.table.setSpan(current_row, 1, 1, 5)

            # Action buttons
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda _=False, i=idx: self.edit_schedule(i))
            self.table.setCellWidget(current_row, 9, edit_btn)

            delete_btn = QPushButton("Delete")
            delete_btn.setStyleSheet("background-color:#802020;color:white;")
            delete_btn.clicked.connect(lambda _=False, i=idx: self.delete_schedule(i))
            self.table.setCellWidget(current_row, 10, delete_btn)

            if idx in self.expanded_rows:
                # Span static columns for group
                span = len(schedule.stops) + 1
                for col in (0, 6, 7, 8, 9, 10):
                    self.table.setSpan(current_row, col, span, 1)
                # Pre-compute arrival/departure times from travel/dwell chain
                arrivals, departures = self._compute_times(schedule)
                for offset, stop in enumerate(schedule.stops, 1):
                    station_item = QTableWidgetItem(stop['station'].name)
                    station_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                    self.table.setItem(current_row + offset, 1, station_item)

                    arr_item = QTableWidgetItem(self._format_time(arrivals[offset-1]))
                    arr_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.table.setItem(current_row + offset, 2, arr_item)

                    dep_item = QTableWidgetItem(self._format_time(departures[offset-1]))
                    dep_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.table.setItem(current_row + offset, 3, dep_item)

                    travel = stop.get('travel_time')
                    dwell = stop.get('dwell_time')
                    travel_item = QTableWidgetItem("" if travel is None else f"{travel} min")
                    travel_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.table.setItem(current_row + offset, 4, travel_item)
                    dwell_item = QTableWidgetItem("" if dwell is None else f"{dwell} min")
                    dwell_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.table.setItem(current_row + offset, 5, dwell_item)

                current_row += span
            else:
                current_row += 1
        

    def handle_cell_click(self, row, col):
        if col != 1:
            return
        item = self.table.item(row, 1)
        schedule_idx = item.data(Qt.ItemDataRole.UserRole)
        
        if schedule_idx is None: # Clicked on an expanded station row
            return
        
        if schedule_idx in self.expanded_rows:
            self.expanded_rows.remove(schedule_idx)
        else:
            self.expanded_rows.add(schedule_idx)
        
        self.refresh_table()
        

    def add_schedule(self):
        dialog = ScheduleEditorDialog(self, self._railway)

        def _on_finished(res: int):
            if res == QDialog.DialogCode.Rejected:
                return
            data = dialog.get_data()
            schedule = self._build_schedule_from_dialog(data)
            self._railway.schedules.add(schedule)
            self.refresh_table()

        dialog.finished.connect(_on_finished)
        dialog.setModal(False)
        dialog.show()

    def edit_schedule(self, schedule_idx):
        schedule = self._railway.schedules.get(schedule_idx)
        dialog = ScheduleEditorDialog(self, self._railway)

        # Pre-population is TODO: current dialog supports only blank creation.
        # Could be extended later to set existing values.

        def _on_finished(res: int):
            if res == QDialog.DialogCode.Rejected:
                return
            data = dialog.get_data()
            updated = self._build_schedule_from_dialog(data)
            # Replace schedule in repository (preserve index ordering)
            self._railway.schedules.remove(schedule)
            self._railway.schedules.add(updated)
            if schedule_idx in self.expanded_rows:
                self.expanded_rows.remove(schedule_idx)
            self.refresh_table()

        dialog.finished.connect(_on_finished)
        dialog.setModal(False)
        dialog.show()

    def delete_schedule(self, schedule_idx):
        schedule = self._railway.schedules.get(schedule_idx)
        self._railway.schedules.remove(schedule)
        self.expanded_rows.discard(schedule_idx)  # Remove from expanded if it was expanded
        self.refresh_table()

    def _format_time(self, minutes: int | None) -> str:
        if minutes is None:
            return ""
        return f"{minutes // 60:02d}:{minutes % 60:02d}"

    def _get_code_color(self, color: str) -> QColor:
        return QColor(*Color[color])

    def _format_route(self, stops: list[dict[str, Station | int]]) -> str:
        if not stops:
            return 'No stations'
        names = [stop['station'].name for stop in stops[:4]]  # take first 4 stations
        if len(stops) > 5:
            return ' → '.join(names) + ' → ...' + ' → ' + stops[-1]['station'].name
        return ' → '.join(names)


    # ------------------------ Dialog data conversion ---------------------
    def _build_schedule_from_dialog(self, data: dict) -> Schedule:
        """Convert raw dialog data (with travel/dwell times) into a Schedule.

        Dialog provides:
          code, color (string)
          first_train_time, last_train_time (HH:MM strings)
          frequency (int minutes)
          stops: list of dicts with id, travel_time, dwell_time
            - First stop: travel_time=None, dwell_time=None
            - Intermediate: both numbers
            - Last: dwell_time=None
        We compute absolute arrival/departure for a reference first train.
        """
        first_dep = self._hhmm_to_minutes(data['first_train_time'])
        last_dep = self._hhmm_to_minutes(data['last_train_time'])

        computed_stops: list[dict[str, Station | int]] = []
        for i, stop in enumerate(data['stops']):
            station = self._railway.stations.get(stop['id'])
            travel = stop.get('travel_time')
            dwell = stop.get('dwell_time')
            computed_stops.append({
                'station': station,
                'travel_time': travel if travel is not None else None,
                'dwell_time': dwell if dwell is not None else None
            })
        schedule = Schedule(
            code=data['code'],
            color=data.get('color', 'RED'),
            first_train=first_dep,
            last_train=last_dep,
            frequency=data['frequency'],
            stops=computed_stops
        )
        return schedule
    def _compute_times(self, schedule: Schedule) -> tuple[list[int | None], list[int | None]]:
        """Derive arrival and departure times from travel/dwell chain.
        Returns (arrivals, departures) lists aligned with schedule.stops.
        First arrival None, final departure None.
        """
        arrivals: list[int | None] = []
        departures: list[int | None] = []
        current_dep = schedule.first_train
        for i, stop in enumerate(schedule.stops):
            if i == 0:
                arrivals.append(None)
                departures.append(current_dep)
                continue
            travel = int(stop['travel_time']) if stop['travel_time'] is not None else 0
            arr = current_dep + travel
            arrivals.append(arr)
            dwell = int(stop['dwell_time']) if stop['dwell_time'] is not None else 0
            if i == len(schedule.stops) - 1:
                departures.append(None)
            else:
                current_dep = arr + dwell
                departures.append(current_dep)
        return arrivals, departures

    def _hhmm_to_minutes(self, hhmm: str) -> int:
        h, m = hhmm.split(':')
        return int(h) * 60 + int(m)

    def closeEvent(self, event):
        """Override closeEvent to emit signal when window is closed"""
        self.window_closed.emit()
        super().closeEvent(event)