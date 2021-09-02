import pandas
import os
from PublicAPISDK import StidSDK

sdk = StidSDK("c68aeb8f9d542f5ea683cacfd6fff4dec4610ee2")
def handle_files(file):
    source_dir = os.path.abspath(os.path.dirname(__file__))
    pd = pandas.read_excel(os.path.join(source_dir,file))
    for stid in pd.values:
        form = dict()
        form["name"] = stid[0]
        form["nrc"] = str(stid[1])
        form["program"] = stid[2]
        form["stid"] = str(stid[3])
        form["valid_from"] = stid[4].date().strftime('%Y/%m/%d')
        form["valid_to"] = stid[5].date().strftime('%Y/%m/%d/')
        print("\n")
        print(f"Uploading {form['name']}: {form['stid']}")
        print(sdk.add_stid(form))

if __name__ == "__main__":
    handle_files("PHARM072021.xlsx")