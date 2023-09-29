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
        self.model = model
        self.view = view
        self.frame = self.view.frames["analyse"]
        self.exception = self.view.frames["exception"] # Import for use!

        self._bind()
    
    def _refresh_analyse_widgets(self, event): 
        """
        Obtain column headers from the loaded dataset to be populated in the appropriate widgets e.g. 
        option menues and row count of Analyse view. Called whenever Analyse side panel is clicked to 
        ensure correct data.
        """
        column_headers = self.model.DATASET.get_column_headers()
        column_headers.insert(0, "------")
        row_count = self.model.DATASET.get_df_row_count()
        self.frame.refresh_analyse_widgets(dataset_attributes=(row_count, column_headers))

    def _plot_visualisation(self, event): 
        """
        Plot selected visualisation based on selected Graph Style and variable(s). 
        """
        dataset_name = self.model.DATASET.get_dataset_name()
        graph_option = self.frame.graph_option_menu.get()
        var_a_column = self.model.DATASET.get_column_data(column=self.frame.variable_a_option_menu.get())
        
        if graph_option == "Scatter": 
            var_b_column = self.model.DATASET.get_column_data(column=self.frame.variable_b_option_menu.get())
        else:
            var_b_column = None

        self.model.analyse.plot_visualisation(
            mode=graph_option, title=dataset_name, var_a=var_a_column, var_b=var_b_column
            )

    def _summarise(self, event): 
        """
        Generate descriptive statistics based on chosen variable (column of data) in the view.
        """
        try: 
            rounding_val = self.model.analyse.convert_to_number(
                mode="round", val=self.frame.summary_round_value_input.get()
                )
        except ValueError as e: 
            self.exception.display_error(e)
            return

        if type(rounding_val) == int: 
            summary = self.model.analyse.summarise(
                var=self.model.DATASET.get_column_data(column=self.frame.summary_option_menu.get()), 
                rounding=rounding_val,
                null_val=self.frame.null_value_input.get()
                )
            self.frame.populate_summary_tables(d=summary)

    def _pivot(self, event): 
        """
        Create pivot table based on selected variable (column) of data, i.e. categorical column, related values
        and the selected aggregate function. 
        """
        try: 
            rounding_val = self.model.analyse.convert_to_number(
                mode="round", val=self.frame.pivot_round_value_input.get()
                )
        except ValueError as e: 
            self.exception.display_error(e)
            return

        if type(rounding_val) == int: 
            pivot_data = self.model.analyse.pivot(
                df=self.model.DATASET.get_reference_to_current_snapshot(),
                vals=self.frame.values_option_menu.get(),
                cat=self.frame.categories_option_menu.get(), 
                agg=self.frame.aggfunc_option_menu.get(),
                rounding=rounding_val
            )
            self.frame.populate_pivot_table(d=pivot_data)
        

    def _tabulate(self, event):
        """Facilitate tabulation of dataset using start_row, end_row values in the view
        and obtaining the specified rows from the loaded dataset before refreshing the 
        widgets in the view. 
        """
        try: 
            start_row = self.model.analyse.convert_to_number(
                mode="start_row", val=self.frame.start_row_input.get()
                )
            end_row = self.model.analyse.convert_to_number(
                mode="end_row", val=self.frame.end_row_input.get()
                )
        except ValueError as e: 
            self.exception.display_error(e)
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
        self.view.frames["menu"].analyse_button.bind("<Button-1>", self._refresh_analyse_widgets)
        self.frame.plot_button.bind("<Button-1>", self._plot_visualisation)
        self.frame.summarise_button.bind("<Button-1>", self._summarise)
        self.frame.pivot_button.bind("<Button-1>", self._pivot)
        self.frame.tabulate_button.bind("<Button-1>", self._tabulate)