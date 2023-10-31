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
        """Obtain column headers from the loaded dataset to be populated in the appropriate widgets e.g.
        option menues. Called whenever Sample side panel is clicked to ensure correct data.
        Also pulls type information of columns of the loaded dataframe and aids in readjusting
        the available comparison operator and attempt to convert the condition entry to match 
        column type. 
        """
        button = event.widget
        parent_frame = button.master

        if parent_frame.cget("state") == "disabled":
            return
        
        column_headers = self.model.DATASET.get_column_headers()
        column_to_data_type_mapping = self.model.DATASET.get_all_column_datatypes()

        if mode == "menus": # Rest sample widgets and clear collection of row instances
            for widget in self.frame.algo_to_widget_set_mapping: 
                self.frame.bulk_toggle(mode="reset", list_of_widgets=self.frame.algo_to_widget_set_mapping[widget])
            self.frame.reset_algo_menu()
            self.frame.reconfig_widgets(level="main", option="------") # reset

        column_headers.insert(0, "------") 
        self.frame.refresh_sample_widgets(mode=mode, dtypes=column_to_data_type_mapping, column_headers=column_headers)

    def _generate(self, event): # Generate Sample
        """Generate sample as per chosen algorithm.

        Args:
            event (_type_): _description_
        """
        if self.frame.get_generate_button_state() == "disabled": 
            return
        
        algo_selection = self.frame.get_sample_algo_menu_selection()
        
        if algo_selection in ["Judgment", "Snowball"]: 
            self._type_check_dataset()

        output = self._validate_user_input()

        if output != False: # passed all validation! 
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-7]
            df = self.model.DATASET.get_reference_to_current_snapshot()
            ds_name = self.model.DATASET.get_dataset_name()

            match algo_selection: 
                case "Simple Random": 
                    self._simple_random(df=df, dataset_name=ds_name, sample_size=output["sample size"])
                case "Stratified": 
                    self._stratified(
                        df=df, dataset_name=ds_name, sample_size=output["sample size"], 
                        dependant_col=self.frame.get_stratified_dependant_col_menu()
                        )
                case "Systematic": 
                    self._systematic(df=df, dataset_name=ds_name, interval=output["sampling interval"])
                case "Under":
                    self._under_sampling(
                        df=df, dataset_name=ds_name, target_col=self.frame.get_under_target_col_menu()
                        )
                case "Over": 
                    self._over_sampling(
                        df=df, dataset_name=ds_name, target_col=self.frame.get_over_target_col_menu()
                    )
                case "Cluster": 
                    self._cluster(
                        df=df, dataset_name=ds_name, sample_size=output["sample size"], 
                        cluster_col=self.frame.get_cluster_column_menu()
                    )
                case "Quota": 
                    ... # TODO final algo
                case "Judgment": 
                    self._judgment(
                        df=df, dataset_name=ds_name, rows_of_operations=self.frame.get_reference_to_rows_of_operations()
                    )
                case "Snowball": 
                    self._showball(
                        df=df, dataset_name=ds_name, rows_of_operations=self.frame.get_reference_to_rows_of_operations()
                    )
            
            self.logger.log_info(f"Sample - generated using: {algo_selection} technique.")
            self._update_sample_status(
                text=f"Sample generated using: {algo_selection} technique at {now}.", colour="lime"
                )
            self.frame.bulk_toggle(mode="reset", list_of_widgets=self.frame.algo_to_widget_set_mapping[algo_selection])
            self.frame.reset_algo_menu()
            self.frame.reconfig_widgets(level="main", option="------") # reset

    def _update_sample_status(self, text, colour): 
        """Update the status of sample component to notify user of outcome.

        Args:
            text (str): custom user specified text.
            colour (str): colour of label text.
        """
        self.frame.update_sample_status(text=text, colour=colour)
    
    def _assert_property(self, getter, row_count, label): 
        """Generalised for use with various view methods.

        Args:
            getter (function): method from view passed through
            row_count (int): row count of dataset
            label (str): label e.g. sample size

        Returns: Boolean value for process continuation or halt.
        """
        try: 
            _input = self.model.sample.convert_to_number(
                val=getter(), 
                custom_error_warning=f"Specify {label} input as integer value above 0."
            )
            assert _input <= row_count, f"{label.capitalize()} input exceeds dataset row count."
            assert _input >= -1, f"{label.capitalize()} input is below zero. Specify 0 or more as value."
        except AssertionError as e: 
            self.exception.display_error(error=e)
            return False
        else: 
            return {f"{label}": _input}
        
    def _type_check_dataset(self): 
        """Get all types of the columns of the dataset for the purposes of limiting user actions 
        for the instances of judgment_snowball_row.
        """
        ...
        
    def _validate_user_input(self): 
        """First step prior to generation of samples.
        Returns False if exception occurs. Otherwise returns dictionary of user inputs.
        """
        algo_selection = self.frame.get_sample_algo_menu_selection()
        row_count = self.model.DATASET.get_df_row_count()

        match algo_selection: 
            case "Simple Random":
                return self._assert_property(
                    self.frame.get_sample_size_entry, row_count=row_count, label="sample size"
                    )
            case "Stratified": 
                return self._assert_property(
                    self.frame.get_strat_sample_size_entry, row_count=row_count, label="sample size"
                    )
            case "Systematic": 
                return self._assert_property(
                    self.frame.get_systematic_interval_entry, row_count=row_count, label="sampling interval"
                    )
            case "Under" | "Over":
                return True # no validation required
            case "Cluster": 
                return self._assert_property(
                    self.frame.get_cluster_sample_size_entry, row_count=row_count, label="sample size"
                )
            case "Quota": 
                ...
            case "Judgment" | "Snowball": 
                all_true_lock = []
                for index, row in enumerate(self.frame.get_reference_to_rows_of_operations()): 
                    try: 
                        condition_value = row.convert_condition_entry_to_float()
                    except ValueError as e: 
                        self.exception.display_error(error=f"Row {index + 1}'s condition is not a float value.")
                        return False
                    else: 
                        all_true_lock.append(True)
                
                if all(all_true_lock): # True
                    return {f"{algo_selection}": condition_value}        
    
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
            dataset_name (str): name of dataset
            df (pandas dataframe): currently loaded dataset
        """
        try: 
            new_sample = self.model.sample.simple_random(df=df, sample_size=sample_size)
            # self._add_generated_dataset_to_snapshot(self) # TODO: add to snapshots
        except Exception as e: 
            self.logger.log_exception("Sample generation failed to complete. Traceback:")
            self.exception.display_error(error=e)

    def _stratified(self, df, dataset_name, sample_size, dependant_col): 
        """Stratified sampling algo

        Args:
            df (pandas dataframe): current loaded dataset
            dataset_name (str): name of dataset
            sample_size (int): integer value
            dependant_col (str): dataset column name
        """
        try: 
            new_sample = self.model.sample.stratified(df=df, sample_size=sample_size, dependant_col=dependant_col)
            # TODO: add to snapshots
        except Exception as e: 
            self.logger.log_exception("Sample generation failed to complete. Traceback:")
            self.exception.display_error(error=e)

    def _systematic(self, df, dataset_name, interval): 
        """Systematic sampling algo

        Args:
            df (pandas dataframe): currently loaded dataset
            dataset_name (str): name of dataset
            interval (integer): interval
        """
        try: 
            new_sample = self.model.sample.systematic(df=df, interval=interval)
            # TODO: add to snapshots
        except Exception as e: 
            self.logger.log_exception("Sample generation failed to complete. Traceback:")
            self.exception.display_error(error=e)
    
    def _under_sampling(self, df, dataset_name, target_col): 
        """Under sampling algo

        Args:
            df (pandas dataframe): currently loaded dataset
            dataset_name (str): name of dataset
            target_col (str): selected column from drop down
        """
        try: 
            new_sample = self.model.sample.under_or_over_sampling(df=df, target_col=target_col, mode="under")
            # TODO: add to snapshots
        except Exception as e: 
            self.logger.log_exception("Sample generation failed to complete. Traceback:")
            self.exception.display_error(error=e)

    def _over_sampling(self, df, dataset_name, target_col):
        """Over sampling algo

        Args:
            df (pandas dataframe): currently loaded dataset
            dataset_name (str): name of dataset
            target_col (str): selected column from drop down
        """
        try: 
            new_sample = self.model.sample.under_or_over_sampling(df=df, target_col=target_col, mode="over")
            # TODO: add to snapshots
        except Exception as e: 
            self.logger.log_exception("Sample generation failed to complete. Traceback:")
            self.exception.display_error(error=e)

    def _cluster(self, df, dataset_name, sample_size, cluster_col): 
        """Cluster sampling algo

        Args:
            df (pandas dataframe): currently loaded dataset
            dataset_name (str): name of dataset
            sample_size (int): number of clusters!
            cluster_col (str): selected cluster column
        """
        try: 
            new_sample = self.model.sample.cluster(df=df, sample_size=sample_size, cluster_col=cluster_col)
            # TODO: add to snapshots
        except Exception as e: 
            self.logger.log_exception("Sample generation failed to complete. Traceback:")
            self.exception.display_error(error=e)

    def _quota(self, df, dataset_name, col, sample_size): 
        """Quota sampling algo

        Args:
            df (pandas dataframe): currently loaded dataset
            dataset_name (str): name of dataset
            col (_type_): _description_
            sample_size (_type_): _description_
        """
        ...

    def _judgment(self, df, dataset_name, rows_of_operations): 
        """Judgment sampling algo

        Args:
            df (pandas dataframe): currently loaded dataset
            dataset_name (str): name of dataset
            rows_of_operations (list): List of nested row objects.
        """
        try: 
            new_sample = self.model.sample.judgment(df=df, rows_of_operations=rows_of_operations)
            # TODO: add to snapshots
        except Exception as e: 
            self.logger.log_exception("Sample generation failed to complete. Traceback:")
            self.exception.display_error(error=e)

    def _showball(self, df, dataset_name, rows_of_operations): 
        """Snowball sampling algo

        Args:
            df (pandas dataframe): currently loaded dataset
            dataset_name (str): name of dataset
            rows_of_operations (list): list of nested row objects
        """
        try: 
            new_sample = self.model.sample.snowball(df=df, rows_of_operations=rows_of_operations)
            # TODO: add to snapshots
        except Exception as e: 
            self.logger.log_exception("Sample generation failed to complete. Traceback:")
            self.exception.display_error(error=e)

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
        self.frame.generate_button.bind("<Button-1>", self._generate)
        self.frame.sampling_algo_menu.bind("<Configure>", self._get_algorithm_info)