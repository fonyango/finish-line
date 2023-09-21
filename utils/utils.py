import os
import json
import pymongo
import pandas as pd
from bson import json_util, ObjectId

class Starter():
    def __init__(self, mongo_data):

        self.mongo_data = mongo_data

    def set_up_database(self):
        """
        Set up mongo db
        """
        MONGO_CREDENTIALS = os.environ.get("MARATHON_DATA_MONGO_CREDENTIALS")
        DB_NAME = os.environ.get("MARATHON_DB_NAME")
        client = pymongo.MongoClient(MONGO_CREDENTIALS)
        database_client = client[DB_NAME]

        print(f"Connected to ..... {DB_NAME}",file=sys.stderr)

        return database_client

    def mongo_to_dataframe(self):
        """
        transform mongo data to a pandas dataframe
        """
        sanitized = json.loads(json_util.dumps(self.mongo_data))
        normalized = pd.json_normalize(sanitized)
        
        df = pd.DataFrame(normalized)

        return df