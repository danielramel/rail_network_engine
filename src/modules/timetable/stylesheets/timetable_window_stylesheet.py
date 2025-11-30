TIMETABLE_STYLESHEET = """
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
"""