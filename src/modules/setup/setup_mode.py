import json
from tkinter import messagebox
from core.graphics.graphics_context import GraphicsContext
from core.models.app_state import AppState
from tkinter import filedialog
import tkinter as tk
from core.models.railway.railway_system import RailwaySystem
from modules.setup.setup_mode_strategy import SetupModeStrategy
from modules.setup.setup_state import SetupState
from modules.setup.ui.start_simulation_button import StartSimulationButton
from modules.setup.ui.route_button import RouteButton
from shared.ui.models.full_screen_ui_component import FullScreenUIComponent
from shared.ui.models.ui_component import UIComponent
from shared.ui.models.ui_controller import UIController
from modules.setup.ui.exit_button import ExitButton
from modules.setup.ui.open_button import OpenButton
from modules.setup.ui.save_button import SaveButton
from modules.setup.ui.setup_mode_selector_buttons import SetupModeSelectorButtons
    

class SetupMode(UIController, FullScreenUIComponent):
    def __init__(self, app_state: AppState, railway: RailwaySystem, graphics: GraphicsContext):
        self._state = SetupState(app_state)
        self._railway = railway
        self._graphics = graphics
        
        self.elements: list[UIComponent] = [
            RouteButton(graphics.screen, railway),
            SaveButton(graphics.screen, railway, self._on_save),
            OpenButton(graphics.screen, self._on_open),
            ExitButton(graphics.screen, self._on_exit),
            StartSimulationButton(graphics.screen, app_state.start_simulation),
            SetupModeSelectorButtons(graphics, self._state),
            SetupModeStrategy(self._state, railway, graphics)
        ]
        
        railway.trains.load_state()

    def _on_save(self, dialog: bool = False):
        data = self._railway.to_dict()
        if dialog is False and self._state.app_state.filepath is not None:
            with open(self._state.app_state.filepath, 'w') as f:
                json.dump(data, f, indent=4)
            self._railway.mark_as_saved()
            return True
        
        root = tk.Tk()
        root.withdraw()
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save simulation as..."
        )
        if not filepath:
            return False # User cancelled save dialog
            
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
                
            self._state.app_state.filepath = filepath
            self._railway.mark_as_saved()
            return True
        except Exception as e:
            self._graphics.alert_component.show_alert(f"Failed to save file: {filepath}\nIssue with saving: {str(e)}")
            return False
        finally:
            root.destroy()
        
          
    def _confirm_unsaved_changes(self) -> bool:
        if self._railway.is_saved:
            return True
        
        result = messagebox.askyesnocancel("Unsaved Changes", 
            "You have unsaved changes. Save before proceeding?")
        if result is True: # Save
            saved = self._on_save()
            return saved
        elif result is False: # Don't Save
            return True
        else:
            return False
        
    def _on_exit(self):
        contin = self._confirm_unsaved_changes()
        
        if contin:
            self._state.app_state.exit()
        
    def _on_open(self):
        contin = self._confirm_unsaved_changes()
        if not contin:
            return None
        root = tk.Tk()
        root.withdraw()
        try:
            filepath = filedialog.askopenfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Open simulation from..."
            )
            if not filepath:
                return None

            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._railway.replace_from_dict(data)
            self._state.app_state.filepath = filepath
        except Exception as e:
            self._graphics.alert_component.show_alert(f"Failed to load file: {filepath}\nIssue with loading: {str(e)}")
            self._state.app_state.filepath = None
        finally:
            root.destroy()