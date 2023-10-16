from .menu import MenuController
from .library import LibraryController
from .analyse import AnalyseController
from .manipulate import ManipulateController
from .sample import SampleController
from .save import SaveController
from .login import LoginController
from .exception import ExceptionController
from .accounts import AccountsController
from .config_new_dataset import ConfigNewDatasetController
from utils.logger_utils import Logger

class Controller:
    def __init__(self, model, view):
        """
        Initialize the Controller component of the application.

        This class represents the Controller component of the application's MVC (Model-View-Controller) architecture.
        It initialises the controllers to be used in this application, and passes the models and views to them.

        Parameters
        ----------
        model : Model
            The applicaiton's model instance.
        name : View
            The application's view instance.
        """
        self.view = view
        self.model = model

        logger = Logger()

        self.library_controller = LibraryController(model, view)
        self.analyse_controller = AnalyseController(model, view)
        self.manipulate_controller = ManipulateController(model, view)
        self.sample_controller = SampleController(model, view)
        self.save_controller = SaveController(model, view)
        self.login_controller = LoginController(model, view, logger)
        self.exception = ExceptionController(model, view)
        self.menu_controller = MenuController(model, view)
        self.accounts_controller = AccountsController(model, view)
        self.config_new_dataset_controller = ConfigNewDatasetController(model, view)

    def start(self):
        """Start the main application."""
        self.view.start_mainloop()