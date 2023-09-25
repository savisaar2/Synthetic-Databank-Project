from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkOptionMenu, StringVar, CTkCheckBox
from .base import BaseView

class ManipulateView(BaseView):
    def __init__(self, root, *args, **kwargs):
        """
        Initialise the Manipulate view of the application.

        This class represents the ManipulateView page of the application.
        It renders the interactive widgets on the frontend of the application.

        Parameters
        ----------
        root : Root
            The applicaiton's root instance.
        """
        # Pass some base title and description to our BaseView class.
        super().__init__(root, "Manipulate", "Configure your Dataset.", *args, **kwargs)
        self._render_page()

    def _render_page(self):
        """Renders widgets on the ManipulateView page."""

        # Rollback frame and label
        self.rollback_frame = CTkFrame(self, fg_color="gray20")
        self.rollback_frame.pack(fill="both", pady=(0, 20), padx=20, expand=False)
        self.rollback_label = CTkLabel(self.rollback_frame, text="Rollback", anchor="w", font=("Arial", 14, "bold"))
        self.rollback_label.pack(side="left", padx=(8, 0))

        # Manipulations frame and label
        self.manipulations_frame = CTkFrame(self, fg_color="gray20")
        self.manipulations_frame.pack(fill="both", pady=(0, 20), padx=20, expand=False)
        self.manipulations_label = CTkLabel(self.manipulations_frame, text="Manipulations", anchor="w", font=("Arial", 14, "bold"))
        self.manipulations_label.pack(padx=(8, 0), pady=(0, 20), fill="both")

        # Action selection in manipulate frame
        self.action_label = CTkLabel(self.manipulations_frame, text="Action:", anchor="w")
        self.action_label.pack(side="left", padx=(10, 0))
        self.action_menu_var = StringVar(value="Select Manipulation")
        self.action_selector = ["Action1", "Action2", "Action3"]
        self.action_selection_menu = CTkOptionMenu(
            self.manipulations_frame, 
            fg_color="gray10", 
            width=3, 
            values=self.action_selector, 
            command=self.manipulation_action_callback,
            variable=self.action_menu_var
            )
        self.action_selection_menu.pack(side="left", padx=(10, 0))

        # 'to' label
        self.to_label = CTkLabel(self.manipulations_frame, text="to -->", anchor="w")
        self.to_label.pack(side="left", padx=(10, 0))   

        # Dataset Name selection in manipulate frame
        self.dataset_name_menu_var = StringVar(value="Select Dataset")
        self.dataset_name_selector = ["Current Dataset"]
        self.dataset_name_menu = CTkOptionMenu(
            self.manipulations_frame, 
            fg_color="gray10", 
            width=3, 
            values=self.dataset_name_selector, 
            command=self.dataset_name_select_callback,
            variable=self.dataset_name_menu_var
            )
        self.dataset_name_menu.pack(side="left", padx=(10, 0))

        # 'or' label
        self.or_label = CTkLabel(self.manipulations_frame, text="(OR)", anchor="w")
        self.or_label.pack(side="left", padx=(10, 0))       

        # Column index selection in manipulate frame
        self.column_label = CTkLabel(self.manipulations_frame, text="Column:", anchor="w")
        self.column_label.pack(side="left", padx=(10, 0))
        self.column_menu_var = StringVar(value="Select Column")
        self.column_selector = ["Col1", "Col2", "Col3", "Col4", "Col5"]
        self.column_selection_menu = CTkOptionMenu(
            self.manipulations_frame, 
            fg_color="gray10", 
            width=3, 
            values=self.column_selector, 
            variable=self.column_menu_var
            )
        self.column_selection_menu.pack(side="left", padx=(10, 0))

        # Schedule button in manipulate frame.
        self.schedule_button = CTkButton(
            self.manipulations_frame, text="Schedule", corner_radius=5, border_spacing=5, anchor="center", state="normal"
            )
        self.schedule_button.pack(side="right", padx=(8, 8), pady=(8,8))

        # Scheduler frame
        self.scheduler_frame = CTkFrame(self, fg_color="gray20")
        self.scheduler_frame.pack(fill="both", pady=(0, 20), padx=20, expand=False)
        self.scheduler_label = CTkLabel(self.scheduler_frame, text="Scheduler", anchor="w", font=("Arial", 14, "bold"))
        self.scheduler_label.pack(padx=(8, 0), pady=(0, 20), fill="both")

        # Generate button
        self.generate_button = CTkButton(
            self.scheduler_frame, 
            text="Generate", 
            corner_radius=5, 
            border_spacing=5, 
            anchor="center", 
            state="normal"
            )
        self.generate_button.pack(side="right", padx=(8, 8), pady=(8,8))

        # Step label
        self.step_label = CTkLabel(self.scheduler_frame, text="Step", anchor="w", font=("Arial", 14))
        self.step_label.pack(side="left", padx=(10, 0))

        # Manipulation label
        self.scheduler_manipulation_label = CTkLabel(self.scheduler_frame, text="Manipulation", anchor="w", font=("Arial", 14))
        self.scheduler_manipulation_label.pack(side="left", padx=(70, 0))

        # Variable label
        self.variable_label = CTkLabel(self.scheduler_frame, text="Variable", anchor="w", font=("Arial", 14))
        self.variable_label.pack(side="left", padx=(100, 0))

        # Outcome label
        self.outcome_label = CTkLabel(self.scheduler_frame, text="Outcome", anchor="w", font=("Arial", 14))
        self.outcome_label.pack(side="left", padx=(100, 0))


    def add_manipulation_to_scheduler(self):
        self.scheduler_item_frame = CTkFrame(self, fg_color="gray20")
        self.scheduler_item_frame.pack(fill="both", pady=(0, 20), padx=20, expand=False)

        # Checkbox
        self.step_checkbox = CTkCheckBox(self.scheduler_item_frame, text="", )
        self.step_checkbox.pack(side="left", padx=(10, 0))
        self.step_checkbox.select()

        # Name of scheduled manipulation
        self.manipulation_label_for_scheduler = CTkLabel(self.scheduler_item_frame, text=str(self.action_menu_var), anchor="w", font=("Arial", 14))
        self.manipulation_label_for_scheduler.pack(side="left")

        # Varible name for scheduled manipulation
        self.variable_label_for_scheduler = CTkLabel(self.scheduler_item_frame, text=str(self.dataset_name_menu_var), anchor="w", font=("Arial", 14))
        self.variable_label_for_scheduler.pack(side="left", padx=(116, 0))

    def dataset_name_select_callback(self, choice):
        self.dataset_name_menu_var = choice

    def manipulation_action_callback(self, choice):
        self.action_menu_var = choice