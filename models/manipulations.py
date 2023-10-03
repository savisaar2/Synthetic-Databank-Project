
from pandas import *
class ManipulationsModel():
    def __init__(self):
        """
        Initialise the ManipulationsModel component of the application.

        This class represents the ManipulationsModel component of the application's MVC (Model-View-Controller) architecture.
        It initialises the models to be consumed by the controllers of this applicaiton.
        """
        super().__init__()
        self._manip_collection()
        self._schedule_set = []

    def _manip_collection(self):
            self.manip_collection = {
                 "add_noise": "add noise function"
                 
            }
    
    def churner(scheduler_row):
        # for r in scheduler_row:
        #     manip_collection[r["action"]](r["args"])
            pass

