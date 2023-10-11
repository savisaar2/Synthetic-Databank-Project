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

        row1_frame = CTkFrame(self.parent_frame, corner_radius=0, fg_color="transparent")
        row2_frame = CTkFrame(self.parent_frame, corner_radius=0, fg_color="transparent")
        row3_frame = CTkFrame(self.parent_frame, corner_radius=0, fg_color="transparent")
        row4_frame = CTkFrame(self.parent_frame, corner_radius=0, fg_color="transparent")

        first_name_label = CTkLabel(row1_frame, width=80, text="First Name:", anchor="w").pack(side="left", padx=5, pady=5)
        self.first_name_entry = CTkEntry(row1_frame)

        self.first_name_entry.pack(side="left", padx=5, pady=5)

        last_name_label = CTkLabel(row1_frame, width=80, text="Last Name:", anchor="w").pack(side="left", padx=5, pady=5)
        self.last_name_entry = CTkEntry(row1_frame)

        self.last_name_entry.pack(side="left", padx=5, pady=5)
        
        username_label = CTkLabel(row1_frame, width=80, text="Username:", anchor="w").pack(side="left", padx=5, pady=5)
        self.username_entry = CTkEntry(row1_frame)
        
        self.username_entry.pack(side="left", padx=5, pady=5)

        initial_label = CTkLabel(row2_frame, width=80, text="Initials:", anchor="w").pack(side="left", padx=5, pady=5)
        self.initial_entry = CTkEntry(row2_frame)

        self.initial_entry.pack(side="left", padx=5, pady=5)

        department_label = CTkLabel(row2_frame, width=80, text="Department:", anchor="w").pack(side="left", padx=5, pady=5)
        self.department_entry = CTkEntry(row2_frame)

        self.department_entry.pack(side="left", padx=5, pady=5)

        office_label = CTkLabel(row2_frame, width=80, text="Office:", anchor="w").pack(side="left", padx=5, pady=5)
        self.office_entry = CTkEntry(row2_frame)

        self.office_entry.pack(side="left", padx=5, pady=5)

        email_label = CTkLabel(row3_frame, width=80, text="Email:", anchor="w").pack(side="left", padx=5, pady=5)
        self.email_entry = CTkEntry(row3_frame, width=250)

        self.email_entry.pack(side="left", padx=5, pady=5)

        bio_label = CTkLabel(row4_frame, text="Bio:", width=80, anchor="nw").pack(side="left", padx=5, pady=5)
        self.bio_entry = CTkEntry(row4_frame, width=620, height=150)

        self.bio_entry.pack(side="left", padx=5, pady=5)

        row1_frame.pack(fill="both", expand=True, padx=10)
        row2_frame.pack(fill="both", expand=True, padx=10)
        row3_frame.pack(fill="both", expand=True, padx=10)
        row4_frame.pack(fill="both", expand=True, padx=10)

        self.button_frame = CTkFrame(self.parent_frame, fg_color="transparent")
        self.button_frame.pack(fill="x", expand=True, padx=20)

    def load_profile_info(self, user):
        self.first_name_entry.delete(0, END)
        self.last_name_entry.delete(0, END)
        self.username_entry.delete(0, END)
        self.initial_entry.delete(0, END)
        self.department_entry.delete(0, END)
        self.office_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.bio_entry.delete(0, END)

        self.first_name_entry.insert(0, user["profile_info"]["first"])
        self.last_name_entry.insert(0, user["profile_info"]["last"])
        self.username_entry.insert(0, user["username"])
        self.initial_entry.insert(0, user["profile_info"]["initials"])
        self.department_entry.insert(0, user["profile_info"]["department"])
        self.office_entry.insert(0, user["profile_info"]["office"])
        self.email_entry.insert(0, user["profile_info"]["email"])
        self.bio_entry.insert(0, user["profile_info"]["bio"])

        self.disable_entries()

    def enable_entries(self):
        self.first_name_entry.configure(state="normal", border_width=1)
        self.last_name_entry.configure(state="normal", border_width=1)
        #self.username_entry.configure(state="normal", border_width=1)
        self.initial_entry.configure(state="normal", border_width=1)
        self.department_entry.configure(state="normal", border_width=1)
        self.office_entry.configure(state="normal", border_width=1)
        self.email_entry.configure(state="normal", border_width=1)
        self.bio_entry.configure(state="normal", border_width=1)

    def disable_entries(self):
        self.first_name_entry.configure(state="disabled", border_width=0)
        self.last_name_entry.configure(state="disabled", border_width=0)
        self.username_entry.configure(state="disabled", border_width=0)
        self.initial_entry.configure(state="disabled", border_width=0)
        self.department_entry.configure(state="disabled", border_width=0)
        self.office_entry.configure(state="disabled", border_width=0)
        self.email_entry.configure(state="disabled", border_width=0)
        self.bio_entry.configure(state="disabled", border_width=0)

    def load_buttons_by_role(self, role):
        for widget in self.button_frame.winfo_children():
            widget.destroy()
            
        if role == "admin":
            self.edit_button = CTkButton(self.button_frame, height=40, border_spacing=10, text="Edit Details", anchor="n")
            self.edit_button.pack(side="left", padx=50)

            self.edit_pw_button = CTkButton(self.button_frame, height=40, border_spacing=10, text="Reset Password", anchor="n")
            self.edit_pw_button.pack(side="left", padx=50)

            self.manage_button = CTkButton(self.button_frame, height=40, border_spacing=10, text="Manage Users", anchor="n")
            self.manage_button.pack(side="left", padx=50)
        else:
            self.edit_button = CTkButton(self.button_frame, height=40, border_spacing=10, text="Edit Details", anchor="n")
            self.edit_button.pack(side="left", padx=50)

            self.edit_pw_button = CTkButton(self.button_frame, height=40, border_spacing=10, text="Reset Password", anchor="n")
            self.edit_pw_button.pack(side="left", padx=50)

    def toggle_edit(self):
        current_text = self.edit_button.cget("text")
        if current_text == "Edit Details":
            self.enable_entries()
            new_text = "Save Details"
            self.edit_button.configure(text=new_text)
        else:
            self.disable_entries()
            new_text = "Edit Details"
            self.edit_button.configure(text=new_text)
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