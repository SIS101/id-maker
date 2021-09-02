import pandas
import os
source_dir = os.path.abspath(os.path.dirname(__file__))
pd = pandas.read_excel(os.path.join(source_dir,"PHARM072021.xlsx"))

print(pd.to_dict())