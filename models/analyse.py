class AnalyseModel():
    def __init__(self):
        """
        Initialise the AnalyseModel component of the application.

        This class represents the AnalyseModel component of the application's MVC (Model-View-Controller) architecture.
        It initialises the models to be consumed by the controllers of this applicaiton.
        """
        super().__init__()

    def plot_visualisation(self, mode, title, var_a, var_b):
        """_summary_

        Args:
            mode (_type_): _description_
            title (_type_): _description_
            var_a (_type_): _description_
            var_b (_type_): _description_
        """
        ...

    def summarise(self, var, rounding, null_val): 
        """Descriptive statistics using pandas methods for speed! Bwazingly fwast!

        Args:
            var (str): variable (column) header
            rounding (int): integer value of the decimal rounding value.
            null_val (str): string value (user input)

        Returns:
            dict: dictionary of case to value mappings
        """
        ...
        
    def pivot(self, df, vals, cat, agg, rounding):
        """Pivot table. 

        Args:
            df (pd.dataframe): dataframe 
            vals (str): header name of the column containing the values.
            cat (str): header name of the column containing the categories.
            agg (str): selected aggregate function e.g. "mean".
            rounding (int): rounding value as per user intput from view.

        Returns:
            dict: A dictionary of category to aggregate function values.
        """
        ...

