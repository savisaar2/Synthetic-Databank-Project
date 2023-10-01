from tkinter import ttk
from customtkinter import CTkFrame, CTkFont, CTkLabel, CTkEntry, CTkButton, CENTER, CTkScrollbar, CTkTextbox
from .base import BaseView

class LibraryView(BaseView):
    def __init__(self, root, *args, **kwargs):
        """
        Initialise the Library view of the application.

        This class represents the LibraryView page of the application.
        It renders the interactive widgets on the frontend of the application.

        Parameters
        ----------
        root : Root
            The applicaiton's root instance.
        """
        # Pass some base title and description to our BaseView class.
        super().__init__(root, "Choose", "Pick or Import an Existing Dataset.", *args, **kwargs)
        self._render_page()

    def _render_page(self):
        """Renders widgets on the LibraryView page."""
        content_frame = self._create_frame(parent_frame=self, padx=20, pady=(0, 20), fill="both", expand=True, color="#242424")
        
        # Define our containers for each section.
        row_1 = self._create_frame(parent_frame=content_frame)
        row_2 = self._create_frame(parent_frame=content_frame, pady=10)
        self.row_3 = self._create_frame(parent_frame=content_frame)
        row_4 = self._create_frame(parent_frame=content_frame, pady=(10, 0))

        # Configure and pack search label, entry and buttons to first row 1.
        self.search_label = self._create_label(row_1, str.upper("search"), "left")
        self.search_input = self._create_entry(row_1, "left")
        self.import_button = self._create_button(row_1, "Import", "left")
        self.new_button = self._create_button(row_1, "New", "left")

        self.tree_view = self._create_treeview(row_2)                   # Render treeview on row 2.
        self.dataset_meta = self._create_label(self.row_3, "", height=140)   # Render metadata on row 3.

        # Render status message when dataset is loaded or not loaded into memory.
        self.dataset_status = self._create_label(row_4, "No Dataset Loaded", height=50, font=CTkFont(size=17, weight="normal"), color="red", anchor="n", fill="x")

    def _create_treeview(self, frame):
        """
        Renders a treeview widget with specified parameters. Then returns the object 
        to the calling variable.
        """
        # Initlise style and configure style.
        style = ttk.Style()
        style.theme_use("clam") # Need to define a default theme.

        # Customise treeview body section.
        style.configure("Treeview",
            background="gray20",
            fieldbackground="gray20",
            foreground="white"
        )
        
        # Customise treeview headings section.
        style.configure("Treeview.Heading",
            foreground="white",
            background="#336AA0",
            font=("Arial", 10)
        )

        # Remove border from treeview and define row selection color.
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
        style.map("Treeview", background=[("selected", "#336aa0")])

        # Define configure and pack the initial treeview.
        tree_view = ttk.Treeview(frame, columns=("Name", "Size"), show="headings", selectmode="browse", height=10)
        tree_view.heading("Name", text="Name")
        tree_view.heading("Size", text="Size")
        tree_view.column("Name", width=500, stretch=True)
        tree_view.column("Size", width=100, stretch=True)

        # Setup vertical scrolling when treeview overflows.
        scrollbar = CTkScrollbar(frame, orientation="vertical", command=tree_view.yview)
        tree_view.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Pack last for rendering issues.
        tree_view.pack(fill="x", padx=20, pady=10)

        # Returns tree_view widget.
        return tree_view
    
    def populate_treeview(self, file_list=None):
        self._clear_dataset_listing()
        for file in file_list:
            name, size = file
            self.tree_view.insert("", "end", values=(name, size))

    def _clear_dataset_listing(self): 
        for item in self.tree_view.get_children(): 
            self.tree_view.delete(item)

    def update_metadata_display(self, metadata):
        # Clear the existing metadata frame content
        for widget in self.row_3.winfo_children():
            widget.destroy()

        if metadata:
            source = metadata.get("Source", "")
            description = metadata.get("Description", "")

            metadata_text = self._create_textbox(self.row_3, height=140, source=source, description=description)

    def _create_frame(self, parent_frame, padx=0, pady=0, fill="x", expand=False, color="gray20"):
        """
        Renders a frame widget with specified parameters. Then returns the object 
        to the calling variable.
        """
        frame = CTkFrame(parent_frame, fg_color=color)
        frame.pack(fill=fill, padx=padx, pady=pady, expand=expand)
        return frame
    
    def _create_label(self, frame, text="Text Here", side=None, height=100, font=None, color="white", anchor="w", fill=None):
        """
        Renders a label widget with specified parameters. Then returns the object 
        to the calling variable.
        """
        label = CTkLabel(frame, text=text, font=font, height=height, text_color=color)
        label.pack(padx=20, anchor=anchor, side=side, fill=fill)
        return label
    
    def _create_textbox(self, frame, height, source, description):
        # Source and description
        metadata_text = CTkTextbox(frame, wrap="word", fg_color="gray20", height=height)
        metadata_text.insert("1.0", f"Source: {source}\n\nDescription: {description}")
        metadata_text.configure(state="disabled")
        metadata_text.pack(side="left", fill="both", expand=True, padx=10)
        return metadata_text

    def _create_entry(self, frame, side):
        """
        Renders a entry widget with specified parameters. Then returns the object 
        to the calling variable.
        """
        entry = CTkEntry(frame, height=45, border_width=1)
        entry.pack(side=side, expand=True, fill="x", padx=10)
        return entry
    
    def _create_button(self, frame, text="Text Here", side="top"):
        """
        Renders a button widget with specified parameters. Then returns the object 
        to the calling variable.
        """
        button = CTkButton(frame, corner_radius=5, height=40, image="", border_spacing=10, text=text, anchor="n")
        button.pack(side=side, fill="x", padx=5)
        return button