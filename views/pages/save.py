from customtkinter import CTkFrame, CTkTabview, CTkLabel, CTkTextbox, CTkEntry, CTkButton, CTkCheckBox, END, filedialog
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
        self.save_frame.pack(expand=True, fill="x", padx=20, pady=20)
        self.save_name_frame = CTkFrame(self.save_frame, fg_color="transparent")
        self.save_name_frame.pack(anchor="center")
        self.save_name_label = CTkLabel(self.save_name_frame, text="Name:", font=("Arial", 18))
        self.save_name_label.pack(side="top", anchor="w")
        self.save_name_entry = CTkEntry(self.save_name_frame, corner_radius=5, font=("Arial", 16), width=300)
        self.save_name_entry.pack(side="bottom")
        self.save_desc_frame = CTkFrame(self.save_frame, fg_color="transparent")
        self.save_desc_frame.pack(anchor="center", pady=(20,0))
        self.save_desc_label = CTkLabel(self.save_desc_frame, text="Description:", font=("Arial", 18))
        self.save_desc_label.pack(side="top", anchor="w")
        self.save_desc_entry = CTkTextbox(
            self.save_desc_frame, border_width=2, border_color="#575b5e", fg_color="#343638", 
            corner_radius=5, font=("Arial", 16), width=300, height=200
            )
        self.save_desc_entry.pack(side="bottom")
        self.save_source_frame = CTkFrame(self.save_frame, fg_color="transparent")
        self.save_source_frame.pack(pady=20)
        self.save_source_label = CTkLabel(self.save_source_frame, text="Source:", font=("Arial", 18))
        self.save_source_label.pack(side="top", anchor="w")
        self.save_source_entry = CTkEntry(self.save_source_frame, corner_radius=5, font=("Arial", 16), width=300)
        self.save_source_entry.pack(side="bottom")
        self.save_button_frame = CTkFrame(self.save_frame, fg_color="transparent")
        self.save_button_frame.pack(expand=True, fill="x", pady=10)
        self.save_button = CTkButton(
            self.save_button_frame, corner_radius=5, text="Overwrite", font=("Arial", 16), width=150, height=40
            )
        self.save_button.pack(expand=True, fill="x", padx=300)

        # Export panel
        self.export_frame = CTkFrame(self.two_panel_tabview.tab("Export"), fg_color="transparent")
        self.export_frame.pack(expand=True, fill="x", padx=20, pady=20)
        self.export_name_frame = CTkFrame(self.export_frame, fg_color="transparent")
        self.export_name_label = CTkLabel(self.export_name_frame, text="Name:", font=("Arial", 18))
        self.export_name_label.pack(side="top", anchor="w")
        self.export_name_entry = CTkEntry(self.export_name_frame, corner_radius=5, font=("Arial", 16), width=300)
        self.export_name_entry.pack(side="bottom")
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
            font=("Arial", 16), width=300, height=136
            )
        self.export_desc_entry.pack(side="bottom")
        self.export_source_frame = CTkFrame(self.export_frame, fg_color="transparent")
        self.export_source_label = CTkLabel(self.export_source_frame, text="Source:", font=("Arial", 18))
        self.export_source_label.pack(side="top", anchor="w")
        self.export_source_entry = CTkEntry(self.export_source_frame, corner_radius=5, font=("Arial", 16), width=300)
        self.export_source_entry.pack(side="bottom")
        self.export_button_frame = CTkFrame(self.export_frame, fg_color="transparent")
        self.export_button_frame.pack(expand=True, fill="x", pady=10)
        self.export_button = CTkButton(
            self.export_button_frame, corner_radius=5, text="Export", font=("Arial", 16), width=150, height=40
            )
        self.export_button.pack(expand=True, fill="x", padx=300)

    def show_export_dialogue(self, file_name):
        """Return full path (dir and file_name).

        Args:
            file_name (str): given name by user in entry widget
        """
        new_file = filedialog.asksaveasfilename(
            confirmoverwrite=True, 
            initialfile=file_name, 
            filetypes=[("CSV Files", "*.csv")]
        )
        return new_file

    def get_export_metadata_checkbox_state(self): 
        """_summary_
        """
        return self.export_metadata_checkbox.get()
    
    def get_name_entry(self, mode): 
        """Get the string value in self.save_name_entry or self.export_name_entry for different purposes.

        Args:
            mode (str): "Overwrite", "Save As" or "Export"

        Returns:
            str: value in text entry box
        """
        if mode == "Overwrite" or mode == "Save As":
            return self.save_name_entry.get()
        elif mode == "Export": 
            return self.export_name_entry.get()
    
    def get_desc_entry(self, mode): 
        """Get the string value in self.save_desc_entry

        Args:
            mode (str): "Overwrite", "Save As" or "Export"

        Returns:
            str: value in text entry box
        """
        if mode == "Overwrite" or mode == "Save As":
            return self.save_desc_entry.get("1.0", END)
        elif mode == "Export": 
            return self.export_desc_entry.get("1.0", END)
    
    def get_source_entry(self, mode): 
        """Get the string value in self.save_source_entry or self.export_source_entry
        depending on mode.

        Args:
            mode (str): "Overwrite", "Save As" or "Export"

        Returns:
            str: value in text entry box
        """
        if mode == "Overwrite" or mode == "Save As": 
            return self.save_source_entry.get()
        elif mode == "Export": 
            return self.export_source_entry.get()
    
    def change_save_button_text(self, mode): 
        """_summary_
        """
        if mode == "Save As":
            self.save_button.configure(text="Save As")
        elif mode == "Overwrite": 
            self.save_button.configure(text="Overwrite")

    def get_save_button_mode(self): 
        """Either return "Overwrite" or "Save As" i.e. mode of the save button.
        """
        return self.save_button.cget("text")
    
    def hide_metadata_widgets(self): 
        """_summary_
        """
        self.export_name_frame.pack_forget()
        self.export_desc_frame.pack_forget()
        self.export_source_frame.pack_forget()

    def show_metadata_widgets(self):
        """_summary_
        """
        self.export_button_frame.pack_forget() # hacky
        self.export_name_frame.pack(anchor="center")
        self.export_desc_frame.pack(anchor="center", pady=(20,0))
        self.export_source_frame.pack(pady=20)
        self.export_button_frame.pack(pady=10)

    def populate_metadata_widgets(self, name, description, source): 
        """_summary_
        """
        self.save_name_entry.delete(0, END)
        self.save_desc_entry.delete('1.0', END)
        self.save_source_entry.delete(0, END)
        self.export_name_entry.delete(0, END)
        self.export_desc_entry.delete('1.0', END)
        self.export_source_entry.delete(0, END)
        self.save_name_entry.insert(0, name)
        self.save_desc_entry.insert(END, description)
        self.save_source_entry.insert(0, source)
        self.export_name_entry.insert(0, name)
        self.export_desc_entry.insert(END, description)
        self.export_source_entry.insert(0, source)

    def display_save_success(self, msg):
        message = CTkLabel(self.save_button_frame, text=msg, height=40)
        # Place the label in the center of the save_button_frame
        message.place(relx=0.5, rely=0.5, anchor="center")
        # Schedule a function to destroy the label after 3000 milliseconds (3 seconds)
        self.save_button_frame.after(3000, message.destroy)

    def display_export_success(self, msg):
        message = CTkLabel(self.export_button_frame, text=msg, height=40)
        # Place the label in the center of the save_button_frame
        message.place(relx=0.5, rely=0.5, anchor="center")
        # Schedule a function to destroy the label after 3000 milliseconds (3 seconds)
        self.export_button_frame.after(3000, message.destroy)
