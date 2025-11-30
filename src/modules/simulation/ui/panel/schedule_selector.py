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
from core.models.timetable import Timetable
from core.config.color import Color


class ScheduleSelector(QWidget):
    schedule_chosen = pyqtSignal(Timetable, int)
    window_closed = pyqtSignal()

    def __init__(self, timetables: list[Timetable], parent=None):
        super().__init__(parent)
        self._timetables = timetables
        self._selected_timetable: Timetable | None = None
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

        self.timetable_list = QListWidget()
        self.timetable_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.timetable_list.itemSelectionChanged.connect(self._on_timetable_selected)
        panels_layout.addWidget(self.timetable_list)

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
        self.timetable_list.clear()
        for timetable in self._timetables:
            if not timetable.stops:
                label = f"{timetable.code} — (no stations)"
            else:
                first_station = timetable.stops[0]["station"].name
                last_station = timetable.stops[-1]["station"].name
                label = f"{timetable.code} — {first_station} → {last_station}"

            item = QListWidgetItem(label)
            item.setData(int(Qt.ItemDataRole.UserRole), timetable)

            # color row background
            item.setBackground(QBrush(QColor(*Color.get(timetable.color))))

            # ensure text contrast
            item.setForeground(Qt.GlobalColor.black)

            self.timetable_list.addItem(item)

    def _on_timetable_selected(self):
        selected_items = self.timetable_list.selectedItems()
        if not selected_items:
            self._selected_timetable = None
            self.start_times_list.clear()
            self.select_btn.setEnabled(False)
            return

        item = selected_items[0]
        schedule = item.data(int(Qt.ItemDataRole.UserRole))
        self._selected_timetable = schedule
        self._populate_start_times(schedule)

    def _populate_start_times(self, timetable: Timetable):
        self.start_times_list.clear()
        start_times = timetable.start_times
        if not start_times:
            self.start_times_list.addItem("(No available start times)")
            
        for t in start_times:
            item = QListWidgetItem(self._fmt_time(t))
            item.setData(int(Qt.ItemDataRole.UserRole), t)
            self.start_times_list.addItem(item)
            
        self.select_btn.setEnabled(bool(timetable.start_times))
        
    def _on_confirm(self):
        timetable_item = self.timetable_list.currentItem()
        time_item = self.start_times_list.currentItem()

        if not timetable_item or not time_item:
            QMessageBox.warning(self, "Incomplete selection", "Select both timetable and start time.")
            return

        timetable = timetable_item.data(int(Qt.ItemDataRole.UserRole))
        start_time = time_item.data(int(Qt.ItemDataRole.UserRole))
        self.schedule_chosen.emit(timetable, start_time)
        super().close()
        
    def closeEvent(self, event) -> None:
        self.window_closed.emit()
        super().closeEvent(event)
    
