# If this file doesn't run by itself, i'll just run it from a main function
from config import Config, DbType
from modules.sync_server import Server_Syncer
# from modules.sql_interface import SQL_Interface


print(Config)

#Stores global variables for this app
app = Config
print(app.base_path)
print(app.DB_PATH)
print(app.SQLALCHEMY_DATABASE_URI)

# Configure the applicati
if __name__ == '__main__':
    # trying = Server_Syncer()
    # trying.sync_csv("sampleFiles/testing.csv")
    # trying.sync_excel("sampleFiles/0000000015e46514 Range Test 07012022.xlsx","combined-csv-files")
    
    res1 = Config.DB.get_battery_by_name()
    print(res1)
    bat_id = res1[0]["battery_id"]
    # Config.DB.get_battery_info_by_daterange(res1[0]["battery_id"])
    Config.DB.get_earliest_battery_time(bat_id)
    Config.DB.get_latest_battery_time(bat_id)