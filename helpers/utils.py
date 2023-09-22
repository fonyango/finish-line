import os
import json
import pymongo
import pandas as pd
from bson import json_util, ObjectId
from decouple import config
import sys

class Starter():

    def set_up_database(self):
        """
        Set up mongo db
        """
        MONGO_CREDENTIALS = config("MARATHON_DATA_MONGO_CREDENTIALS")
        DB_NAME = config("MARATHON_DB_NAME")
        client = pymongo.MongoClient(MONGO_CREDENTIALS)
        database_client = client[DB_NAME]

        print(f"Connected to ..... {DB_NAME}",file=sys.stderr)

        return database_client

    def mongo_to_dataframe(self,mongo_data):
        """
        transform mongo data to a pandas dataframe
        """
        sanitized = json.loads(json_util.dumps(mongo_data))
        normalized = pd.json_normalize(sanitized)
        
        df = pd.DataFrame(normalized)

        return df