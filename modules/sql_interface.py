from ast import Num
from multiprocessing import connection
import sqlite3
import pandas as pd
from sqlite3 import Error
from modules.db_interface import DbInterface
import hashlib
import numpy as np


from sqlalchemy import and_, create_engine, Table, MetaData, insert
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import asc, desc, func
import datetime, os, time
from models import Battery, BatteryInfo, MicroController, Location

from constants.batteries.battery_info_cols import bat_info_col as bicol


def datetimeToUnix(dt: datetime)->int:
    # print("datetimeToUnix")
    # print(dt)
    # print(type(dt))
    return time.mktime(dt.timetuple())

class SQL_Interface(DbInterface):

    sql_session = None
    engine = None
    connection = None
    config = {}
    def __init__(self, config):
        self.config = config
        self.DB_PATH = self.config.DB_PATH
        self.__create_session()
        self.__create_metadata_obj()
        self._create_tables()

    def __create_db(self):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(self.DB_PATH)
            print(sqlite3.version)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def __create_metadata_obj(self):
        self.metadata_obj = MetaData()

    def _create_tables(self):
        table_names = ["battery","battery_info","location","microController"]
        for name in table_names:
            if not self.__is_table_exist(name):
                self._create_table(name)
        print("TABLES CREATED")
        print('=' * 50)
    def _create_table(self, table_name: str):
        table_to_create = None
        if table_name == "battery":
            table_to_create = Battery
        elif table_name == "battery_info":
            table_to_create = BatteryInfo
        elif table_name == "location":
            table_to_create = Location
        elif table_name == "microController":
            table_to_create = MicroController
        
        if  table_name is None:
            return
        table_to_create.__table__.create(self.engine)

    def __create_session(self):
        # TODO add support for checking db exists
        if (not os.path.exists(self.DB_PATH)):
            self.__create_db()
        engine = create_engine(self.config.SQLALCHEMY_DATABASE_URI)  
        self.engine = engine
        self.connection = engine.connect()
        Session = sessionmaker()
        Session.configure(bind=engine)
        self.sql_session = Session()  \

        # HERE ON NEED BREAK DOWN INTO DIFFERENT GROUPS

    def __is_table_exist(self, table_name: str) -> bool:
        return self.engine.dialect.has_table(self.connection, table_name)

    def get_battery_sorted_by_cell_diff(self, num = 5):
        """
        Gets a list of battery(s) sorted in desc order

        Args:
            num: top "num" batteries to extract based on MOST_RECENT cell_diff

        Returns:
            List: list of batteries sorted in descending order
        
        """

    def get_battery_above_cell_diff(self, cell_diff = -1):
        """
        Gets a list of battery(s) above specified cell_diff

        Args:
            cell_diff: Threshold to extract batteries with MOST_RECENT cell_diff above this

        Returns:
            List: list of batteries
        
        """

    def get_top_n_batteries_by_V(self, num = 5, isAsc = True):
        """
        Gets a list of n battery(s) with highest/lowest overall voltage 

        Args:
            num: Top "num" batteries with highest/lowest overall voltage
            isAsc: If true, get lowest ones, else get highest ones

        Returns:
            List: list of batteries
        
        """

    def get_batteries_by_location(self, location_id):
        """
        Gets a list of battery(s) with a specific location

        Args:
            location_id: location_id of where battery is stationed

        Returns:
            List: list of batteries
        """

    def get_pinned_batteries(self):
        """
        Gets a list of battery(s) that are pinned by user

        Returns:
            List: list of batteries
        """


    def get_active_batteries(self):
        """
        Gets a list of active battery(s)

        Returns:
            List: list of batteries
        """

    def get_inactive_batteries(self):
        """
        Gets a list of inactive battery(s)

        Returns:
            List: list of batteries
        """

    def get_battery_by_name(self, name: str = "") -> str:
        """
        Gets a list of battery(s) by full/partial matching name

        Args:
            name: String to match against name

        Returns:
            List: list of batteries
        
        """
        name_search = "%{}%".format(name)
        bat = (
            self.sql_session.query(Battery)
            .filter(Battery.name.like(name_search))
            .all()
        )
        # print(bat)
        if (len(bat) == 0):
            return None
        # for record in bat:
        #     print(record.__dict__)
        return [x.__dict__ for x in bat]


    def get_earliest_battery_time(self, battery_id):
        bat_info = (
            self.sql_session.query(func.min(BatteryInfo.unix_timestamp))
            .filter(
                BatteryInfo.battery_id == battery_id,
            )
            .scalar()
        )
        print(bat_info)
        return bat_info

    def get_latest_battery_time(self, battery_id):
        bat_info = (
            self.sql_session.query(func.max(BatteryInfo.unix_timestamp))
            .filter(
                BatteryInfo.battery_id == battery_id,
            )
            .scalar()
        )
        print(bat_info)
        return bat_info

    def get_battery_info_by_daterange(self, battery_id, start=0, end=datetime.datetime.timestamp(datetime.datetime.now())):
        """
        Gets a list of battery info given a battery_id, start time and end time and

        Args:
            battery_id: Id of battery to examine
            start: Unix time stamp start of logging range
            end: Unix time stamp end of logging range

        Returns:
            List: list of battery infos sorted in ascending order

        """
        # print(battery_id)
        # print(start)
        # print(end)
        bat_info = (
            self.sql_session.query(BatteryInfo)
            .filter(
                BatteryInfo.battery_id == battery_id,
                and_(BatteryInfo.unix_timestamp >= start, BatteryInfo.unix_timestamp <= end)
            )
            .all()
        )
        print(len(bat_info))
        if (len(bat_info) == 0):
            return None
        return [x.__dict__ for x in bat_info]


    def get_pinned_locations(self):
        """
        Gets a list of locations pinned by user. This is useful if 
        we decide to focus on pilot programs at certain places and want to
        place more focus on them

        Returns:
            List: list of locations
        """

    
    def add_battery_infos(self, row):
        pass

    


    def batch_add_battery_infos(self, battery_id, df):
        print(f"batch_add_battery_infos: {battery_id}")
        
        # Check if battery exists
        bat = (
            self.sql_session.query(Battery)
            .filter(Battery.battery_id == battery_id)
            .one_or_none()
        )

        if bat is not None:
            print(f"bat {battery_id} exists")
        else:
            print(f"bat {battery_id} don't exist")
            bat = Battery(
                battery_id=battery_id,
                name = "MIAO"
            )
            self.sql_session.add(bat)
            self.sql_session.commit()

        def helper(x):
            dt_col = pd.to_datetime(x[bicol.datetime], infer_datetime_format=True) 
            u_time = datetimeToUnix(dt_col)
            # Check if datetime exists
            bat_info = (
                self.sql_session.query(BatteryInfo)
                .filter(
                    BatteryInfo.battery_id == battery_id,
                    BatteryInfo.unix_timestamp == u_time
                )
                .one_or_none()
            )
            if bat_info is not None:
                return np.nan
            return BatteryInfo(
                unix_timestamp = u_time,
                battery_id = battery_id,
                current = x[bicol.current],
                voltage = x[bicol.voltage],
                charge = x[bicol.charge],
                t1 = x[bicol.t1],
                t2 = x[bicol.t2],
                t3 = x[bicol.t3],
                charge_mos = x[bicol.charge_mos],
                discharge_mos = x[bicol.discharge_mos],
                v1 = x[bicol.v1],
                v2 = x[bicol.v2],
                v3 = x[bicol.v3],
                v4 = x[bicol.v4],
                v5 = x[bicol.v5],
                v6 = x[bicol.v6],
                v7 = x[bicol.v7],
                v8 = x[bicol.v8],
                v9 = x[bicol.v9],
                v10 = x[bicol.v10],
                v11 = x[bicol.v11],
                v12 = x[bicol.v12],
                v13 = x[bicol.v13],
                max_cell_diff = x[bicol.cellDiff]
            )
            

        CELL_COLS = ['v1', 'v2', 'v3', 'v4', 'v5', 'v6',
       'v7', 'v8', 'v9', 'v10', 'v11', 'v12', 'v13']
        # Compute cell diff
        def getMaxVoltageDiff(row):
            minVol = 10.0
            maxVol = -1
            for v_col in CELL_COLS:
                cur_vol = row[v_col]
        #         print(f"cur_vol: {cur_vol}")
                if cur_vol < minVol:
                    minVol = cur_vol
                if cur_vol > maxVol:
                    maxVol = cur_vol
        #     print(f"{maxVol} vs {minVol}")
            return maxVol - minVol

        df = df.dropna(subset=CELL_COLS)
        df[bicol.cellDiff] = df.apply(getMaxVoltageDiff, axis=1)

        objects = df.apply(helper,axis=1)
        objects.dropna(inplace=True)
        self.sql_session.add_all(objects.tolist())
        self.sql_session.commit()


# from config import Config
# if __name__ == '__main__':
#     Config.DB.get_battery_by_name()