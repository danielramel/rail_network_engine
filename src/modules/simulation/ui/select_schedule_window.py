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
from core.models.schedule import Schedule


class SelectScheduleWindow(QWidget):
    """
    Window that receives a list of Schedule objects (or any objects).
    The user selects one item and clicks "Select Schedule" or double-clicks an item.
    The window emits `selected_schedule` with the selected object and then closes.
    """
    selected_schedule = pyqtSignal(object)

    def __init__(self, schedules: list[Schedule], parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Schedule")
        self.setGeometry(300, 200, 520, 360)
        self._schedules = schedules

        self._build_ui()
        self._populate_list()

    def _build_ui(self) -> None:
        v = QVBoxLayout()
        title = QLabel("Choose a schedule from the list")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        v.addWidget(title)

        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.list_widget.itemDoubleClicked.connect(self._on_item_double_clicked)
        self.list_widget.currentItemChanged.connect(self._on_selection_changed)
        v.addWidget(self.list_widget)

        buttons = QHBoxLayout()
        self.select_btn = QPushButton("Select Schedule")
        self.select_btn.setEnabled(False)
        self.select_btn.clicked.connect(self._on_select_clicked)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.close)

        buttons.addWidget(self.select_btn)
        buttons.addWidget(cancel_btn)
        v.addLayout(buttons)

        self.setLayout(v)

    @staticmethod
    def _format_time(minutes: int) -> str:
        h = minutes // 60
        m = minutes % 60
        return f"{h:02d}:{m:02d}"

    def _populate_list(self) -> None:
        self.list_widget.clear()
        for s in self._schedules:
            # Display a concise, human-friendly label
            if hasattr(s, "first_train") and hasattr(s, "last_train"):
                label = f"{s.code} — {self._format_time(s.first_train)} → {self._format_time(s.last_train)} (freq {s.frequency}m)"
            else:
                label = str(s)
            item = QListWidgetItem(label)
            # store the object in user role
            item.setData(int(Qt.ItemDataRole.UserRole), s)
            self.list_widget.addItem(item)

    def _on_selection_changed(self, current, previous) -> None:
        self.select_btn.setEnabled(current is not None)

    def _on_item_double_clicked(self, item: QListWidgetItem) -> None:
        self._emit_and_close(item)

    def _on_select_clicked(self) -> None:
        item = self.list_widget.currentItem()
        if item is None:
            QMessageBox.warning(self, "No selection", "Please select a schedule first.")
            return
        self._emit_and_close(item)

    def _emit_and_close(self, item: QListWidgetItem) -> None:
        selected = item.data(int(Qt.ItemDataRole.UserRole))
        # Emit the selected object
        self.selected_schedule.emit(selected)
        # Close the window
        self.close()