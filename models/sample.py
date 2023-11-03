import os
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.utils import resample
import numpy as np


class SampleModel():
    def __init__(self):
        """
        Initialise the SampleModel component of the application.

        This class represents the SampleModel component of the application's MVC (Model-View-Controller) architecture.
        It initialises the models to be consumed by the controllers of this applicaiton.
        """
        super().__init__()
        self.sample_example_descriptions = {
            "------": 
                "Reminder, a new snapshot is created in the process of generating a sample. To undo or" +
                " roll-back the dataframe to a state prior to the sample generation, navigate to the Manipulation" +
                " page's rollback section.",
            "Simple Random": 
                "Simple Random Sampling (without replacement) \n\nInvolves randomly" +
                " selecting individuals or elements from a population without replacement. Each member of" +
                " the population has an equal and independent chance of being chosen for the sample. Once an" +
                " individual is selected, they are not placed back into the population, reducing the population size" +
                " for subsequent selections. (Latpate R, Kshirsagar J, Gupta VK & Chandre G, 2021, Advanced sampling" +
                " methods, Springer, Singapore)", 
            "Stratified": 
                "Stratified Sampling \n\nInvolves categorising a population into distinct groups, or" +
                " 'strata,' and then independently sampling from each stratum. Stratified sampling can be" +
                " particularly useful when working with categorical variables or class labels in a classification" +
                " problem. (Latpate R, Kshirsagar J, Gupta VK & Chandre G, 2021, Advanced sampling methods," + 
                " Springer, Singapore )", 
            "Systematic": 
                "Systematic Sampling \n\nObtained by selecting a random starting point in the" +
                " data frame and then taking every kth item (sampling interval k) in the frame till the desired" +
                " sample size is reached. You calculate the sampling interval by dividing the total population size" +
                " by the desired sample size. For example, if you have a population of 1,000 and you want a sample" + 
                " of 100, the sampling interval would be 10 (1,000/100 = 10). (Latpate R, Kshirsagar J, Gupta VK &" +
                " Chandre G, 2021, Advanced sampling methods, Springer, Singapore)",
            "Over": 
                "Over Sampling \n\nInvolves randomly duplicating existing samples from the" + 
                " minority class until the class balance is achieved. This could lead to overfitting. (Latpate R," +
                " Kshirsagar J, Gupta VK & Chandre G, 2021, Advanced sampling methods, Springer, Singapore)", 
            "Under": 
                "Under Sampling \n\nInvolves randomly selects a subset of instances from the majority" +
                " class, effectively reducing the number of majority class samples. The downside is that it may lead" +
                " to loss of information. (Latpate R, Kshirsagar J, Gupta VK & Chandre G, 2021, Advanced sampling" +
                " methods, Springer, Singapore)",
            "Cluster": 
                "Cluster Sampling \n\nIs a method where the population is divided into clusters, and a" + 
                " random sample of these clusters is selected instead of individual elements from the entire" + 
                " population. It's essential to make sure that the selected column or variable  used to define" +
                " clusters accurately represents meaningful groups in your dataset,  often based on factors" +
                " like geography or natural associations (e.g., schools, neighbourhoods, cities). (Latpate R," + 
                " Kshirsagar J, Gupta VK & Chandre G, 2021, Advanced sampling methods, Springer, Singapore)", 
            "Judgment": 
                "Judgment Sampling \n\nIn judgment sampling, the researcher or data collector uses their own" +
                " judgment and expertise to select specific individuals or elements for inclusion in the sample." +
                " The sample is selected based on the researcher's perception of which elements will best represent" +
                " the population or provide valuable insights. (Wikipedia" + 
                " https://en.wikipedia.org/wiki/Judgment_sample)", 
            "Snowball": 
                "Snowball Sampling \n\nA non-probabilistic or purposive sampling technique commonly used" + 
                " in research when it is difficult to identify and access members of a specific population or" + 
                " social group, such as hidden or marginalised populations. It relies on the use of existing" + 
                " participants or informants to refer and recruit additional participants. (Wikipedia," + 
                " https://en.wikipedia.org/wiki/Snowball_sampling)"
        }

    def get_algorithm_info(self, selection): 
        """Return example information for display in view. 

        Args:
            selection (str): menu item.
        """
        return self.sample_example_descriptions[selection]
    
    def convert_to_number(self, val, custom_error_warning): 
        """Convert user input / entry to number

        Args:
            val (str): user specified input.
            custom_error_warning (str): error string for overlay display.
        Returns:
            int: value
        """
        assert val.isdigit(), custom_error_warning
        return int(val.strip())
    
    def simple_random(self, df, sample_size): 
        """simple random algorithm. Hardcode random_state of 42.

        Args:
            df (pandas dataframe): reference to current pandas dataframe.
            sample_size (int): user input for sample size.
        """
        new_sample = df.sample(n=sample_size, replace=False, random_state=42)
        
        return new_sample
    
    def stratified(self, df, sample_size, dependant_col): 
        """Stratified sampling technique.

        Args:
            df (pandas dataframe): current loaded dataset.
            sample_size (int): size of sample in integer value.
            dependant_col (str): selected column name. 
        """
        stratified_shuffle_split = StratifiedShuffleSplit(n_splits=1, test_size=sample_size, random_state=42)
        for _, test_index in stratified_shuffle_split.split(df, df[dependant_col]): 
            new_sample = df.iloc[test_index]
        
        return new_sample

    def systematic(self, df, interval): 
        """Systematic sampling technique

        Args:
            df (pandas dataframe): current loaded dataset.
            interval (int): sampling interval
        """
        return df.iloc[::interval]

    def under_or_over_sampling(self, df, target_col, mode): 
        """Under sampling technique

        Args:
            df (pandas dataframe): current loaded dataset.
            target_col (str): value of selected column.
            mode (str): "over", or "under".
        """
        mode_toggle = {"under": False, "over": True}

        new_sample = df.dropna(subset=[target_col]) # drop rows with missing vals in the target col
        
        class_data = {} # separate data into classes
        for class_label in new_sample[target_col].unique(): 
            class_data[class_label] = new_sample[new_sample[target_col] == class_label]

        # specify desired sample size for under or over sampling (e.g., to balance classes)
        # adjust sample size based on your requirements, it may be set to the size of the smollest or largest class
        if mode == "under": 
            under_over_sample_size = min(len(class_data[class_label]) for class_label in new_sample[target_col].unique())
        elif mode == "over": 
            under_over_sample_size = max(len(class_data[class_label]) for class_label in new_sample[target_col].unique())

        under_over_sampled_classes = [] 
        for class_label in new_sample[target_col].unique(): # perform under or over sampling on each class
            class_data_under_over_sampled = resample(
                class_data[class_label], 
                replace=mode_toggle[mode], # no replacement to reduce samples
                n_samples=under_over_sample_size, # set size of smollest or largest class
                random_state=42
            )
            under_over_sampled_classes.append(class_data_under_over_sampled)

        balanced_data = pd.concat(under_over_sampled_classes) # combine under or sampled classes

        return balanced_data

    def cluster(self, df, sample_size, cluster_col): 
        """Cluster sampling technique

        Args:
            df (pandas dataframe): current loaded dataset.
            sample_size (int): size of sample
            cluster_col (str): target column
        """
        # calculate the proportion of each cluster in the population
        cluster_proportions = df[cluster_col].value_counts(normalize=True).to_dict()

        new_sample = pd.DataFrame() # empty df

        # iterate through unique clusters & sample with desired size
        for cluster, proportion in cluster_proportions.items(): 
            cluster_size = int(sample_size * proportion)
            cluster_sample = df[df[cluster_col] == cluster].sample(cluster_size)
            new_sample = pd.concat([new_sample, cluster_sample])

        return new_sample

    def judgment_or_snowball(self, mode, df, rows_of_operations, sample_size=None): 
        """Judgment or snowball sampling technique. Generalised as most functionality remains the same between
        the two algorithms. Differentiated by sample size (seed) for snowball.

        Args:
            mode (str): either "Judgment" or "Snowball".
            df (pandas dataframe): currently loaded dataset.
            rows_of_operations (list): list of all the row objects (instances).
            sample_size (int): only applicable if snowball is chosen.
        """
        def two_series_criteria(x, op, y): 
            """Returns x & y or x | y
            """
            if op == "AND": 
                return x & y
            elif op == "OR": 
                return x | y
        
        def calculate_individual_row(row_of_values): 
            """Calculate pandas series object based on criteria, comparison op and conditional val.

            Args:
                row_of_values (dict): takes one dictionary with row of values as defined in 
                instance i.e. return of method get_value_set

            Returns: instance of pandas.core.series.Series of single row to be chained if more rows exist.
            """
            match row_of_values["comparison_op"]: 
                case "EQUAL": 
                    return df[row_of_values["criteria"]] == row_of_values["conditional_val"]
                case "LESS": 
                    return df[row_of_values["criteria"]] < row_of_values["conditional_val"]
                case "MORE": 
                    return df[row_of_values["criteria"]] > row_of_values["conditional_val"]
                case "NOT EQUAL": 
                    return df[row_of_values["criteria"]] != row_of_values["conditional_val"]
        
        def cumulative_criteria(chain_of_pandas_series, chain_of_logical_ops): 
            """Calculate the cumulative criteria

            Args:
                chain_of_pandas_series (list): list of pandas Series objects
                chain_of_logical_ops (list): strings either "AND" or "OR"
            """
            num_of_rows = len(chain_of_pandas_series)
            
            if num_of_rows == 1: # no logical ops
                return chain_of_pandas_series.pop()
            elif num_of_rows == 2:
                x = chain_of_pandas_series.pop(0)
                y = chain_of_pandas_series.pop(0)
                op = chain_of_logical_ops.pop(0)
                return two_series_criteria(x=x, op=op, y=y)
            else: 
                last_row = chain_of_pandas_series.pop()
                index = 0 # counter
                while index < num_of_rows - 2: # length excluding last row plus start at index 0
                    x = chain_of_pandas_series.pop(0)
                    y = chain_of_pandas_series.pop(0)
                    op = chain_of_logical_ops.pop(0)
                    chain_of_pandas_series.insert( # add back prior to re-calculating.
                        0, two_series_criteria(x=x, op=op, y=y)
                    )
                    index += 1 
                x = chain_of_pandas_series.pop(0)
                op = chain_of_logical_ops.pop(0)
                return two_series_criteria(x=x, op=op, y=last_row)
        
        rows_of_values = [] # [{"criteria": colx, "comparison_op": "EQUALS", "conditional_val": 42}, n...]
        chain_of_logical_ops = [] # [OR, AND]
        chain_of_pandas_series = [] # output of single row calculations

        for row in rows_of_operations: # build collection of values and separate logical operators
            rows_of_values.append(row.get_value_set())
            chain_of_logical_ops.append(row._get_logical_operator())

        for row in rows_of_values: # build chain of individual pandas series
            chain_of_pandas_series.append(calculate_individual_row(row_of_values=row))

        criteria = cumulative_criteria(chain_of_pandas_series, chain_of_logical_ops)
        sample = df[criteria]
        judgment_sample = [sample] 
        judgment_sample_df = pd.concat(judgment_sample) # concat the judgment sample df into one df (caters multiple)
        judgment_sample_df.reset_index(drop=True, inplace=True) # reset index of final judgment sample

        return judgment_sample_df