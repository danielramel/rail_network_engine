"""Stylesheets for the Train Editor Dialog"""


TABLE_STYLE = """
    QTableWidget {
        selection-background-color: #4a90e2;
        selection-color: white;
    }

    QTableWidget::item:selected {
        background-color: blue;
        color: white;
    }
    QTableWidget::item:selected:hover {
        background-color: red;
        color: white;
    }
"""


MOVE_BUTTON_STYLE = """
    QPushButton {
        font-size: 14pt;
        min-width: 32px;
        max-width: 32px;
        min-height: 32px;
        max-height: 32px;
        background-color: #2196F3;
        color: white;
        border: 1px solid #1976D2;
        border-radius: 4px;
        padding: 0px;
    }
    QPushButton:hover {
        background-color: #1E88E5;
        border-color: #1565C0;
    }
    QPushButton:pressed {
        background-color: #1565C0;
    }
"""


ADD_BUTTON_STYLE = """
    QPushButton {
        font-size: 18pt;
        font-weight: bold;
        min-width: 32px;
        max-width: 32px;
        min-height: 32px;
        max-height: 32px;
        background-color: #4CAF50;
        color: white;
        border: 1px solid #388E3C;
        border-radius: 4px;
        padding: 0px;
        text-align: center;
    }
    QPushButton:hover {
        background-color: #43A047;
        border-color: #2E7D32;
    }
    QPushButton:pressed {
        background-color: #388E3C;
    }
"""


REMOVE_BUTTON_STYLE = """
    QPushButton {
        font-size: 16pt;
        min-width: 32px;
        max-width: 32px;
        min-height: 32px;
        max-height: 32px;
        background-color: #f44336;
        color: white;
        border: 1px solid #d32f2f;
        border-radius: 4px;
        padding: 0px;
    }
    QPushButton:hover {
        background-color: #e53935;
        border-color: #c62828;
    }
    QPushButton:pressed {
        background-color: #d32f2f;
    }
"""
