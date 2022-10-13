This folder saves the code for cleaning the ingredients of recipes from Kochbar.de
The process is described as follows:
- After getting the original datasets from the Uni server, the "step_one" was applied to delete the non-ingredient terms (as described in the thesis).
- Before starting the data cleaning, I split the ingredient lists by ',', leading to the ingredients contain only one word (e.g., Salz, Zucker), two words (e.g.), three words (e.g.), and longer ones (e.g.). Thus you can see the sub-folders in this folder named such as 'one_ingr_processing','two_ingr_processing', etc.
- In order to apply the Google Translation API (which can translate 500,000 characters per month) for free and improve the efficiency of the processing, I firt did the data cleaning on the German ingredient lists, including normalising the ingredients by combining the same ingredient with different names (due to dialects or typos, for example), and deleting the non-ingredient terms, etc. 
- There were several steps for dealing with the ingredients. Each step of cleaning genreating new dataset, which would be the input for the next step. For example, you may see 'one_ingr_processing_001', which followed by 'one_ingr_processing_002', etc.
- After dealing with the German ingredients, Google Translation API was applied to translate these into English.
- The automatic translation was done manually, some changes were done with Numbers on my Mac.
