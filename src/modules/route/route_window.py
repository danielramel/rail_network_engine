from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QTableWidget, QTableWidgetItem,
    QPushButton, QDialog, QHBoxLayout, QLabel
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from core.config.color import Color
from core.models.station import Station
from core.models.route import Route
from modules.route.route_editor_dialog import RouteEditorDialog
from modules.route.stylesheets.route_stylesheet import ROUTE_STYLESHEET
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QHeaderView
from core.models.railway.railway_system import RailwaySystem

class RouteWindow(QMainWindow):
    window_closed = pyqtSignal()
    def __init__(self, railway: RailwaySystem):
        super().__init__()
        self._railway = railway
        self.expanded_rows: set[int] = set()
        self._init_layout()
        self.refresh_table()

    # ------------------------------ UI setup ------------------------------
    def _init_layout(self):
        self.setWindowTitle("Route Management")
        self.setStyleSheet(ROUTE_STYLESHEET)
        self.setMinimumSize(1150, 400)


        central = QWidget(self)
        root = QVBoxLayout(central)

        # Top bar with actions
        top_bar = QHBoxLayout()
        top_bar.addWidget(QLabel("Routes"))
        top_bar.addStretch()
        add_btn = QPushButton("Add Route")
        add_btn.clicked.connect(self.add_route)
        top_bar.addWidget(add_btn)
        root.addLayout(top_bar)

        # Table
        table = QTableWidget()
        table.setColumnCount(11)
        table.setHorizontalHeaderLabels([
            "Code", "Route", "", "", "", "", "First", "Last", "Freq", "Edit", "Delete"
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
        """Rebuild route view based on repository contents."""
        routes = self._railway.routes.all()
        total_rows = 0
        for index, route in enumerate(routes):
            total_rows += 1
            if index in self.expanded_rows:
                total_rows += len(route.stops)+1  # +1 for header row

        self.table.setRowCount(total_rows)
        self.table.clearSpans()

        current_row = 0
        for idx, route in enumerate(routes):
            route_text = self._format_route(route)
            row_items = [
                QTableWidgetItem(route.code),
                QTableWidgetItem(route_text),
                QTableWidgetItem(""),  # arrival placeholder
                QTableWidgetItem(""),  # departure placeholder
                QTableWidgetItem(""),  # travel placeholder
                QTableWidgetItem(""),  # stop placeholder
                QTableWidgetItem(self._format_time(route.first_train)),
                QTableWidgetItem(self._format_time(route.last_train)),
                QTableWidgetItem(f"{route.frequency} min"),
            ]

            # Styling for code cell using route color if provided
            row_items[0].setBackground(self._get_code_color(route.color))
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

            self.table.setSpan(current_row, 1, 1, 5)

            # Action buttons
            edit_btn = QPushButton()
            edit_btn.clicked.connect(lambda _=False, i=idx: self.edit_route(i))
            self.table.setCellWidget(current_row, 9, edit_btn)

            delete_btn = QPushButton()
            delete_btn.setStyleSheet("background-color:#802020;color:white;")
            delete_btn.clicked.connect(lambda _=False, i=idx: self.delete_route(i))
            self.table.setCellWidget(current_row, 10, delete_btn)

            if idx in self.expanded_rows:
                span = len(route.stops) + 2
                for col in (0, 6, 7, 8, 9, 10):
                    self.table.setSpan(current_row, col, span, 1)
                # Pre-compute arrival/departure times from travel/stop chain
                self._set_table_widget_item(current_row+1, 1, "Station", bold=True)
                self._set_table_widget_item(current_row+1, 2, "Arrival", bold=True)
                self._set_table_widget_item(current_row+1, 3, "Departure", bold=True)
                self._set_table_widget_item(current_row+1, 4, "Travel", bold=True)
                self._set_table_widget_item(current_row+1, 5, "Dwell", bold=True)
                arrivals, departures = self._compute_times(route)
                for i, stop in enumerate(route.stops):
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
        route_idx = item.data(Qt.ItemDataRole.UserRole)
        
        if route_idx is None: # Clicked on an expanded station row
            return
        
        if route_idx in self.expanded_rows:
            self.expanded_rows.remove(route_idx)
        else:
            self.expanded_rows.add(route_idx)
        
        self.refresh_table()
        

    def add_route(self):
        dialog = RouteEditorDialog(self, self._railway)

        def _on_finished(res: int):
            if res == QDialog.DialogCode.Rejected:
                return
            data = dialog.get_data()
            route = self._build_route_from_dialog(data)
            self._railway.routes.add(route)
            self.refresh_table()

        dialog.finished.connect(_on_finished)
        dialog.setModal(False)
        dialog.show()

    def edit_route(self, route_idx):
        route = self._railway.routes.get(route_idx)
        dialog = RouteEditorDialog(self, self._railway, route)

        def _on_finished(res: int):
            if res == QDialog.DialogCode.Rejected:
                return
            data = dialog.get_data()
            updated = self._build_route_from_dialog(data)
            # Replace route in repository (preserve index ordering)
            self._railway.routes.remove(route)
            self._railway.routes.add(updated)
            if route_idx in self.expanded_rows:
                self.expanded_rows.remove(route_idx)
            self.refresh_table()

        dialog.finished.connect(_on_finished)
        dialog.setModal(False)
        dialog.show()

    def delete_route(self, route_idx):
        route = self._railway.routes.get(route_idx)
        self._railway.routes.remove(route)
        self.expanded_rows.discard(route_idx)  # Remove from expanded if it was expanded
        self.refresh_table()

    def _format_time(self, minutes: int | None) -> str:
        if minutes is None:
            return ""
        return f"{minutes // 60:02d}:{minutes % 60:02d}"

    def _get_code_color(self, color: str) -> QColor:
        return QColor(*Color.get(color))

    def _format_route(self, route: Route) -> str:
        stops = route.stops
        if not stops:
            return 'No stations'
        names = [stop['station'].name for stop in stops[:3]]  # take first 3 stations
        if len(stops) > 3:
            return ' → '.join(names) + ' → ...' + ' → ' + stops[-1]['station'].name + f" ({route.get_full_travel_time()} min)"
        return ' → '.join(names) + f" ({route.get_full_travel_time()} min)"


    # ------------------------ Dialog data conversion ---------------------
    def _build_route_from_dialog(self, data: dict) -> Route:
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
        route = Route(
            code=data['code'],
            color=data.get('color', 'RED'),
            first_train=first_dep,
            last_train=last_dep,
            frequency=data['frequency'],
            stops=computed_stops
        )
        return route
    def _compute_times(self, route: Route) -> tuple[list[int | None], list[int | None]]:
        arrivals: list[int | None] = []
        departures: list[int | None] = []
        current_dep = route.first_train
        for i, stop in enumerate(route.stops):
            if i == 0:
                arrivals.append(None)
                departures.append(current_dep)
                continue
            travel = int(stop['travel_time']) if stop['travel_time'] is not None else 0
            arr = current_dep + travel
            arrivals.append(arr)
            stop = int(stop['stop_time']) if stop['stop_time'] is not None else 0
            if i == len(route.stops) - 1:
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
