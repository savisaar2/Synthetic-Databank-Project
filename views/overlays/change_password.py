from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton, END

class ChangePwView(CTkFrame):
    def __init__(self, root, admin=False, *args, **kwargs):
        """
        Initialise the ChangePw overlay of the application.

        This class represents the ChangePwView overlay of the application.
        It renders the interactive widgets on the frontend of the application.

        Parameters
        ----------
        root : Root
            The applicaiton's root instance.
        """
        super().__init__(root, *args, **kwargs)
        self.admin = admin # Trigger for administrative view.
        self._setup_page()

    def _setup_page(self):
        """Renders the widgets on the ChangePwView."""
        self.overlay_frame = CTkFrame(self.master)
        self.overlay_frame.place(
            relx=0.5, rely=0.5, anchor="center",
            relwidth=1, relheight=1
        )
        self.overlay_frame.lower()

        # Define a content frame for the widgets.
        self.content_frame = CTkFrame(self.overlay_frame, fg_color="transparent")
        self.content_frame.pack(expand=True, padx=20, pady=20)

        # Create dynamic title based on access role.
        self.title_label = self.create_label(self.content_frame, "New Password" if self.admin else "Change Password", ("Arial", 24), side="top", pady=20)

        # Inputs frame will hold our entry widgets.
        self.inputs_frame = CTkFrame(self.content_frame)
        self.inputs_frame.pack(pady=20)

        # Non admin users require to enter account password to change password.
        if not self.admin:
            self.old_pw_entry = self.create_placeholder_field(self.inputs_frame, "Current Password", 250, "center", ("Arial", 16))

        # Define new password and verification entries.
        self.new1_pw_entry = self.create_placeholder_field(self.inputs_frame, "New Password", 250, "center", ("Arial", 16))
        self.new2_pw_entry = self.create_placeholder_field(self.inputs_frame, "Verify Password", 250, "center", ("Arial", 16))

        # Define a button frame and add save and cancel button to it.
        button_frame = CTkFrame(self.content_frame)
        button_frame.pack(pady=10)
        self.save_button = self.create_button(button_frame, "Change Password", height=40)
        self.cancel_button = self.create_button(button_frame, "Cancel", height=40)

    def create_placeholder_field(self, parent_frame, placeholder, width=140, justify="left", font=None):
        """
        Create a entry widget with a placeholder.
        """
        entry = CTkEntry(parent_frame, placeholder_text=placeholder, width=width, border_width=1, justify=justify, font=font, height=40, show="*")
        entry.pack(pady=5)
        return entry

    def create_button(self, frame, text, width=150, height=40, side="left", color=None, padx=5, pady=5):
        """
        Create a button widget.
        """
        button = CTkButton(frame, corner_radius=5, text=text, height=height, width=width, fg_color=color)
        button.pack(side=side, padx=padx, pady=pady)
        return button
    
    def create_label(self, parent_frame, text, font=None, width=100, side="left", pady=10):
        """
        Create a label widget.
        """
        label = CTkLabel(parent_frame, text=text, font=font, width=width)
        label.pack(side=side, padx=5, pady=pady)
        return label

    def clear_inputs(self):
        """
        Clears all entry widgets.
        """
        if not self.admin:
            self.old_pw_entry.delete(0, END)
        self.new1_pw_entry.delete(0, END)
        self.new2_pw_entry.delete(0, END)

    def show_view(self):
        """Shows the ChangePwView overlay."""
        self.overlay_frame.focus_set()
        self.overlay_frame.lift()

    def hide_view(self):
        """Hides the ChangePwView overlay."""
        self.overlay_frame.lower()