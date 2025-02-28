import time
import pandas as pd
from datetime import datetime
from loguru import logger
from bs4 import BeautifulSoup
from sqlalchemy import Engine
from selenium.webdriver.common.by import By

from ._pet_products_etl import PetProductsETL
from .utils import execute_query, update_url_scrape_status, get_sql_from_file

SHOP = "PetPlanet"
BASE_URL = "https://www.petplanet.co.uk"
CATEGORIES = {
    "dog_food": "/d7/dog_food", 
    "dog_products": "/d2/dog_products", 
    "cat_food": "/d34/cat_food", 
    "cat_products": "/d3/cat_products", 
    "other_small_furries": "/d298/other_small_furries", 
    "pet_health": "/d2709/pet_health"
}

class PetPlanetETL(PetProductsETL):
    
    def transform(self, soup: BeautifulSoup, url: str):
        pass

    def get_links(self, category: str) -> pd.DataFrame:
        # Data validation on category
        cleaned_category = category.lower()
        if cleaned_category not in CATEGORIES.keys():
            raise ValueError(f"Invalid category. Value must be in {CATEGORIES}")
        
        path = CATEGORIES[cleaned_category]
        url = f"{BASE_URL}{path}"

        urls = []

        
        
        df = pd.DataFrame({"url": urls})
        df.drop_duplicates(inplace=True)
        df.insert(0, "shop", SHOP)

        return df

    def run(self, db_conn: Engine, table_name: str):
        pass

    def refresh_links(self, db_conn: Engine, table_name: str):
        execute_query(db_conn, f"TRUNCATE TABLE {table_name};")

        for category in CATEGORIES:
            df = self.get_links(category)
            self.load(df, db_conn, table_name)

        sql = get_sql_from_file("insert_into_urls.sql")
        execute_query(db_conn, sql)