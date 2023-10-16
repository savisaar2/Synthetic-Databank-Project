from customtkinter import CTkFrame, CTkLabel, CTkOptionMenu, CTkButton, CTkEntry, CTkCanvas, CTkScrollbar, CTkTextbox
from .base import BaseView

class SampleView(BaseView):
    def __init__(self, root, *args, **kwargs):
        """
        Initialise the Sample view of the application.

        This class represents the SampleView page of the application.
        It renders the interactive widgets on the frontend of the application.

        Parameters
        ----------
        root : Root
            The applicaiton's root instance.
        """
        # Pass some base title and description to our BaseView class.
        super().__init__(root, "Sample", "Create a Sample of your Dataset.", *args, **kwargs)
        self._render_page()
        self._render_rollback()

    def _render_page(self):
        """Renders widgets on the SampleView page."""
        self.parent_frame = CTkFrame(self, fg_color="gray20")
        self.parent_frame.pack(fill="both", pady=(0, 20), padx=20, expand=True)

        # Sampling options
        self.s_frame = CTkFrame(self.parent_frame, fg_color="transparent")
        self.s_frame.pack(fill='x', pady=(20, 0), padx=20)
        self.algorithm_label = CTkLabel(self.s_frame, text="Sampling Algorithm:", anchor="w")
        self.algorithm_label.pack(side="left", padx=(8, 0))
        self.sampling_algo_options = [
            "------", "Simple Random", "Stratified", "Systematic", "Under", "Over"
            ]
        self.sampling_algo_menu = CTkOptionMenu(
            self.s_frame, fg_color="gray10", width=3, values=self.sampling_algo_options, 
            command=lambda option: self.reconfig_widgets(option, "sampling")
            )
        self.sampling_algo_menu.pack(side="left", padx=(8, 0))

        # Simple Random - sub widgets
        self.sample_size_label = CTkLabel(self.s_frame, text="Sample Size:", anchor="w")
        self.sample_size_entry = CTkEntry(self.s_frame, corner_radius=5, width=50, state="disabled")

        # Stratified - sub widgets
        self.num_of_splits_label = CTkLabel(self.s_frame, text="Number of Splits:", anchor="w")
        self.num_of_splits_entry = CTkEntry(self.s_frame, corner_radius=5, width=50, state="disabled")

        # Systematic - sub widgets 
        self.sampling_interval_label = CTkLabel(self.s_frame, text="Sampling Interval:", anchor="w")
        self.sampling_interval_entry = CTkEntry(self.s_frame, corner_radius=5, width=50, state="disabled")

        # Common widgets - used by stratified, under, over.
        self.dependant_col_label = CTkLabel(self.s_frame, text="Dependent Column:", anchor="w")
        self.dependant_col_menu = CTkOptionMenu(
            self.s_frame, fg_color="gray10", width=3, values=("------",), 
            command=lambda option: self.reconfig_widgets(option, "sampling")
        )
        # Big Button
        self.run = CTkButton(
            self.s_frame, text="Run", corner_radius=5, border_spacing=5, anchor="center", state="disabled"
            )
        self.run.pack(side="right", padx=(8, 8))

        # Widget toggle groupings
        self.all_widgets = [
            self.sample_size_label, self.sample_size_entry, self.num_of_splits_label, 
            self.num_of_splits_entry, self.sampling_interval_label, self.sampling_interval_entry, 
            self.dependant_col_label, self.dependant_col_menu
            ]
        
        self.simple_widgets = [
            self.sample_size_label, self.sample_size_entry
        ]

        self.stratified_widgets = [
            self.num_of_splits_label, self.num_of_splits_entry, self.dependant_col_label, self.dependant_col_menu
        ]

        self.systematic_widgets = [
            self.sampling_interval_label, self.sampling_interval_entry
        ]

        self.under_over_widgets = [
            self.dependant_col_label, self.dependant_col_menu
        ]

    def _render_rollback(self):
        self.rollback_label = CTkLabel(self, text="Rollback", anchor="w")
        self.rollback_label.pack(padx=30, pady=(0, 10), fill="both")
        
        self.rollback_frame = CTkFrame(self, fg_color="transparent") 
        self.rollback_frame.pack(fill="x", anchor="nw", pady=(0, 10), padx=0, expand=True) 
        
        self.rb_inner_right = CTkFrame(self.rollback_frame, fg_color="gray10", width=410, height=120) # Row group W x H
        self.rb_inner_right.pack(side="right", fill="both", padx=(10, 20), expand=True)
        
        self.rb_inner_top_left = CTkFrame(self.rollback_frame, fg_color="gray10") 
        self.rb_inner_top_left.pack(side="top", fill="both", padx=(20, 10), expand=True)
        
        self.sliding_snapshot_canvas = CTkCanvas(
            self.rb_inner_top_left, bg="gray10", highlightthickness=0, height=45 # sets sliding window width
            )
        self.sliding_snapshot_canvas.pack(fill="x", padx=10, pady=(10, 5))

        self.sliding_snapshot_x_scroll = CTkScrollbar(
            self.rb_inner_top_left, orientation="horizontal", command=self.sliding_snapshot_canvas.xview
            )
        self.sliding_snapshot_x_scroll.pack(fill="x", padx=10)
        self.sliding_snapshot_canvas.configure(xscrollcommand=self.sliding_snapshot_x_scroll.set)
        
        self.rb_inner_bottom_left = CTkFrame(self.rollback_frame, fg_color="transparent", height=10)
        self.rb_inner_bottom_left.pack(side="bottom", fill="both", padx=(20, 10), expand=True)
        
        self.revert_button = CTkButton(
            self.rb_inner_bottom_left, text="Revert", corner_radius=5, anchor="center", state="disabled"
            )
        self.revert_button.pack(side="left", anchor="nw", padx=10, pady=(10, 0))

    def display_snapshot_ui(self, items):
        """
        Display the appropriate snapshots as stored in per DATASET._SNAPSHOTS. 
        """
        self.sliding_snapshot_canvas.delete("all") # clear first

        block_width = 55 # Snapshot block width
        gap_width = 25 # Snapshot gap width

        vertical_center = self.sliding_snapshot_canvas.winfo_height() // 2

        next_x = 0

        for index, item in enumerate(items):
            item_x = next_x + (block_width // 2)

            # Create a rectangle with a unique tag to represent an individual snapshot.
            self.sliding_snapshot_canvas.create_rectangle(
                item_x - (block_width // 2), vertical_center - 45,
                item_x + (block_width // 2), vertical_center + 45,
                fill="#336AA0", outline="" # Non current blocks (blue)
            )

            self.sliding_snapshot_canvas.create_text(
                item_x, vertical_center, text=index #item["Name"]
            )

            next_x += block_width + gap_width

        current_item_x = next_x + (block_width // 2)

        next_x += gap_width

        self.sliding_snapshot_canvas.create_rectangle(
            current_item_x - (block_width // 2), vertical_center - 45,
            current_item_x + (block_width // 2), vertical_center + 45,
            fill="green", outline=""
        )
        
        self.sliding_snapshot_canvas.create_text(
            current_item_x, vertical_center, text=""
        )

        self.sliding_snapshot_canvas.update_idletasks()
        self.sliding_snapshot_canvas.configure(scrollregion=self.sliding_snapshot_canvas.bbox("all"))

    def display_specific_snapshot_info(self, name, desc, schedule_set, txt_color): 
        """_summary_

        Args:
            name (_type_): _description_
            desc (_type_): _description_
            schedule_set (_type_): _description_
        """
        for widget in self.rb_inner_right.winfo_children(): # Clear first
            widget.destroy()

        self._create_textbox(
            self.rb_inner_right, width=390, height=120, name=name, description=desc, txt_color=txt_color
            )

    def _create_textbox(self, frame, width, height, name, description, txt_color):
        snapshot_details = CTkTextbox(frame, wrap="word", fg_color="gray10", width=width, height=height)
        snapshot_details.insert("1.0", f"Name: {name}\n\nDescription: {description}")
        snapshot_details.configure(state="disabled", text_color=txt_color)
        snapshot_details.pack(side="left", fill="both", expand=True, padx=10)

    def refresh_sample_widgets(self, column_headers):
        """Populate / update the values of the dropdown menus view with appropriate column headers 
        of the working dataset.

        Args:
            column_headers (list): A list of column headers (str).
        """
        self.dependant_col_menu.configure(values=column_headers) 

    def reconfig_widgets(self, option, option_set): 
        """Toggle (disable or enable) the appropriate widget based on predefined conditions.

        Args:
            option (str): selected item of an options menu
            option_set (str): the specific options menu
        """
        def bulk_toggle(mode, list_of_widgets): 
            if mode == "off": 
                for w in list_of_widgets: 
                    w.configure(state="disabled")
            elif mode == "on": 
                for w in list_of_widgets: 
                    w.configure(state="normal")
            elif mode == "hide": 
                for w in list_of_widgets: 
                    w.pack_forget()
            elif mode == "show": 
                for w in list_of_widgets: 
                    w.pack(side="left", padx=(8, 0))
            elif mode == "reset_menu": 
                for w in list_of_widgets: 
                    w.set("------") 

        if option_set == "sampling": 
            match option: 
                case "------":
                    bulk_toggle("hide", self.all_widgets)
                case "Simple Random":
                    bulk_toggle("hide", [
                        widget for widget in self.all_widgets if widget not in self.simple_widgets
                        ])
                    bulk_toggle("show", self.simple_widgets)
                    bulk_toggle("off", [
                        widget for widget in self.all_widgets if widget not in self.simple_widgets
                    ])
                    bulk_toggle("on", self.simple_widgets)
                case "Stratified": 
                    bulk_toggle("hide", [
                        widget for widget in self.all_widgets if widget not in self.stratified_widgets
                        ])
                    bulk_toggle("show", self.stratified_widgets)
                    bulk_toggle("off", [
                        widget for widget in self.all_widgets if widget not in self.stratified_widgets
                    ])
                    bulk_toggle("on", self.stratified_widgets)
                case "Systematic": 
                    bulk_toggle("hide", [
                        widget for widget in self.all_widgets if widget not in self.systematic_widgets
                        ])
                    bulk_toggle("show", self.systematic_widgets)
                    bulk_toggle("off", [
                        widget for widget in self.all_widgets if widget not in self.systematic_widgets
                    ])
                    bulk_toggle("on", self.systematic_widgets)
                case "Under" | "Over": 
                    bulk_toggle("hide", [
                        widget for widget in self.all_widgets if widget not in self.under_over_widgets
                        ])
                    bulk_toggle("show", self.under_over_widgets)
                    bulk_toggle("off", [
                        widget for widget in self.all_widgets if widget not in self.under_over_widgets
                    ])
                    bulk_toggle("on", self.under_over_widgets)
                        