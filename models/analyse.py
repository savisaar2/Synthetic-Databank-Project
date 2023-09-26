import plotly.express as px
import plotly.graph_objects as go
from pandas import pivot_table as pt
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
        # Configure styles
        match mode: 
            case "Box":
                plot = px.box(y=var_a, title=title)
            case "Histogram": 
                plot = go.Figure(data=[go.Histogram(x=var_a, nbinsx=20)])
                plot.update_layout(title=title)
            case "Line": 
                plot = px.line(y=var_a, title=title)
            case "Scatter": 
                plot = px.scatter(x=var_a, y=var_b, title=title)
            case "Violin": 
                plot = px.violin(y=var_a, box=True, title=title)

        # Configure plot attributes
        if mode in ["Box", "Violin"]: 
            plot.update_traces(marker=dict(size=2)) # size of dots
        elif mode in ["Scatter"]: 
            plot.update_traces(marker=dict(size=3))

        plot.update_xaxes(title_text=var_a.name)
        if mode == "Scatter": 
            plot.update_yaxes(title_text=var_b.name)
        else: 
            plot.update_yaxes(title_text="")
        
        plot.show()

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

