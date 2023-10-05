from utils.logger_utils import Logger

class MenuController:
    def __init__(self, model, view):
        """
        Initialises an instance of the MenuController class.

        This class handles logic and interaction between the Menu view.

        Parameters
        ----------
        model : Model
            The applicaiton's model instance.
        name : View
            The application's view instance.
        """
        self.logger = Logger()
        self.model = model
        self.view = view
        self.frame = self.view.frames["menu"]
        self._bind()

    def _switch_view(self, view_name):
        """Switch views.

        Args:
            view_name (str): View to switch to
        """
        self.logger.log_info(f"User changed view to '{view_name}'.")
        self.view.switch_view(view_name)    

    def _bind(self):
        """
        Private method to establish event bindings.
        Implement this method to set up event handlers and connections
        for user interactions with widgets on the view related to the menu.
        """
        # Add event click event bindings to menu items.
        self.frame.library_button.bind("<Button-1>", lambda _: self._switch_view("library"))
        self.frame.analyse_button.bind("<Button-1>", lambda _: self._switch_view("analyse"))
        self.frame.manipulate_button.bind("<Button-1>", lambda _: self._switch_view("manipulate"))
        self.frame.sample_button.bind("<Button-1>", lambda _: self._switch_view("sample"))
        self.frame.save_button.bind("<Button-1>", lambda _: self._switch_view("save"))
        self.frame.accounts_button.bind("<Button-1>", lambda _: self._switch_view("accounts"))
        self.frame.end_button.bind("<Button-1>", lambda _: self.view.root.quit())