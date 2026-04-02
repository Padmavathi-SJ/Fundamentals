import pandas as pd #for CSV
from datetime import date
import os # to handle folders

def generate_report(changes):
    if not changes:
        print("No price changes found.")
        return
    
    data = []
    
    for name, old, new in changes:
        change = ((new - old) / old) * 100 #calculate % change
        data.append([name, old, new, round(change, 2)])
   
    df = pd.DataFrame(data, columns=["Product", "Old Price", "New Price", "Change %"])

    os.makedirs("reports", exist_ok=True) #create folder if not exists
    filename = f"reports/{date.today()}.csv"
    
    df.to_csv(filename, index=False) #save dataframe to csv without index

    print(f"Report saved to {filename}")