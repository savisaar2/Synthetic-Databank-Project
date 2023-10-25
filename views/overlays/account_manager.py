from customtkinter import CTkFrame, CTkLabel, CTkScrollableFrame, CTkButton

class AccountMgmtView(CTkFrame):
    def __init__(self, root, *args, **kwargs):
        """
        Initialise the AccountMgmt overlay of the application.

        This class represents the AccountMgmtView overlay of the application.
        It renders the interactive widgets on the frontend of the application.

        Parameters
        ----------
        root : Root
            The applicaiton's root instance.
        """
        super().__init__(root, *args, **kwargs)
        self._setup_page()

    def _setup_page(self):
        """Renders the widgets on the AccountMgmtView."""
        self.overlay_frame = CTkFrame(self.master)
        self.overlay_frame.place(
            relx=0.5, rely=0.5, anchor="center",
            relwidth=1, relheight=1
        )
        self.overlay_frame.lower()

        # Define a title for overlay.
        self.title_label = self.create_label(self.overlay_frame, "Global Accounts Manager", ("Arial", 24), width=230, side="top", pady=20)

        # Define a content frame for widgets.
        self.content_frame = CTkScrollableFrame(self.overlay_frame)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header frame for the table.
        self.header_frame = CTkFrame(self.content_frame, corner_radius=0, fg_color="#336AA0")
        self.header_frame.pack(side="top", fill="x")

        # Content frame for the table.
        self.table_frame = CTkFrame(self.content_frame, fg_color="gray20")
        self.table_frame.pack(fill="x", expand=True, pady=0, anchor="n")

        # Define our headers for the table.
        self.firstname_heading = self.create_label(self.header_frame, "Firstname", ("Arial", 16))
        self.lastname_heading = self.create_label(self.header_frame, "Lastname", ("Arial", 16))
        self.username_heading = self.create_label(self.header_frame, "Username", ("Arial", 16))
        self.role_heading = self.create_label(self.header_frame, "Role", ("Arial", 16))
        self.initials_heading = self.create_label(self.header_frame, "Initials", ("Arial", 16), width=30)
        self.email_heading = self.create_label(self.header_frame, "Email", ("Arial", 16), width=260)
        self.actions_heading = self.create_label(self.header_frame, "Actions", ("Arial", 16), width=120)

        # Define button frame and add cancel and new user button to frame.
        button_frame = CTkFrame(self.overlay_frame)
        button_frame.pack(pady=(0, 10), padx=20, fill="x")
        self.cancel_button = self.create_button(button_frame, "Back")
        self.new_user_button = self.create_button(button_frame, "New User", side="right")

    def create_label(self, parent_frame, text, font=None, width=100, side="left", pady=10):
        """
        Create a label widget.
        """
        label = CTkLabel(parent_frame, text=text, font=font, width=width)
        label.pack(side=side, padx=5, pady=pady)
        return label

    def create_button(self, frame, text, width=150, height=40, side="left", color=None, padx=5, pady=5):
        """
        Create a button widget.
        """
        button = CTkButton(frame, corner_radius=5, text=text, height=height, width=width, fg_color=color)
        button.pack(side=side, padx=padx, pady=pady)
        return button

    def populate_user_accounts(self, accounts):
        # Initialise lists to store row frames, separator frames, delete buttons, and edit buttons.
        row_frames = []
        separator_frames = []
        self.delete_buttons = []
        self.edit_buttons = []

        # Clear any existing widgets within the table frame.
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # Loop through the user accounts and create a row for each user.
        for i, user in enumerate(accounts, start=1):
            # Create a frame for each row.
            row_frame = CTkFrame(self.table_frame, fg_color="transparent")
            row_frames.append(row_frame)

            # Create a separator line between rows.
            separator = CTkFrame(self.table_frame, height=1, fg_color="gray30")
            separator_frames.append(separator)

            # Create labels to display user information.
            # TODO: Might remove variables (unused).
            firstname_label = self.create_label(row_frame, user["firstname"])
            lastname_label = self.create_label(row_frame, user["lastname"])
            username_label = self.create_label(row_frame, user["username"])
            role_label = self.create_label(row_frame, user["role"])
            initials_label = self.create_label(row_frame, user["initials"], width=30)
            email_label = self.create_label(row_frame, user["email"], width=260)

            # Create edit and delete buttons for each row.
            edit_button = self.create_button(row_frame, "Edit", width=60, padx=10)
            delete_button = self.create_button(row_frame, "Delete", width=60, color="red", padx=10)

            # Store the delete and edit buttons in their respective lists.
            self.delete_buttons.append(delete_button)
            self.edit_buttons.append(edit_button)

        # Pack rows and separators within the table frame.
        for i, (row_frame, separator_frame) in enumerate(zip(row_frames, separator_frames)):
            row_frame.pack(side="top", fill="x", expand=False, pady=5)
            
            # Check if not the last item and add a separator.
            if i < len(row_frames) - 1:
                separator_frame.pack(side="top", fill="x")


    def remove_frame(self, frame):
        """
        Remove specified frame from view.

        Will be used to remove user row from accounts list.
        """
        frame.destroy()

    def show_view(self):
        """Shows the AccountMgmtView overlay."""
        self.overlay_frame.lift()

    def hide_view(self):
        """Hides the AccountMgmtView overlay."""
        self.overlay_frame.lower()