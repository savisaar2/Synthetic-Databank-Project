from utils.logger_utils import Logger
from datetime import datetime


class SampleController:
    def __init__(self, model, view):
        """
        Initialises an instance of the SampleController class.

        This class handles logic and interaction between the Sample view and dataframe model.

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
        self.frame = self.view.frames["sample"]
        self.exception = self.view.frames["exception"]
        
        self._bind()

    def _refresh_sample_widgets(self, event, mode): 
        """
        Obtain column headers from the loaded dataset to be populated in the appropriate widgets e.g. 
        option menues. Called whenever Sample side panel is clicked to ensure correct data.
        """
        button = event.widget
        parent_frame = button.master

        if parent_frame.cget("state") == "disabled":
            return
        
        column_headers = self.model.DATASET.get_column_headers()
        column_headers.insert(0, "------")
        self.frame.refresh_sample_widgets(mode=mode, column_headers=column_headers)

    def _generate(self, event): # Generate Sample
        """Generate sample as per chosen algorithm.

        Args:
            event (_type_): _description_
        """
        output = self._validate_user_input()
        algo_selection = self.frame.get_sample_algo_menu_selection()

        if output != False: # passed all validation! 
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-7]
            df = self.model.DATASET.get_reference_to_current_snapshot()
            ds_name = self.model.DATASET.get_dataset_name()

            match algo_selection: 
                case "Simple Random": 
                    self._simple_random(df=df, dataset_name=ds_name, sample_size=output["sample_size"])
                case "Stratified": 
                    ...
                case "Systematic": 
                    ...
                case "Under":
                    ...
                case "Over": 
                    ...
                case "Cluster": 
                    ...
                case "Quota": 
                    ...
                case "Judgment": 
                    ...
                case "Snowball": 
                    ...
            self.logger.log_info(f"Sample - generated using: {algo_selection} technique.")
            self._update_sample_status(
                text=f"Sample generated using: {algo_selection} technique at {now}.", colour="lime"
                )
            self.frame.reset_algo_menu()
            self.frame.reconfig_widgets(level="main", option="------") # reset

    def _update_sample_status(self, text, colour): 
        """Update the status of sample component to notify user of outcome.

        Args:
            text (str): custom user specified text.
            colour (str): colour of label text.
        """
        self.frame.update_sample_status(text=text, colour=colour)
    
    def _validate_user_input(self): 
        """First step prior to generation of samples.
        Returns False if exception occurs. Otherwise returns dictionary of user inputs.
        """
        algo_selection = self.frame.get_sample_algo_menu_selection()
        row_count = self.model.DATASET.get_df_row_count()

        match algo_selection: 
            case "Simple Random":
                try: 
                    _input = self.model.sample.convert_to_number(
                        val=self.frame.get_sample_size_entry(), 
                        custom_error_warning="Specify sample size input as an integer value above 0."
                        )
                    assert _input <= row_count, "Sample size input exceeds dataset row count."
                    assert _input >= -1, "Sample size input is below zero. Specify 0 or more as value."
                except AssertionError as e: 
                    self.exception.display_error(error=e)
                    return False
                else: 
                    return {"sample_size": _input}
            case "Stratified": 
                ...
            case "Systematic": 
                ...
            case "Under":
                ...
            case "Over": 
                ...
            case "Cluster": 
                ...
            case "Quota": 
                ...
            case "Judgment": 
                ...
            case "Snowball": 
                ...
    
    def _add_generated_dataset_to_snapshot(self, df, dataset_name, description, schedule_set): 
        """_summary_

        Args:
            df (_type_): _description_
        """
        ...
        # TODO: check out generate function of manipulate to add appropriate info to DATASET > snapshots in order for proper rollback integration from sample.
        # self.model.DATASET.add_generated_dataset_to_snapshot(
        #     schedule_set="Sample generation: Simple Random", dataset_name=dataset_name, df=new_sample
        #     )

    def _simple_random(self, df, dataset_name, sample_size): 
        """Simple random sampling.

        Args:
            dataset_name (_type_): _description_
            df (_type_): _description_
        """
        try: 
            new_sample = self.model.sample.simple_random(df=df,sample_size=sample_size)
            # self._add_generated_dataset_to_snapshot(self)
        except Exception as e: 
            self.logger.log_exception("Sample generation failed to complete. Traceback:")
            self.exception.display_error(error=e)

    def _stratified(self, df, dataset_name, num_of_splits, dependant_col): 
        """_summary_

        Args:
            df (_type_): _description_
            dataset_name (_type_): _description_
            num_of_splits (_type_): _description_
            dependant_col (_type_): _description_
        """
        ...

    def _systematic(self, df, dataset_name, interval): 
        """_summary_

        Args:
            df (_type_): _description_
            dataset_name (_type_): _description_
            interval (_type_): _description_
        """
        ...
    
    def _under_sampling(self, df, dataset_name, dependant_col): 
        """_summary_

        Args:
            df (_type_): _description_
            dataset_name (_type_): _description_
            dependant_col (_type_): _description_
        """
        ...

    def _over_sampling(self, df, dataset_name, dependant_col):
        """_summary_

        Args:
            df (_type_): _description_
            dataset_name (_type_): _description_
            dependant_col (_type_): _description_
        """
        ...

    def _cluster(self, df, dataset_name, cluster_col, cluster_entry): 
        """_summary_

        Args:
            df (_type_): _description_
            dataset_name (_type_): _description_
            cluster_col (_type_): _description_
            cluster_entry (_type_): _description_
        """
        ...

    def _quota(self, df, dataset_name, col, sample_size): 
        """_summary_

        Args:
            df (_type_): _description_
            dataset_name (_type_): _description_
            col (_type_): _description_
            sample_size (_type_): _description_
        """
        ...

    def _judgment(self, df, dataset_name, rows_of_args): 
        """_summary_

        Args:
            df (_type_): _description_
            dataset_name (_type_): _description_
            rows_of_args (list): List of nested list of widget values.
        """
        # TODO: use judgment_snowball_row_arg_builder
        ...

    def _judgment_snowball_row_arg_builder(self): 
        """_summary_
        """
        ...

    def _showball(self, df, dataset_name, rows_of_args): 
        """_summary_

        Args:
            df (_type_): _description_
            dataset_name (_type_): _description_
            rows_of_args (_type_): _description_
        """
        # TODO: use judgment_snowball_row_arg_builder
        ...


    def _get_algorithm_info(self, event):
        """Get text description of algorithm. 
        """
        selection = self.frame.get_sample_algo_menu_selection()
        description = self.model.sample.get_algorithm_info(selection=selection)
        self.frame.update_algorithm_description_info(text=description)

    def _bind(self):
        """
        Private method to establish event bindings.
        Implement this method to set up event handlers and connections
        for user interactions with widgets on the view related to the sample page.
        """
        self.view.frames["menu"].sample_button.bind(
            "<Button-1>", lambda event, mode="menus": self._refresh_sample_widgets(event, mode)
            )
        self.frame.add_row.bind("<Button-1>", lambda event, mode="rows": self._refresh_sample_widgets(event, mode))
        self.frame.generate.bind("<Button-1>", self._generate)
        self.frame.sampling_algo_menu.bind("<Configure>", self._get_algorithm_info)