from customtkinter import CTkFrame, CTkLabel

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

        self.logo_label = CTkLabel(self.overlay_frame, text="Manager")
        self.logo_label.pack(padx=100,pady=10)

    def show_view(self):
        """Shows the AccountMgmtView overlay."""
        self.overlay_frame.lift()

    def hide_view(self):
        """Hides the AccountMgmtView overlay."""
        self.overlay_frame.lower()