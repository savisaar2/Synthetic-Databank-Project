from .dataset import DatasetModel
from .analyse import AnalyseModel

class Model:
    def __init__(self):
        """
        Initialise the Model component of the application.

        This class represents the Model component of the application's MVC (Model-View-Controller) architecture.
        It initialises the models to be consumed by the controllers of this applicaiton.
        """
        self.DATASET = DatasetModel()
        self.analyse = AnalyseModel()