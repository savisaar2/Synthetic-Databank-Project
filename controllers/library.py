class LibraryController:
    def __init__(self, model, view):
        """
        Initialises an instance of the LibraryController class.

        This class handles logic and interaction between the library view and dataframe model.

        Parameters
        ----------
        model : Model
            The applicaiton's model instance.
        name : View
            The application's view instance.
        """
        self.model = model
        self.view = view
        self.frame = self.view.frames["library"]
        self.import_overlay = self.view.frames["import"]

        self._display_dataset_list(mode="all")

        self._bind()

    def _display_dataset_list(self, mode, subset=None):
        data = self.model.library.get_datasets(mode, subset)
        self.frame.populate_treeview(file_list=data)

    def _search_databank(self):
        pass

    def _create_new_dataset(self):
        pass

    def _show_metadata(self):
        pass

    def _load_dataset(self):
        pass

    def _bind(self):
        """
        Private method to establish event bindings.
        Implement this method to set up event handlers and connections
        for user interactions with widgets on the view related to the library page.
        """
        self.frame.search_input.bind("<Key>", lambda event: self._search_databank())
        self.frame.import_button.bind("<Button-1>", lambda _: self.import_overlay.show_view())
        self.frame.new_button.bind("<Button-1>", lambda event: self._create_new_dataset())
        self.frame.tree_view.bind("<<TreeviewSelect>>", lambda event: self._show_metadata())
        self.frame.tree_view.bind("<Double-1>", lambda event: self._load_dataset())