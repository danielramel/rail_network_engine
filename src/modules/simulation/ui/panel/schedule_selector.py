from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QColor, QBrush
from core.models.route import Route
from core.config.color import Color


class ScheduleSelector(QWidget):
    schedule_chosen = pyqtSignal(Route, int)
    window_closed = pyqtSignal()

    def __init__(self, routes: list[Route], parent=None):
        super().__init__(parent)
        self._routes = routes
        self._selected_route: Route | None = None
        self.setWindowTitle("Select Schedule")
        self.setGeometry(300, 200, 600, 400)

        self._init_ui()
        self._populate_schedule_list()

    def _init_ui(self):
        main_layout = QVBoxLayout()

        title = QLabel("Select a schedule")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        main_layout.addWidget(title)

        # Horizontal layout for the two panels
        panels_layout = QHBoxLayout()

        self.route_list = QListWidget()
        self.route_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.route_list.itemSelectionChanged.connect(self._on_route_selected)
        panels_layout.addWidget(self.route_list)

        self.start_times_list = QListWidget()
        self.start_times_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        panels_layout.addWidget(self.start_times_list)

        main_layout.addLayout(panels_layout)

        btn_layout = QHBoxLayout()
        self.select_btn = QPushButton("Confirm Selection")
        self.select_btn.setEnabled(False)
        self.select_btn.clicked.connect(self._on_confirm)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.close)
        btn_layout.addWidget(self.select_btn)
        btn_layout.addWidget(cancel_btn)

        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)


    @staticmethod
    def _fmt_time(minutes: int) -> str:
        h, m = divmod(minutes, 60)
        return f"{h:02d}:{m:02d}"

    def _populate_schedule_list(self):
        self.route_list.clear()
        for s in self._routes:
            if not s.stops:
                label = f"{s.code} — (no stations)"
            else:
                first_station = s.stops[0]["station"].name
                last_station = s.stops[-1]["station"].name
                label = f"{s.code} — {first_station} → {last_station}"

            item = QListWidgetItem(label)
            item.setData(int(Qt.ItemDataRole.UserRole), s)

            # color row background
            item.setBackground(QBrush(QColor(*Color[s.color])))

            # ensure text contrast
            item.setForeground(Qt.GlobalColor.black)

            self.route_list.addItem(item)

    def _on_route_selected(self):
        selected_items = self.route_list.selectedItems()
        if not selected_items:
            self._selected_route = None
            self.start_times_list.clear()
            self.select_btn.setEnabled(False)
            return

        item = selected_items[0]
        schedule = item.data(int(Qt.ItemDataRole.UserRole))
        self._selected_route = schedule
        self._populate_start_times(schedule)

    def _populate_start_times(self, schedule: Route):
        self.start_times_list.clear()
        times = list(range(schedule.first_train, schedule.last_train + 1, schedule.frequency))
        for t in times:
            item = QListWidgetItem(self._fmt_time(t))
            item.setData(int(Qt.ItemDataRole.UserRole), t)
            self.start_times_list.addItem(item)
        self.select_btn.setEnabled(bool(times))

    def _on_confirm(self):
        route_item = self.route_list.currentItem()
        time_item = self.start_times_list.currentItem()

        if not route_item or not time_item:
            QMessageBox.warning(self, "Incomplete selection", "Select both route and start time.")
            return

        route = route_item.data(int(Qt.ItemDataRole.UserRole))
        start_time = time_item.data(int(Qt.ItemDataRole.UserRole))
        self.schedule_chosen.emit(route, start_time)
        super().close()
        
    def closeEvent(self, event) -> None:
        self.window_closed.emit()
        super().closeEvent(event)
    
