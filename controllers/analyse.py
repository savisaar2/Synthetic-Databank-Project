from utils.logger_utils import Logger
import threading

class AnalyseController:
    def __init__(self, model, view):
        """
        Initialises an instance of the AnalyseController class.

        This class handles logic and interaction between the Analyse view and dataframe model.

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
        self.frame = self.view.frames["analyse"]
        self.exception = self.view.frames["exception"] # Import for use!

        self._bind()
    
    def _calculate_and_refresh_stats(self, event): 
        """
        Obtain column headers from the loaded dataset to be populated in the appropriate widgets e.g. 
        option menues and row count of Analyse view. Called whenever Analyse side panel is clicked to 
        ensure correct data. 
        Also calculate all the descriptive stats and show in first panel of three. 
        """
        button = event.widget
        parent_frame = button.master

        if parent_frame.cget("state") == "disabled":
            return

        df = self.model.DATASET.get_reference_to_current_snapshot()
        column_headers = self.model.DATASET.get_column_headers()
        column_headers.insert(0, "------")
        row_count = self.model.DATASET.get_df_row_count()

        # Get descriptive stats
        desc_mode, descriptive_stats = self.model.analyse.descriptive_statistics(df=df,row_count=row_count)

        # Get summary stats for entire dataset
        summary_mode, summary_stats = self.model.analyse.summary_statistics(df=df)

        # Corr analysis
        corr_mode, correlation_stats = self.model.analyse.correlation_analysis(df=df)

        # Refresh option menu with column headers & row count
        self.frame.refresh_open_menus(dataset_attributes=(row_count, column_headers))

        # Refresh table 1 of 3 (Panel: Entire Dataset) i.e. Descriptive Stats - Entire Dataset
        self.frame.populate_stats_table(stat="descriptive", mode=".", df=descriptive_stats)

        # Refresh table 2 of 3 (Panel: Entire Dataset) i.e. Summary Statistics - Entire Dataset
        self.frame.populate_stats_table(stat="summary", mode=summary_mode, df=summary_stats)

        # Refresh table 3 of 3 (Panel: Entire Dataset) i.e. Correlation Analysis - Entire Dataset
        self.frame.populate_stats_table(stat="correlation", mode=corr_mode, df=correlation_stats)

    def _plot_visualisation(self, event): 
        """
        Plot selected visualisation based on selected Graph Style and variable(s). 
        """
        # Defaults
        dataset_name = self.model.DATASET.get_dataset_name()
        var_a_column = None
        var_b_column = None
        df_ref = None 
        graph_option = self.frame.graph_option_menu.get()

        if graph_option == "Heat Map":
            df_ref = self.model.DATASET.get_reference_to_current_snapshot() # reference to the current dataframe
        else: 
            var_a_column = self.model.DATASET.get_column_data(column=self.frame.variable_a_option_menu.get())

        if graph_option == "Scatter": 
            var_b_column = self.model.DATASET.get_column_data(column=self.frame.variable_b_option_menu.get())

        browser_task = threading.Thread(target=self.model.analyse.plot_visualisation, kwargs={
            "mode":graph_option, "title":dataset_name, "var_a":var_a_column, "var_b":var_b_column, "df_ref":df_ref
            })
        browser_task.start()

    def _summarise_column(self, event): 
        """
        Generate descriptive statistics based on chosen variable (column of data) in the view.
        """
        selection = self.frame.col_summary_option_menu.get()
        if selection != "------": 
            summary = self.model.analyse.summarise_column(
                var=self.model.DATASET.get_column_data(column=selection)
                )
            self.frame.populate_summary_tables(d=summary)

    def _pivot(self, event): 
        """
        Create pivot table based on selected variable (column) of data, i.e. categorical column, related values
        and the selected aggregate function. 
        """
        pivot_data = self.model.analyse.pivot(
            df=self.model.DATASET.get_reference_to_current_snapshot(),
            vals=self.frame.values_option_menu.get(),
            cat=self.frame.categories_option_menu.get(), 
            agg=self.frame.aggfunc_option_menu.get(),
        )
        self.frame.populate_pivot_table(d=pivot_data)

    def _tabulate(self, event):
        """Facilitate tabulation of dataset using start_row, end_row values in the view
        and obtaining the specified rows from the loaded dataset before refreshing the 
        widgets in the view. 
        """
        try: 
            start_row = self.model.analyse.convert_to_number(val=self.frame.start_row_input.get())
            end_row = self.model.analyse.convert_to_number(val=self.frame.end_row_input.get())
        except ValueError as e: 
            self.exception.display_error("Specify start/end row values as an integer values.")
            return

        headers = self.model.DATASET.get_column_headers()
        rows = self.model.DATASET.get_df_row_by_range(start_row=start_row, end_row=end_row)
        self.frame.create_and_populate_raw_table(
            container_frame=self.frame.tt_frame,
            column_headers=headers, 
            rows=rows
        )

    def _bind(self):
        """
        Private method to establish event bindings.
        Implement this method to set up event handlers and connections
        for user interactions with widgets on the view related to the analyse page.
        """
        self.view.frames["menu"].analyse_button.bind("<Button-1>", self._calculate_and_refresh_stats)
        self.frame.plot_button.bind("<Button-1>", self._plot_visualisation)
        self.frame.col_summary_option_menu.bind("<Configure>", self._summarise_column)
        self.frame.pivot_button.bind("<Button-1>", self._pivot)
        self.frame.tabulate_button.bind("<Button-1>", self._tabulate)