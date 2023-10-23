import pandas as pd
import random

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
                "Reminder, a new snapshot will be created in the process of generating a sample. To under or" +
                " roll-back the dataframe to a state prior to the sample generation, do so at the Manipulation" +
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
            "Quota": 
                "Quota Sampling \n\nA non-random method that involves dividing the population into subgroups" +
                " or strata and then selecting participants non-randomly based on a specific quota or predefined" + 
                " criteria. (Wikipedia, https://en.wikipedia.org/wiki/Quota_sampling)", 
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
    
