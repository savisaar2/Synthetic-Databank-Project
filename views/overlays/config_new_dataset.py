from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkOptionMenu, CTkEntry, CTkScrollableFrame
from tkinter import StringVar

class ConfigNewDatasetView(CTkFrame):
    def __init__(self, root, *args, **kwargs):
        """
        Initialise the ConfigNewDataset overlay of the application.

        This class represents the ConfigNewDataset overlay of the application.
        It renders the interactive widgets on the frontend of the application.

        Parameters
        ----------
        root : Root
            The applicaiton's root instance.
        """
        super().__init__(root, *args, **kwargs)
        self.variables = {"action": "", "col_name": "", "arg_a": "", "arg_b": "", "rows": "" }
        self.widget_list = []
        self._setup_page()
        self.col_pos= -1

    def _setup_page(self):
        """Renders the widgets on the config new dataset overlay."""
        self.overlay_frame = CTkFrame(self.master)
        self.overlay_frame.place(
            relx=0.5, rely=0.5, anchor="center",
            relwidth=1, relheight=1
        )
        self.overlay_frame.lower()

        self.title_label = CTkLabel(self.overlay_frame, text="Configure New Dataset", font=("Arial", 24), anchor="center")
        self.title_label.pack(padx=100,pady=(50,0))

        self.frame_1 = CTkFrame(self.overlay_frame, fg_color="gray20")
        self.frame_1.pack(fill="both", padx=150, pady=(2, 0))
        self.config_col_label = CTkLabel(self.frame_1, text="Configure New Column", font=("Arial", 14, "bold"))
        self.config_col_label.pack(padx=8,pady=8, anchor='w')

        self.frame_2 = CTkFrame(self.overlay_frame, fg_color="gray20")
        self.frame_2.pack(fill="both", padx=150, pady=(2,2))

        self.frame_3 = CTkFrame(self.overlay_frame, fg_color="gray20")
        self.frame_3.pack(fill="both", padx=150, pady=(0,0))
        self.add_col_button = CTkButton(self.frame_3, text="Add Column", corner_radius=5, border_spacing=5, anchor="center", 
                                        state="disabled")
        self.add_col_button.pack(padx=8,pady=8, side="right")

        self.frame_4 = CTkFrame(self.overlay_frame, fg_color="gray20")
        self.frame_4.pack(fill="both", padx=150, pady=(20,0))
        self.dataset_config_settings_label = CTkLabel(self.frame_4, text="Dataset Configuration Settings", font=("Arial", 14, "bold"))
        self.dataset_config_settings_label.pack(padx=8,pady=8, side="left")
        entry_box_command = self.register(self._entry_box_rows_callback)
        self.rows_entry_box = CTkEntry(
            self.frame_4,
            corner_radius=5, 
            width=50,
            validate='key',
            validatecommand=(entry_box_command, '%P')
            ) 
        self.rows_entry_box.pack(padx=8,pady=8, side="right")
        self.rows_label = CTkLabel(self.frame_4, text="Rows:")
        self.rows_label.pack(padx=8,pady=8, side="right")

        self.frame_5 = CTkScrollableFrame(self.overlay_frame, fg_color="gray20", height=150)
        self.frame_5.pack(fill="both", padx=150, pady=(2,0))

        self.frame_6 = CTkFrame(self.overlay_frame, fg_color="gray20")
        self.frame_6.pack(fill="both", padx=150, pady=(2,50))
        self.confirm_button = CTkButton(self.frame_6, text="Confirm", corner_radius=5, border_spacing=5, anchor="center", state="disabled")
        self.confirm_button.pack(padx=8,pady=8, side="right")
        self.cancel_button = CTkButton(self.frame_6, text="Cancel", corner_radius=5, border_spacing=5, anchor="center")
        self.cancel_button.pack(padx=8,pady=8, side="right")

        # Action menu selector
        self.action_selection_menu = self._drop_down_menu_template(self.frame_2,"Select Column Type", ["Custom Integer Range", "Custom Float Range", "Categorical"],
                                                                  self._action_selection_callback, col_pos=0, row_pos=0)
    def _entry_box_rows_callback(self,choice):
        """Entry box for float callback function. Sets arg a as user choice.

            Args:
                choice (str): User selection via dropdown menu or entry box.
        """
        try:
            self.rows = int(choice)
            self.confirm_button.configure(state="normal")
        except ValueError:
            self.confirm_button.configure(state="disabled")
        return True

    def _action_selection_callback(self, choice):
        self.variables = {"action": "", "col_name": "", "arg_a": "", "arg_b": "", "rows": "" }
        self.variables["action"] = choice
        self._refresh_menu_widgets(1)
        
        self.pos_1_entry = self._user_entry_box_template(self.frame_2, "Enter Column Name", self._entry_box_standard_callback, 200, 1)

        match choice:
            case "Custom Integer Range":
                self.pos_2_entry = self._user_entry_box_template(self.frame_2, "Enter min integer value", self._entry_box_int_arg_a_callback, 150, 2)
                self.pos_3_entry = self._user_entry_box_template(self.frame_2, "Enter max integer value", self._entry_box_int_arg_b_callback, 150, 3)
            case "Custom Float Range":
                self.pos_1_entry = self._user_entry_box_template(self.frame_2, "Enter min float value", self._entry_box_float_arg_a_callback, 150, 2)
                self.pos_2_entry = self._user_entry_box_template(self.frame_2, "Enter max float value", self._entry_box_float_arg_b_callback, 150, 3)
            case "Categorical":
                self.pos_1_menu = self._drop_down_menu_template(self.frame_2,
                                                                "Select Column Type", 
                                                                ["first_name", "last_name", "address",
                                                                 "date_of_birth"],
                                                                self._categorical_callback, col_pos=2, row_pos=0)
    
    def _categorical_callback(self, choice):
        self.variables["arg_a"] = choice
        self.add_col_button.configure(state="normal")

    def _entry_box_standard_callback(self, choice):
        """Entry box for strings callback function. Sets arg a as user choice.

            Args:
                choice (str): User selection via dropdown menu or entry box.
        """
        match len(choice):
            case _ if len(choice) <= 20:
                self.variables["col_name"] = choice
                return True

    def _entry_box_float_arg_a_callback(self, choice):
        """Entry box for float callback function. Sets arg a as user choice.

            Args:
                choice (str): User selection via dropdown menu or entry box.
        """
        try:
            self.variables["arg_a"] = float(choice)
        except ValueError:
            self.add_col_button.configure(state="disabled")
        return True
    
    def _entry_box_float_arg_b_callback(self, choice):
        """Entry box for float callback function. Sets arg a as user choice.

            Args:
                choice (str): User selection via dropdown menu or entry box.
        """
        try:
            self.variables["arg_b"] = float(choice)
            if self.variables["arg_b"] > self.variables["arg_a"]:
                self.add_col_button.configure(state="normal")
        except ValueError:
            self.add_col_button.configure(state="disabled")
        return True
      
    def _entry_box_int_arg_a_callback(self, choice):
        """Entry box for float callback function. Sets arg a as user choice.

            Args:
                choice (str): User selection via dropdown menu or entry box.
        """
        try:
            self.variables["arg_a"] = int(choice)
        except ValueError:
            self.add_col_button.configure(state="disabled")
        return True
    
    def _entry_box_int_arg_b_callback(self, choice):
        """Entry box for int callback function. Sets arg a as user choice.

            Args:
                choice (str): User selection via dropdown menu or entry box.
        """
        try:
            self.variables["arg_b"] = int(choice)
            if self.variables["arg_b"] > self.variables["arg_a"]:
                self.add_col_button.configure(state="normal")
        except ValueError:
            self.add_col_button.configure(state="disabled")
        return True

    def show_view(self):
        """Shows the AccountEditorView overlay."""
        self.overlay_frame.lift()

    def hide_view(self):
        """Hides the AccountEditorView overlay."""
        self.overlay_frame.lower()

    def _drop_down_menu_template(self, frame, start_text:str, menu_options:list, callback, col_pos:int, row_pos:int=0):    
        """Drop down menu widget template.

        Args:
            frame (ctk fram obj): Frame to place drop down menu.
            start_text (str): Placeholder text of entry widget.
            menu_options (list): List of menu options.
            command_func (function): Callback function associated with widget.
            col_pos (int): Column position to place on grid.
            row_pos (int): Row position to place on grid.
            
        Returns:
            Ctk widget: A Ctk drop down menu widget object.
        """
        drop_down_menu = CTkOptionMenu(
            frame, 
            fg_color="gray10", 
            width=3, 
            values=menu_options, 
            command=callback,
            variable=StringVar(value=start_text)
            )
        drop_down_menu.grid(row=row_pos, column=col_pos, padx=(8, 8), pady=(8, 8))
        self.widget_list.append({"col_pos": col_pos, "widget": drop_down_menu})
        return drop_down_menu
    
    def _user_entry_box_template(self, frame, start_text:str, callback, width:int, col_pos:int, row_pos:int=0):
        """Entry box widget template.

        Args:
            frame (Ctk frame widget): Frame to place entry box widget
            start_text (str): Placeholder text of entry widget.
            callback (function): Callback function associated with widget.
            width (int): width of entry box
            col_pos (int): Column position to place on grid.
            row_pos (int): Row position to place on grid.

        Returns:
            Ctk widget: A Ctk entry box widget object.
        """
        entry_box_command = self.register(callback)
        user_entry_box = CTkEntry(
            frame,
            corner_radius=5, 
            width=width,
            validate='key',
            validatecommand=(entry_box_command, '%P')
            ) 
        user_entry_box.grid(column=col_pos, row=row_pos,  padx=(0, 2), pady=(8, 8), sticky="w")
        user_entry_box.configure(placeholder_text=start_text)
        self.widget_list.append({"col_pos": col_pos, "widget": user_entry_box})
        return user_entry_box
    
    def _refresh_menu_widgets(self, col_ref:int):
        """Method to refresh menu widget in manipulations frame.

        Args:
            col_ref (int): Refrence to widget column position.
        """
        # Refresh UI widget variables.
        self.add_col_button.configure(state="disabled")


        # Remove widgets from view based on column of current widget.
        match col_ref:
            case 1:
                for widget in self.widget_list:
                    if widget["col_pos"] != 0:
                        widget["widget"].grid_forget()
            case 2:
                for widget in self.widget_list:
                    if widget["col_pos"] != 1:
                        widget["widget"].grid_forget()
            case 3:
                for widget in self.widget_list:
                    if widget["col_pos"] != 1 and widget["col_pos"] != 2:
                        widget["widget"].grid_forget()
            case 4:
                for widget in self.widget_list:
                    if widget["col_pos"] != 1 and widget["col_pos"] != 2 and widget["col_pos"] != 3:
                        widget["widget"].grid_forget()
            case 5:
                for widget in self.widget_list:
                    if widget["col_pos"] != 1 and widget["col_pos"] != 2 and widget["col_pos"] != 3 and widget["col_pos"] != 4:
                        widget["widget"].grid_forget()

    def add_col_to_config(self):
        if self.add_col_button._state == "normal":
            self.col_pos += 1

            # col # label
            self.col_pos_label = CTkLabel(
                self.frame_5, 
                text=str(self.col_pos),
                )
            self.col_pos_label.grid(row=self.col_pos, column=0, padx=(8, 8), pady=(8, 0), sticky='w')

            # Label for scheduled manipulation outcome
            self.action_label = CTkLabel(
                self.frame_5, 
                text=self.variables["action"],
                )
            self.action_label.grid(row=self.col_pos, column=1, padx=(8, 8), pady=(8, 0), sticky='w')

            self.action_label = CTkLabel(
                self.frame_5, 
                text=self.variables["col_name"],
                )
            self.action_label.grid(row=self.col_pos, column=2, padx=(8, 8), pady=(8, 0), sticky='w')

            # Label for variables
            arg_a = self.variables["arg_a"]
            arg_b = self.variables["arg_b"]
            if arg_b == "":
                label_text = arg_a
            else:
                label_text = f"Min: {arg_a}, Max: {arg_b}"

            self.action_label = CTkLabel(
                self.frame_5, 
                text=label_text
                )
            self.action_label.grid(row=self.col_pos, column=3, padx=(8, 8), pady=(8, 0), sticky='w')

            self._refresh_menu_widgets(1)