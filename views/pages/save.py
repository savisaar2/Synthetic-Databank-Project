from customtkinter import CTkFrame, CTkTabview, CTkLabel, CTkTextbox, CTkEntry, CTkButton, CTkCheckBox
from .base import BaseView

class SaveView(BaseView):
    def __init__(self, root, *args, **kwargs):
        """
        Initialise the Save view of the application.

        This class represents the SaveView page of the application.
        It renders the interactive widgets on the frontend of the application.

        Parameters
        ----------
        root : Root
            The applicaiton's root instance.
        """
        # Pass some base title and description to our BaseView class.
        super().__init__(
            root, "Save & Export", "Save your dataset or export it for external consumption.", *args, **kwargs
            )
        self._render_page()

    def _render_page(self):
        """Renders widgets on the SaveView page."""
        self.two_panel_tabview = CTkTabview(master=self, fg_color="gray20", width=744, height=563)
        self.two_panel_tabview.add("Save")
        self.two_panel_tabview.add("Export")
        self.two_panel_tabview.pack()

        # Save panel
        self.save_frame = CTkFrame(self.two_panel_tabview.tab("Save"), fg_color="transparent")
        self.save_frame.pack(expand=True, padx=20, pady=20)
        self.save_desc_frame = CTkFrame(self.save_frame, fg_color="transparent")
        self.save_desc_frame.pack(anchor="center")
        self.save_desc_label = CTkLabel(self.save_desc_frame, text="Description:", font=("Arial", 18))
        self.save_desc_label.pack(side="top", anchor="w")
        self.save_description_entry = CTkTextbox(
            self.save_desc_frame, border_width=2, border_color="#575b5e", fg_color="#343638", 
            corner_radius=5, font=("Arial", 16), width=300, height=200
            )
        self.save_description_entry.pack(side="bottom")
        self.save_source_frame = CTkFrame(self.save_frame, fg_color="transparent")
        self.save_source_frame.pack(pady=20)
        self.save_source_label = CTkLabel(self.save_source_frame, text="Source:", font=("Arial", 18))
        self.save_source_label.pack(side="top", anchor="w")
        self.save_source_entry = CTkEntry(self.save_source_frame, corner_radius=5, font=("Arial", 16), width=300)
        self.save_source_entry.pack(side="bottom")
        self.save_button_frame = CTkFrame(self.save_frame, fg_color="transparent")
        self.save_button_frame.pack(pady=10)
        self.save_button = CTkButton(
            self.save_button_frame, corner_radius=5, text="Save", font=("Arial", 16), width=150, height=40
            )
        self.save_button.pack(side="left", padx=5)
        self.save_as_button = CTkButton(
            self.save_button_frame, corner_radius=5, text="Save As", font=("Arial", 16), width=150, height=40
            )
        self.save_as_button.pack(side="left", padx=5)

        # Export panel
        self.export_frame = CTkFrame(self.two_panel_tabview.tab("Export"), fg_color="transparent")
        self.export_frame.pack(expand=True, padx=20, pady=20)
        self.export_metadata_frame = CTkFrame(self.export_frame, fg_color="transparent")
        self.export_metadata_frame.pack(anchor="center")
        self.export_metadata_checkbox = CTkCheckBox(
            self.export_metadata_frame, text="Export Metadata In Addition To Dataset", font=("Arial", 16)
            )
        self.export_metadata_checkbox.pack(pady=20)
        self.export_desc_frame = CTkFrame(self.export_frame, fg_color="transparent")
        self.export_desc_label = CTkLabel(self.export_desc_frame, text="Description:", font=("Arial", 18))
        self.export_desc_label.pack(side="top", anchor="w")
        self.export_desc_entry = CTkTextbox(
            self.export_desc_frame, border_width=2, border_color="#575b5e", fg_color="#343638", corner_radius=5, 
            font=("Arial", 16), width=300,
            )
        self.export_desc_entry.pack(side="bottom")
        self.export_source_frame = CTkFrame(self.export_frame, fg_color="transparent")
        self.export_source_label = CTkLabel(self.export_source_frame, text="Source:", font=("Arial", 18))
        self.export_source_label.pack(side="top", anchor="w")
        self.export_source_entry = CTkEntry(self.export_source_frame, corner_radius=5, font=("Arial", 16), width=300)
        self.export_source_entry.pack(side="bottom")
        self.export_button_frame = CTkFrame(self.export_frame, fg_color="transparent")
        self.export_button_frame.pack(pady=10)
        self.export_button = CTkButton(
            self.export_button_frame, corner_radius=5, text="Export", font=("Arial", 16), width=150, height=40
            )
        self.export_button.pack(side="left", padx=5)

    def get_export_metadata_checkbox_state(self): 
        """_summary_
        """
        return self.export_metadata_checkbox.get()
    
    def hide_metadata_widgets(self): 
        """_summary_
        """
        self.export_desc_frame.pack_forget()
        self.export_source_frame.pack_forget()

    def show_metadata_widgets(self):
        """_summary_
        """
        self.export_button_frame.pack_forget() # hacky
        self.export_desc_frame.pack(anchor="center")
        self.export_source_frame.pack(pady=20)
        self.export_button_frame.pack(pady=10)