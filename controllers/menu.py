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
        self._highlight_active_button(self.frame.library_button)
        self._bind()

    def _switch_view(self, event, view_name):
        """Switch views.

        Args:
            view_name (str): View to switch to
        """
        button = event.widget
        parent_frame = button.master

        # If button is not disabled change button focus color and switch view.
        if parent_frame.cget("state") == "normal":
            self._highlight_active_button(parent_frame)
            self.logger.log_info(f"User changed view to '{view_name}'.")
            self.view.switch_view(view_name)

    def _highlight_active_button(self, button):
        """
        Defaults button colors and sets focus to active button.
        """
        self.frame.library_button.configure(fg_color="#336aa0")
        self.frame.analyse_button.configure(fg_color="#336aa0")
        self.frame.manipulate_button.configure(fg_color="#336aa0")
        self.frame.sample_button.configure(fg_color="#336aa0")
        self.frame.save_button.configure(fg_color="#336aa0")
        self.frame.accounts_button.configure(fg_color="#336aa0")
        button.configure(fg_color="#0a3556")

    def _confirm_quit(self):
        result = self.view.frames["exception"].display_confirm("Are you sure you want to quit?")
        if result:
            self.view.root.quit()

    def _bind(self):
        """
        Private method to establish event bindings.
        Implement this method to set up event handlers and connections
        for user interactions with widgets on the view related to the menu.
        """
        # Add event click event bindings to menu items.
        self.frame.library_button.bind("<Button-1>", lambda event, args="library": self._switch_view(event, args))
        self.frame.analyse_button.bind("<Button-1>", lambda event, args="analyse": self._switch_view(event, args))
        self.frame.manipulate_button.bind("<Button-1>", lambda event, args="manipulate": self._switch_view(event, args))
        self.frame.sample_button.bind("<Button-1>", lambda event, args="sample": self._switch_view(event, args))
        self.frame.save_button.bind("<Button-1>", lambda event, args="save": self._switch_view(event, args))
        self.frame.accounts_button.bind("<Button-1>", lambda event, args="accounts": self._switch_view(event, args))
        self.frame.end_button.bind("<Button-1>", lambda _: self._confirm_quit())