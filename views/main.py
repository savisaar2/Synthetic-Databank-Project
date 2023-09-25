from .root import Root
from .pages.library import LibraryView
from .pages.accounts import AccountsView
from .pages.analyse import AnalyseView
from .pages.manipulate import ManipulateView
from .pages.menu import MenuView
from .pages.sample import SampleView
from .pages.save import SaveView
from .overlays.login import LoginView
from .overlays.importfile import ImportView
from .overlays.change_password import ChangePwView
from .overlays.account_manager import AccountMgmtView
from .overlays.account_editor import AccountEditorView

class View:
    def __init__(self):
        """
        Initialise the View component of the application.

        This class represents the View component of the application's MVC (Model-View-Controller) architecture.
        It initialises the root window, creates instances of various view classes for different application pages
        and overlays, and manages the currently displayed view.
        """
        self.root = Root()
        self.frames = {}

        # Hide root during page rendering.
        self.root.withdraw()

        # Add our pages into self.frames.
        self._add_frame(AccountsView, "accounts")
        self._add_frame(AnalyseView, "analyse")
        self._add_frame(ManipulateView, "manipulate")
        self._add_frame(MenuView, "menu")
        self._add_frame(SampleView, "sample")
        self._add_frame(SaveView, "save")
        self._add_frame(LibraryView, "library") # Last rendered sits on top of stack.

        # Add our overlays into self.frames.
        self._add_frame(LoginView, "login")
        self._add_frame(ImportView, "import")
        self._add_frame(ChangePwView, "change_password")
        self._add_frame(AccountMgmtView, "accounts_manager")
        self._add_frame(AccountEditorView, "accounts_editor")

        self.current_view = None

        # Display application after rendering completed.
        self.root.deiconify()

    def _add_frame(self, view_class, name):
        """
        Create an instance of a view class and add it to the frames dictionary.

        Parameters
        ----------
        view_class : str
            The imported classname.
        name : str
            The name to identify the instance.
        """
        self.frames[name] = view_class(self.root)

    def switch_view(self, name):
        """
        Switch the current view to the specified view.

        Parameters
        ----------
        name : str
            The name of the instance in self.frames.
        """
        self.current_view = self.frames[name]
        self.current_view.lift()

    def start_mainloop(self):
        """Start the main application event loop."""
        self.root.mainloop()