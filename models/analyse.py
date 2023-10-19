import plotly.express as px
import plotly.graph_objects as go
from pandas import pivot_table as pt
from pandas import DataFrame

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

    def summarise_column(self, var): 
        """Descriptive statistics of individual columns of data. 
        Not to be confused with summary_statistics() method.

        Args:
            var (str): variable (column) a column of dataframe 

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
        null_count = var.isnull().sum()

        summary = {
            "Min": var.min(), 
            "Max": var.max(),
            "Mean": var.mean(),
            "Median": var.median(),
            "Mode": var.mode()[0], # Mode returns dataframe, index 0 is actual value
            "Null Count": null_count,
            "SD": var.std(),
            "Variance": var.var(),
            "IQR": iqr,
            "Outlier Count": outlier_count,
            "Skew": var.skew(),
            "Kurtosis": var.kurt()
        }
        return {key: value for key, value in summary.items()} 
    
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
        return {key: value for key, value in temp_dict.items()} # rounding
    
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
        
    def descriptive_statistics(self, df, row_count): 
        """Calculate descriptive statistics for entire pandas datafram (dataset). 

        Args:
            dataframe (pandas dataframe): from dataset model method call
            row_count (int): Number of rows 

        Returns: 
            Dictionary of results to be used in tree view.
        """
        non_null = df.count()
        descriptive_stats = DataFrame({
            "#": range(1, len(df.columns) + 1), 
            "Column": df.columns, 
            "Non-Null Count": non_null, 
            "Null Count": non_null - row_count, 
            "Data Type": df.dtypes
        })
        return ["descriptive", descriptive_stats]

    def summary_statistics(self, df): 
        """Pandas describe() method used to return description of entire dataset. i.e. 
        Summary statistics in the first panel of Analyse view.

        Args:
            df (pandas dataframe): from dataset model method call.

        Returns: list consisting of mode i.e. "numerical" or "categorical", and pandas dataframe
        """
        summary_stats = df.describe()

        if self._type_compatibility(mode="any", type_group="numeric", df=df):
            return ["numeric", summary_stats]
        elif self._type_compatibility(mode="any", type_group="categorical", df=df):
            return ["categorical", summary_stats] # won't reach here unless non are numeric
        else: # nothing to show!
            return ["null", summary_stats]
    
    def correlation_analysis(self, df): 
        """Pandas corr() method used to return correlation analysis of entire dataset.

        Args:
            df (pandas dataframe): from dataset model method call

        Returns: either string value indicating non compatibility of analysis on 
        the particular df or a DICTIONARY object with the results
        """
        result = self._type_compatibility(mode="all", type_group="numeric", df=df)
        if result: # True
            correlation_stats = df.corr() 
            return ["numeric", correlation_stats]
        else: 
            return ["null", 0]
    
    def _type_compatibility(self, mode, type_group, df): 
        """Preprocessing task, check if type of column or entire dataset is or contains types
        that will not work on particular analysis operations. 

        Args:
            mode (str): "any" or "all", depending on what is required, if any exists, will return true
                otherwise, only if all exists will return true. 
            type_group (str): "numeric", "categorical", "boolean", "datetime".
            df (pandas dataframe): pandas dataframe

        Returns: Boolean value
        """
        types = {
            "numeric": (
                "int64", "int32", "int16", "int8", "float64", "float32", "complex", "UInt8", "UInt16",
                "UInt32", "UInt64", "int64Dtype", "float64Dtype"
                ), 
            "categorical": (
                "category", "object", "string", "StringDtype"
                ), 
            "boolean": (
                "bool",
                ), 
            "date_time": (
                "datetime64", "timedelta64", "period"
                )
        }
        check = []
        all_dtypes = set()
        for coltype in df.dtypes: 
            all_dtypes.add(str(coltype))
        
        if mode == "any": 
            for _type in all_dtypes:
                if _type in types[type_group]:
                    check.append(_type)
            if len(check) >= 1:
                return True
            else:
                return False
                    
        elif mode == "all":
            for _type in all_dtypes:
                if _type not in types[type_group]:
                    return False
            return True