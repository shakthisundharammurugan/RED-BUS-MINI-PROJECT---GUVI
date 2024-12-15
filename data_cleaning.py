import pandas as pd

##########################################################

def clean_data(data):
  df = pd.DataFrame(data)
  df["id"] = df.index
  df["Price"] = df["Price"].apply(lambda x: x.replace("INR", ""))
  df["Departure Time"] = pd.to_datetime(df["Departure Time"]).dt.time
  df["Reaching Time"] = pd.to_datetime(df["Reaching Time"]).dt.time
  df["Seat Availability"] = df["Seat Availability"].apply(lambda x: (x.split(" "))[0])
  df["Star Rating"] = df["Star Rating"].apply(lambda x: x.strip())
  df["Price"] = df["Price"].apply(lambda x: x.strip())
  df["Seat Availability"] = df["Seat Availability"].apply(lambda x: x.strip())
  
  for i in range(len(df)):
    try:
        df.at[i, "Star Rating"] = float(df.at[i, "Star Rating"])
    except ValueError:
        df.at[i, "Star Rating"] = None
        
  df["Price"] = df["Price"].apply(float)
  df["Seat Availability"] = df["Seat Availability"].astype(int)
  return df