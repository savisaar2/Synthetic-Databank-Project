from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkOptionMenu
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
        self._setup_page()
        self.variables = {}

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
        self.add_col_button.grid(row=0, column=3, padx=(0, 2), pady=(8, 8))

        # Action menu selector
        self.action_selection_menu = self._drop_down_menu_template(self.frame_1,"Select Column Type", ["Integer", "Float", "Categorical"],
                                                                  None, col_pos=0, row_pos=0)

    def _action_selection_callback(self, choice):
        self.variables["action"] = choice

        match choice:
            case "Integer":
                self.pos_1_menu = self._drop_down_menu_template(self.frame_1,"Select Column Type", ["Add Integer", "Add Float", "Add Categorical"],
                                                                            None, col_pos=0, row_pos=0)
            case "Float":
                self.pos_1_menu = self._drop_down_menu_template(self.frame_1,"Select Column Type", ["Add Integer", "Add Float", "Add Categorical"],
                                                                            None, col_pos=0, row_pos=0)
            case "Categorical":
                self.pos_1_menu = self._drop_down_menu_template(self.frame_1,"Select Column Type", ["Add Integer", "Add Float", "Add Categorical"],
                                                                            None, col_pos=0, row_pos=0)



    def show_view(self):
        """Shows the AccountEditorView overlay."""
        self.overlay_frame.lift()

    def hide_view(self):
        """Hides the AccountEditorView overlay."""
        self.overlay_frame.lower()

    def _drop_down_menu_template(self, frame, start_text:str, menu_options:list, command_func, col_pos:int, row_pos:int=0):    
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
            command=command_func,
            variable=StringVar(value=start_text)
            )
        drop_down_menu.grid(row=row_pos, column=col_pos, padx=(8, 8), pady=(8, 8))
        return drop_down_menu