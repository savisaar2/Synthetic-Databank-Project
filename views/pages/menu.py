from customtkinter import CTkFrame

class MenuView(CTkFrame):
    def __init__(self, root, *args, **kwargs):
        """
        Initialise the Menu view of the application.

        This class represents the MenuView section of the application.
        It renders the interactive widgets on the frontend of the application.

        Parameters
        ----------
        root : Root
            The applicaiton's root instance.
        """
        # Pass some base parameters to our BaseView class.
        super().__init__(root.menu_frame, *args, **kwargs)
        self._render_menu()

    def _render_menu(self):
        """Renders widgets on the Menu section."""
        pass