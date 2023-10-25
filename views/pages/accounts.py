from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkCanvas, CTkButton, END
from .base import BaseView

class AccountsView(BaseView):
    def __init__(self, root, *args, **kwargs):
        """
        Initialise the Accounts view of the application.

        This class represents the AccountsView page of the application.
        It renders the interactive widgets on the frontend of the application.

        Parameters
        ----------
        root : Root
            The applicaiton's root instance.
        """
        # Pass some base title and description to our BaseView class.
        super().__init__(root, "Account Management", "Manage User Accounts.", *args, **kwargs)
        self._render_page()

    def _render_page(self):
        """Renders widgets on the AccountsView page."""
        self.parent_frame = CTkFrame(self)
        self.parent_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Define rows to hold the entry widgets.
        row1_frame = CTkFrame(self.parent_frame, corner_radius=0, fg_color="transparent")
        row2_frame = CTkFrame(self.parent_frame, corner_radius=0, fg_color="transparent")
        row3_frame = CTkFrame(self.parent_frame, corner_radius=0, fg_color="transparent")
        row4_frame = CTkFrame(self.parent_frame, corner_radius=0, fg_color="transparent")

        # Create entry with labels.
        self.first_name_entry = self.create_entry_with_label(row1_frame, "First Name:", "w")
        self.last_name_entry = self.create_entry_with_label(row1_frame, "Last Name:", "w")
        self.username_entry = self.create_entry_with_label(row1_frame, "Username:", "w")
        self.initial_entry = self.create_entry_with_label(row2_frame, "Initals:", "w")
        self.department_entry = self.create_entry_with_label(row2_frame, "Department:", "w")
        self.office_entry = self.create_entry_with_label(row2_frame, "Office:", "w")
        self.email_entry = self.create_entry_with_label(row3_frame, "Email:", "w", entry_width=280)

        # Bio Textbox and Label
        bio_label = CTkLabel(row4_frame, text="Bio:", width=80, anchor="nw").pack(side="left", padx=5, pady=5)
        self.bio_entry = CTkEntry(row4_frame, width=620, height=150)

        self.bio_entry.pack(side="left", padx=5, pady=5)

        # Pack the row frames.
        row1_frame.pack(fill="both", expand=True, padx=10)
        row2_frame.pack(fill="both", expand=True, padx=10)
        row3_frame.pack(fill="both", expand=True, padx=10)
        row4_frame.pack(fill="both", expand=True, padx=10)

        # Define the buttons frame.
        self.button_frame = CTkFrame(self.parent_frame, fg_color="transparent")
        self.button_frame.pack(fill="x", expand=True, padx=20)

    def create_entry_with_label(self, frame, text, anchor, entry_width=140):
        """
        Creates an entry widget with a label.
        """
        label = CTkLabel(frame, width=80, text=text, anchor=anchor).pack(side="left", padx=5, pady=5)
        entry = CTkEntry(frame, width=entry_width)
        entry.pack(side="left", padx=5, pady=5)
        return entry

    def load_profile_info(self, user):
        """
        Populate user data into entry widgets.

        Parameters
        ----------
        user : dict
            Dictionary of key value representing user data.
        """
        self.enable_entries()
        
        # Clear all our entries before writing.
        self.first_name_entry.delete(0, END)
        self.last_name_entry.delete(0, END)
        self.username_entry.delete(0, END)
        self.initial_entry.delete(0, END)
        self.department_entry.delete(0, END)
        self.office_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.bio_entry.delete(0, END)

        # Write new values to our entry widgets.
        self.first_name_entry.insert(0, user["firstname"])
        self.last_name_entry.insert(0, user["lastname"])
        self.username_entry.insert(0, user["username"])
        self.initial_entry.insert(0, user["initials"])
        self.department_entry.insert(0, user["department"])
        self.office_entry.insert(0, user["office"])
        self.email_entry.insert(0, user["email"])
        self.bio_entry.insert(0, user["bio"])

        self.disable_entries()

    def enable_entries(self):
        """
        Enable all entry widgets.
        """
        self.first_name_entry.configure(state="normal", border_width=1)
        self.last_name_entry.configure(state="normal", border_width=1)
        #self.username_entry.configure(state="normal", border_width=1)
        self.initial_entry.configure(state="normal", border_width=1)
        self.department_entry.configure(state="normal", border_width=1)
        self.office_entry.configure(state="normal", border_width=1)
        self.email_entry.configure(state="normal", border_width=1)
        self.bio_entry.configure(state="normal", border_width=1)

    def disable_entries(self):
        """
        Disabled all entry widgets.
        """
        self.first_name_entry.configure(state="disabled", border_width=0)
        self.last_name_entry.configure(state="disabled", border_width=0)
        self.username_entry.configure(state="disabled", border_width=0)
        self.initial_entry.configure(state="disabled", border_width=0)
        self.department_entry.configure(state="disabled", border_width=0)
        self.office_entry.configure(state="disabled", border_width=0)
        self.email_entry.configure(state="disabled", border_width=0)
        self.bio_entry.configure(state="disabled", border_width=0)

    def load_buttons_by_role(self, role):
        """
        Render buttons based on role.

        Parameters
        ----------
        role : str
            The authenticated users role (admin|user).
        """
        # Destroy all widgets in button frame.
        for widget in self.button_frame.winfo_children():
            widget.destroy()
            
        # Render standard user buttons edit and edit pw.
        self.edit_button = CTkButton(self.button_frame, height=40, border_spacing=10, text="Edit Details", anchor="n")
        self.edit_button.pack(side="left", padx=50)

        self.edit_pw_button = CTkButton(self.button_frame, height=40, border_spacing=10, text="Reset Password", anchor="n")
        self.edit_pw_button.pack(side="left", padx=50)

        # Render admin specific management button if authenticated as admin.
        if role == "admin":
            self.manage_button = CTkButton(self.button_frame, height=40, border_spacing=10, text="Manage Users", anchor="n")
            self.manage_button.pack(side="left", padx=50)

    def toggle_edit(self):
        """
        Toggled profile edit mode between edit and save.

        When saved will return profile data.
        """
        current_text = self.edit_button.cget("text")
        if current_text == "Edit Details":
            # Enabled all entry widgets and change button text to Save Details.
            self.enable_entries()
            self.edit_button.configure(text="Save Details")
        else:
            # Disable all entry widgets and change button back to Edit Details.
            self.disable_entries()
            self.edit_button.configure(text="Edit Details")

            # Return profile info from saving.
            return {
                "profile_info": {
                    "first": self.first_name_entry.get(), 
                    "last": self.last_name_entry.get(),
                    "initials": self.initial_entry.get(), 
                    "department": self.department_entry.get(), 
                    "office": self.office_entry.get(), 
                    "email": self.email_entry.get(), 
                    "bio": self.bio_entry.get()
                }
            }