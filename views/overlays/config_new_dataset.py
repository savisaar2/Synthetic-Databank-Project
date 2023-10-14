from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkOptionMenu, CTkEntry
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
        self.variables = {}
        self.widget_list = []
        self._setup_page()

    def _setup_page(self):
        """Renders the widgets on the AccountEditorView."""
        self.overlay_frame = CTkFrame(self.master)
        self.overlay_frame.place(
            relx=0.5, rely=0.5, anchor="center",
            relwidth=1, relheight=1
        )
        self.overlay_frame.lower()

        self.logo_label = CTkLabel(self.overlay_frame, text="Configure New Dataset")
        self.logo_label.pack(padx=100,pady=10)

        self.frame_1 = CTkFrame(self.overlay_frame, fg_color="gray20", border_color="white")
        self.frame_1.pack(fill="both", padx=150, pady=(100, 0))
        self.frame_2 = CTkFrame(self.overlay_frame, fg_color="gray20", border_color="white")
        self.frame_2.pack(fill="both", padx=150, pady=(20,100))

        self.add_col_button = CTkButton(
            self.frame_1, 
            text="Add Column", 
            corner_radius=5, 
            border_spacing=5, 
            anchor="center", 
            state="disabled",
            )
        self.add_col_button.grid(row=0, column=3, padx=(8, 2), pady=(8, 8))

        # Action menu selector
        self.action_selection_menu = self._drop_down_menu_template(self.frame_1,"Select Column Type", ["Integer", "Float", "Categorical"],
                                                                  self._action_selection_callback, col_pos=0, row_pos=0)

    def _action_selection_callback(self, choice):
        self.variables["action"] = choice
        self._refresh_menu_widgets(1)

        match choice:
            case "Integer":
                self.pos_1_entry = self._user_entry_box_template(self.frame_1, "Enter min integer value", None, 150, 1)
                self.pos_2_entry = self._user_entry_box_template(self.frame_1, "Enter max integer value", None, 150, 2)
            case "Float":
                self.pos_1_entry = self._user_entry_box_template(self.frame_1, "Enter min float value", None, 150, 1)
                self.pos_2_entry = self._user_entry_box_template(self.frame_1, "Enter max float value", None, 150, 1)
            case "Categorical":
                self.pos_1_menu = self._drop_down_menu_template(self.frame_1,
                                                                "Select Column Type", 
                                                                ["first_name", "last_name", "address",
                                                                "Add Categorical", "date_of_birth"],
                                                                None, col_pos=1, row_pos=0)



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