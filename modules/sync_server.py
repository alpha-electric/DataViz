print(__name__)

print(__file__)

# from multiprocessing.managers import SyncManager

import os
import pandas as pd
from config import Config
class Server_Syncer():

    def __init__(self) -> None:
        pass

    def sync_csv(self,csv_path: str)-> None:
        df = pd.read_csv(csv_path)
        # either derive from path or as part of extracting the key value store
        battery_id = 2
        self.sync_df(battery_id,df)

    def sync_excel(self,excel_path: str, sheet_name: str)-> None:
        print("os.getcwd()")
        print(os.getcwd())
        df = pd.read_excel(excel_path,sheet_name=sheet_name,engine="openpyxl")
        battery_id = 2
        self.sync_df(battery_id,df)

    def sync_df(self, battery_id,df):
        print(df.describe())
        Config.DB.batch_add_battery_infos(battery_id,df)


