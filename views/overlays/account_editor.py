from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkTextbox, CTkButton, END, CTkOptionMenu

class AccountEditorView(CTkFrame):
    def __init__(self, root, new_account=False, *args, **kwargs):
        """
        Initialise the AccountEditor overlay of the application.

        This class represents the AccountEditorView overlay of the application.
        It renders the interactive widgets on the frontend of the application.

        Parameters
        ----------
        root : Root
            The applicaiton's root instance.
        """
        super().__init__(root, *args, **kwargs)
        self.new_account = new_account
        self._setup_page()

    def _setup_page(self):
        """Renders the widgets on the AccountEditorView."""
        self.overlay_frame = CTkFrame(self.master)
        self.overlay_frame.place(
            relx=0.5, rely=0.5, anchor="center",
            relwidth=1, relheight=1
        )
        self.overlay_frame.lower()

        # Define a title for overlay.
        self.title_label = CTkLabel(self.overlay_frame, text="New Account" if self.new_account else "Edit User Profile", font=("Arial", 24), anchor="center")
        self.title_label.pack(pady=20)

        # This is our containing frame for widget content.
        self.content_frame = CTkFrame(self.overlay_frame)
        self.content_frame.pack(fill="both", expand=False, padx=20, pady=20)

        # Frame holding all entry widgets.
        input_frame = CTkFrame(self.content_frame, fg_color="transparent")
        input_frame.pack(padx=20, pady=20)

        # Separate frames as 4 separate rows.
        row1_frame = CTkFrame(input_frame, corner_radius=0, fg_color="transparent")
        row2_frame = CTkFrame(input_frame, corner_radius=0, fg_color="transparent")
        row3_frame = CTkFrame(input_frame, corner_radius=0, fg_color="transparent")
        row4_frame = CTkFrame(input_frame, corner_radius=0, fg_color="transparent")

        # Row1 widgets.
        self.first_name_entry = self.create_field(row1_frame, "First Name:")
        self.last_name_entry = self.create_field(row1_frame, "Last Name:")
        self.username_entry = self.create_field(row1_frame, "Username:")

        # Row2 Widgets.
        self.initial_entry = self.create_field(row2_frame, "Initials:")
        self.department_entry = self.create_field(row2_frame, "Department:")
        self.office_entry = self.create_field(row2_frame, "Office:")

        # Row3 Widgets.
        self.email_entry = self.create_field(row3_frame, "Email:", width=250)
        blank = CTkLabel(row3_frame, width=120, text="", anchor="w")
        blank.pack(side="left", padx=5, pady=5)
        role_label = CTkLabel(row3_frame, width=80, text="Role:", anchor="w")
        role_label.pack(side="left", padx=5, pady=5)
        self.role_entry = CTkOptionMenu(row3_frame, values=["standard", "admin"])
        self.role_entry.pack(side="left", padx=5, pady=5)

        # Row4 Widgets.
        self.bio_entry = self.create_textbox(row4_frame, "Bio:", width=620)

        # Display all rows.
        row1_frame.pack(fill="both", expand=True, padx=10)
        row2_frame.pack(fill="both", expand=True, padx=10)
        row3_frame.pack(fill="both", expand=True, padx=10)
        row4_frame.pack(fill="both", expand=True, padx=10)

        # Frame holding all button widgets.
        buttons_frame = CTkFrame(self.content_frame, fg_color="transparent")
        buttons_frame.pack(padx=20, pady=20)

        # Button used to save profile data.
        self.save_button = self.create_button(buttons_frame, "Save")

        if self.new_account:
            password_label = CTkLabel(input_frame, width=80, text="User Password:", anchor="w")
            password_container = CTkFrame(input_frame, corner_radius=0, fg_color="transparent")
            self.password_entry = self.create_mask_field(password_container, "New Password")
            self.verify_password_entry = self.create_mask_field(password_container, "Verify New Password")
            password_label.pack(padx=5, pady=5)
            password_container.pack()
            self.cancel_button = self.create_button(buttons_frame, "Cancel")
        else:
            # Buttons for Done and Reset Pw.
            self.done_button = self.create_button(buttons_frame, "Done")
            self.reset_pw_button = self.create_button(buttons_frame, "Change Password")

    def create_field(self, parent_frame, label_text, width=140, height=28):
        """
        Create a entry widget.
        """
        label = CTkLabel(parent_frame, width=80, text=label_text, anchor="w")
        entry = CTkEntry(parent_frame, state="normal", width=width, border_width=1)
        label.pack(side="left", padx=5, pady=5)
        entry.pack(side="left", padx=5, pady=5)
        return entry

    def create_textbox(self, parent_frame, label_text, width=None):
        """
        Create a textbox widget.
        """
        label = CTkLabel(parent_frame, width=80, text=label_text, anchor="nw")
        entry = CTkTextbox(parent_frame, state="normal", width=width, fg_color="#353638", border_width=1)
        label.pack(fill="both", side="left", padx=5, pady=5)
        entry.pack(side="left", padx=5, pady=5)
        return entry
    
    def create_mask_field(self, parent_frame, placeholder, width=150, border_width=1):
        """
        Create a masked entry widget.
        """
        entry = CTkEntry(parent_frame, show="*", placeholder_text=placeholder, width=width, border_width=border_width)
        entry.pack(side="left", padx=5, pady=5)
        return entry
    
    def create_button(self, frame, text, width=150, height=40):
        """
        Create a button widget.
        """
        button = CTkButton(frame, corner_radius=5, text=text, font=("Arial", 16), width=width, height=height)
        button.pack(side="left", padx=5, pady=(0, 50))
        return button

    def populate_fields(self, profile):
        """
        Populates widgets with profile data.
        """
        # Defines our payload with entry widgets and expected values.
        fields_to_populate = {
            self.first_name_entry: profile["profile_info"]["first"],
            self.last_name_entry: profile["profile_info"]["last"],
            self.username_entry: profile["username"],
            self.initial_entry: profile["profile_info"]["initials"],
            self.department_entry: profile["profile_info"]["department"],
            self.office_entry: profile["profile_info"]["office"],
            self.email_entry: profile["profile_info"]["email"],
        }

        # Loop through dictionary and delete existing data and write new data.
        for field, value in fields_to_populate.items():
            field.delete(0, END)
            field.insert(0, value)

        # Textbox needs a different solution.
        self.bio_entry.delete(0.0, END)
        self.bio_entry.insert(0.0, profile["profile_info"]["bio"])
        self.role_entry.set(profile["role"])

    def show_view(self):
        """Shows the AccountEditorView overlay."""
        if self.new_account:
            # Define our widgets to be cleared.
            fields_to_clear = [
                self.first_name_entry, self.last_name_entry, self.username_entry,
                self.initial_entry, self.department_entry, self.office_entry,
                self.email_entry
            ]

            # Run clearing using loop.
            for field in fields_to_clear:
                field.delete(0, END)

            # Bio is cleared differently.
            self.bio_entry.delete(0.0, END)

            # Reset role widgets to standard.
            self.role_entry.set("standard")

            # Clear password widgets.
            password_fields = [self.password_entry, self.verify_password_entry]
            for field in password_fields:
                field.delete(0, END)
        
        # Show view.
        self.overlay_frame.lift()

    def hide_view(self):
        """Hides the AccountEditorView overlay."""
        self.overlay_frame.lower()