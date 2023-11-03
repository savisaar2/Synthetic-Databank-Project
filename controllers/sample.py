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
        
        output = self._validate_user_input()

        if output != False: # passed all validation! 
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
                case "Judgment": 
                    self._judgment(
                        df=df, dataset_name=ds_name, 
                        rows_of_operations=self.frame.get_reference_to_rows_of_operations()
                    )
                case "Snowball": 
                    result = self._showball(
                        df=df, dataset_name=ds_name, 
                        rows_of_operations=self.frame.get_reference_to_rows_of_operations(), 
                        sample_size=int(self.frame.get_snowball_sample_size_entry()) # guaranteed as post validation
                    )
                    if result == False: 
                        return

            self._post_generation_tasks(algo_selection=algo_selection)
            
    def _post_generation_tasks(self, algo_selection): 
        """Post generation tasks

        Args: 
            algo_selection (str): name of selected algorithm.
        """
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-7]
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
        
    def _validate_user_input(self): 
        """First step prior to generation of samples.
        Returns False if exception occurs. Otherwise returns dictionary of user inputs.
        """
        algo_selection = self.frame.get_sample_algo_menu_selection()
        row_count = self.model.DATASET.get_df_row_count()

        match algo_selection: 
            case "Simple Random":
                return self._assert_property(
                    getter=self.frame.get_sample_size_entry, row_count=row_count, label="sample size"
                    )
            case "Stratified": 
                return self._assert_property(
                    getter=self.frame.get_strat_sample_size_entry, row_count=row_count, label="sample size"
                    )
            case "Systematic": 
                return self._assert_property(
                    getter=self.frame.get_systematic_interval_entry, row_count=row_count, label="sampling interval"
                    )
            case "Under" | "Over":
                return True # no validation required
            case "Cluster": 
                return self._assert_property(
                    getter=self.frame.get_cluster_sample_size_entry, row_count=row_count, label="sample size"
                )
            case "Judgment" | "Snowball": 
                if algo_selection == "Snowball": 
                    if self._assert_property(
                        getter=self.frame.get_snowball_sample_size_entry, row_count=row_count, label="sample size"
                    ) == False: 
                        return False 
                    
                all_true_lock = []
                
                for index, row in enumerate(self.frame.get_reference_to_rows_of_operations()): 
                    try: # try and convert condition to same datatype as Criteria
                        condition_value = row.convert_condition_to_criteria()
                    except AssertionError as e:
                        self.exception.display_error(error=f"Row {index + 1}'s {e}")
                        return False
                    else: 
                        all_true_lock.append(True)
                    
                if all(all_true_lock): # True
                    return {f"{algo_selection}": condition_value}
    
    def _add_generated_dataset_to_snapshot(self, df, algo, description): 
        """_summary_

        Args:
            df (pandas dataframe): ...
            algo (str): name of the sampling algorithm
            description: arguments / conditions for algo
        """
        self.model.DATASET.add_generated_dataset_to_snapshot(
            df=df, dataset_name="Sampled Dataset",
            schedule_set=[{
                    "step": 1, "action": f"{algo}", "sub_action": f"{description}",
                    "args": {"": "", "": "", "": ""}, "column": "", "outcome": "Success"
                    }]
            )

    def _simple_random(self, df, dataset_name, sample_size): 
        """Simple random sampling.

        Args:
            dataset_name (str): name of dataset
            df (pandas dataframe): currently loaded dataset
        """
        try: 
            new_sample = self.model.sample.simple_random(df=df, sample_size=sample_size)
            self._post_sampling_tasks(
                df=new_sample, snapshot_algo_name="Simple Sampling", 
                description=f"Sample Size: {sample_size}", algo_name="Simple Random", 
                configs={"sample_size": sample_size}
                )
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
            self._post_sampling_tasks(
                df=new_sample, snapshot_algo_name="Stratified Sampling", 
                description=f"Sample Size: {sample_size}, Dependant Column: {dependant_col}", algo_name="Stratified", 
                configs={"sample_size": sample_size, "dependant_col": dependant_col}
                )
        except ValueError as e: 
            self.logger.log_exception("Sample generation failed to complete. Traceback:")
            self.exception.display_error("Selected column either contains NaN or is a non categorical column of data.")
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
            self._post_sampling_tasks(
                df=new_sample, snapshot_algo_name="Systematic Sampling", 
                description=f"Sample Interval: {interval}", algo_name="Systematic", 
                configs={"interval": interval}
                )
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
            self._post_sampling_tasks(
                df=new_sample, snapshot_algo_name="Under Sampling", 
                description=f"Target Column: {target_col}", algo_name="Under", 
                configs={"target_col": target_col}
                )
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
            self._post_sampling_tasks(
                df=new_sample, snapshot_algo_name="Over Sampling", 
                description=f"Target Column: {target_col}", algo_name="Over", 
                configs={"target_col": target_col}
                )
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
            self._post_sampling_tasks(
                df=new_sample, snapshot_algo_name="Cluster Sampling", 
                description=f"Sample Size: {sample_size}, Cluster Column: {cluster_col}", algo_name="Cluster", 
                configs={"sample_size": sample_size, "cluster_col": cluster_col}
                )
        except Exception as e: 
            self.logger.log_exception("Sample generation failed to complete. Traceback:")
            self.exception.display_error(error=e)

    def _judgment(self, df, dataset_name, rows_of_operations): 
        """Judgment sampling algo

        Args:
            df (pandas dataframe): currently loaded dataset
            dataset_name (str): name of dataset
            rows_of_operations (list): List of nested row objects.
        """
        try: 
            new_sample = self.model.sample.judgment_or_snowball(
                mode="Judgment", df=df, rows_of_operations=rows_of_operations
                )
            self._post_sampling_tasks(
                df=new_sample, snapshot_algo_name="Judgment Sampling", 
                description="Multi-row criteria sampling", algo_name="Judgment", rows=rows_of_operations
                )
        except Exception as e: 
            self.logger.log_exception("Sample generation failed to complete. Traceback:")
            self.exception.display_error(error=e)

    def _showball(self, df, dataset_name, rows_of_operations, sample_size): 
        """Snowball sampling algo

        Args:
            df (pandas dataframe): currently loaded dataset
            dataset_name (str): name of dataset
            rows_of_operations (list): list of nested row objects
            sample_size (int): integer value to specify sample size.
        """
        try: 
            new_sample = self.model.sample.judgment_or_snowball(
                mode="Snowball", df=df, rows_of_operations=rows_of_operations, sample_size=sample_size
                )
            new_sample_length = len(new_sample)
            if new_sample_length < sample_size: 
                add_more_rows = self.exception.display_confirm(
                    message=f"Snowball sampling configuration produced {new_sample_length} samples. \n" +
                    "YES to amend or add more criteria. NO to finalise."
                    )
                if add_more_rows: 
                    return False
                else: # finalise
                    self._post_sampling_tasks(
                        df=new_sample, snapshot_algo_name="Snowball Sampling", 
                        description="Multi-row criteria sampling", algo_name="Snowball", rows=rows_of_operations
                        )
            else: # over sample size definition 
                confirm_excess = self.exception.display_confirm(
                    message=f"Snowball sampling produced {new_sample_length - sample_size} more than sample size.\n" +
                    "YES to keep excess and finalise or NO to manually amend (e.g. remove row(s))."
                )
                if confirm_excess: 
                    self._post_sampling_tasks(
                        df=new_sample, snapshot_algo_name="Snowball Sampling", 
                        description="Multi-row criteria sampling", algo_name="Snowball", rows=rows_of_operations
                        )
                else: 
                    return False
        except Exception as e: 
            self.logger.log_exception("Sample generation failed to complete. Traceback:")
            self.exception.display_error(error=e)

    def _post_sampling_tasks(self, df, snapshot_algo_name, description, algo_name, configs=None, rows=None): 
        """Add successfully generated sample to snapshots.
        """
        self._add_generated_dataset_to_snapshot(
        df=df, algo=f"{snapshot_algo_name}", 
        description=f"{description}."
        )
        if algo_name in ["Judgment", "Snowball"]: 
            config_to_text = self._algo_config_to_text(algo_name=f"{algo_name}", rows=rows)
        else: 
            config_to_text = self._algo_config_to_text(algo_name=f"{algo_name}", configs=configs)
        self.logger.log_info(config_to_text) # log 
        self._display_algo_config(text=config_to_text) 
    
    def _get_algorithm_info(self, event):
        """Get text description of algorithm to display to user to provide guidence. 
        """
        selection = self.frame.get_sample_algo_menu_selection()
        if selection != "------": 
            description = self.model.sample.get_algorithm_info(selection=selection)
            self.frame.update_algorithm_description_info(text=description)
    
    def _algo_config_to_text(self, algo_name, configs=None, rows=None): 
        """Returns a formated string with appropriate algorithm configurations for use in 
        _log_algo_config and _show_algo_config.

        Args: 
            algo_name (str): name of the selected algorithm. 
            configs (dict): cater for basic algos
            rows (objects): cater for adv algos i.e., judgment and snowball
        """
        output = f"Sample - generated using: {algo_name} technique using the following configuration(s):\n"

        if algo_name == "Snowball": 
            output += f"Sample size: {self.frame.get_snowball_sample_size_entry()}\n"
        
        match algo_name: 
            case "Simple Random":
                output += f"Sample size: {configs['sample_size']}"
            case "Stratified": 
                output += f"Sample size: {configs['sample_size']} | Dependant column: {configs['dependant_col']}"
            case "Systematic": 
                output += f"Sampling interval: {configs['interval']}"
            case "Under" | "Over": 
                output += f"Target column: {configs['target_col']}"
            case "Cluster": 
                output += f"Sample size: {configs['sample_size']} | Cluster column: {configs['cluster_col']}"
            case "Judgment" | "Snowball":
                for row in rows:
                    vals = row.get_value_set()
                    logical_op = row._get_logical_operator()
                    output += f"Criteria: {vals['criteria']} | Comparison operator: {vals['comparison_op']} | Conditional value: {vals['conditional_val']} | Logical operator: {logical_op}\n"

        return output.rstrip()

    def _display_algo_config(self, text): 
        """Update algorithm description info section with user configuration information post sample generation.

        Args:
            text (str): return from _algo_config_to_text 
        """
        self.frame.update_algorithm_description_info(text=text)

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