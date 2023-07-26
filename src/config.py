import os
from dataclasses import dataclass

import pymongo
import streamlit as st


@dataclass
class EnvironmentVariable:
    mongo_db_url = os.getenv("MONGO_DB_URL")

    def __post_init__(self):
        if self.mongo_db_url is None:
            self.mongo_db_url = st.secrets['MONGO_DB_URL']


env_var = EnvironmentVariable()
mongo_client = pymongo.MongoClient(env_var.mongo_db_url)
TARGET_COLUMN = "class"
