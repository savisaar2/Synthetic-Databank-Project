import plotly.offline as pyo
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

    def plot_visualisation(self, mode, title, var_a, var_b, df_ref):
        """Plot!

        Args:
            mode (str): Type of graph
            title (str): Name of the dataset
            var_a (str): selected column
            var_b (str): selected column
            df_ref (pandas Dataframe): reference to the currently loaded dataframe
        """
        # Configure styles
        match mode: 
            case "Box":
                plot = px.box(y=var_a, title=title)
            case "Histogram": 
                plot = go.Figure(data=[go.Histogram(x=var_a, nbinsx=20)])
                plot.update_layout(title=title)
            case "Heat Map":
                heatmap = go.Heatmap(z=df_ref.values, x=df_ref.columns, y=df_ref.index, colorscale="Viridis")
                layout = go.Layout(title=title)
                plot = go.Figure(data=[heatmap], layout=layout)
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

        if mode == "Scatter": 
            plot.update_yaxes(title_text=var_b.name)
        else: 
            plot.update_yaxes(title_text="")

        if mode != "Heat Map":
            plot.update_xaxes(title_text=var_a.name)
                    
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
        q1 = self._q1(var=var)
        q3 = self._q3(var=var)
        iqr = self._iqr(q3=q3, q1=q1)
        lower_bound = self._lower_bound(q1=q1, iqr=iqr)
        upper_bound = self._upper_bound(q3=q3, iqr=iqr)
        identified_outliers = (var < lower_bound) | (var > upper_bound)
        outlier_count = identified_outliers.sum()
        null_series = var == self._typify(null_val) # pandas series of Boolean values

        summary = {
            "Min": var.min(), 
            "Max": var.max(),
            "Mean": var.mean(),
            "Median": var.median(),
            "Mode": var.mode()[0], # Mode returns dataframe, index 0 is actual value
            "Null Count": null_series.sum(), # counts all True values in series
            "SD": var.std(),
            "Variance": var.var(),
            "IQR": iqr,
            "Outlier Count": outlier_count,
            "Skew": var.skew(),
            "Kurtosis": var.kurt()
        }
        return {key: round(value, rounding) for key, value in summary.items()} # rounding
    
    def _typify(self, null_val): 
        """Convert null_val as specified by user into the correct type. 

        Args:
            null_val (_type_): _description_

        Returns:
            _type_: _description_
        """
        try: 
            converted = float(null_val)
            return converted
        except Exception as e: 
            return null_val # likely string or empty? TODO: use raise

    def _iqr(self, q3, q1):
        """IQR - inter quartile range

        Args:
            q3 (float): first quartile
            q1 (float): third quartile

        Returns:
            float: IQR value
        """
        return q3 - q1
        
    def _q1(self, var): 
        """1st quartile

        Args:
            var (str): selected column

        Returns:
            float: Returns calculated value of 1st quartile of a given column of data.
        """
        return var.quantile(0.75)
    
    def _q3(self, var): 
        """3rd quartile

        Args:
            var (str): selected column

        Returns:
            float: Returns calculated value of 3rd quartile of a given column of data.
        """
        return var.quantile(0.75)
    
    def _lower_bound(self, q1, iqr):
        """Lower bound calculation

        Args:
            q1 (float): first quartile value
            iqr (float): IQR value

        Returns:
            float: lower bound value
        """
        return q1 - 1.5 * iqr

    def _upper_bound(self, q3, iqr):
        """Upper bound calculation

        Args:
            q3 (float): third quartile value
            iqr (float): IQR value

        Returns:
            float: upper bound value
        """
        return q3 + 1.5 * iqr
        
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
        pivot_calculation = pt(data=df, values=vals, index=cat, aggfunc=agg)
        temp_dict = pivot_calculation.to_dict()[vals] # return in following sample format {"cat1": 333, "cat2": 444}
        return {key: round(value, rounding) for key, value in temp_dict.items()} # rounding
    
    def convert_to_number(self, val): 
        """Convert 

        Args:
            val (str): user specified input.

        Returns:
            int: value
        """
        if val.isdigit(): 
            return int(val)
        else: 
            raise ValueError
            

