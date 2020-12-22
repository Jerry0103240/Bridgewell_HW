import mysql.connector
import numpy as np
import logging
import threading

db_settings = {"host":"",
               "account":"",
               "password":"",
               "database":"dsp_rtb",
               "table":"ad_settings"}

class MySQL():
    def __init__(self, db_settings):
        """
        Initialize MySQL settings

            Parameters
            ----------
            db_settings : database settings (host, account, password, database, table)
        """
        self.host = db_settings["host"]
        self.account = db_settings["account"]
        self.password = db_settings["password"]
        self.database = db_settings["database"]
        self.table = db_settings["table"]
        self.connection = mysql.connector.connect(
            host=self.host,
            database=self.database,
            user=self.account,
            password=self.password)
        self.cursor = self.connection.cursor()

    def execute(self, sql):
        """
        MySQL execution

            Parameters
            ---------
            sql : MySQL statements
        """
        self.cursor.execute(sql)

    def commit(self):
        self.connection.commit()

    def delete(self, id):
        """
        MySQL execution

            Parameters
            ---------
            id : Delete data of chosen id from table
        """
        ad_settings = self.fetch_all_data()
        if len(ad_settings) >= id:
            self.execute(f"DELETE FROM `{sql.database}`.`{sql.table}` WHERE creative_id={id};")
            self.commit()
        else:
            print(f"creative_id {id} does not exist!")

    def insert(self, status, bidding_cpm):
        """
        Insert data into table

            Parameters
            ---------
            status : true or false
            bidding_cpm : integers, cost per thousand impressions
        """
        self.execute(f"INSERT INTO `{sql.database}`.`{sql.table}` (`status`, `bidding_cpm`) VALUES ({status}, {bidding_cpm});")
        self.commit()

    def fetch_all_data(self):
        """
        Return all data from chosen table.
        """
        self.execute(f"SELECT * FROM {self.database}.{self.table};")
        record = self.cursor.fetchall()
        return record

    def fetch_id_data(self, id):
        """
        Return id data from chosen table.
        """
        ad_settings = self.fetch_all_data()
        if len(ad_settings) >= id:
            self.execute(f"SELECT * FROM {self.database}.{self.table} WHERE creative_id={id};")
            record = self.cursor.fetchone()
            return record
        else:
            print(f"creative_id {id} does not exist!")

    def fetch_filtered_data(self, sql):
        """
        Return filtered data from chosen table.

            Parameters
            ---------
            sql : MySQL statements
        """
        self.execute(sql)
        record = self.cursor.fetchall()
        return record

    def bidding_strategy(self, bid_floor):
        """
        Return highest bidding price & creative_id

            Parameters
            ---------
            bid_floor : lowest price to be accepted
        """
        logging.basicConfig(level=logging.INFO)
        ad_settings = self.fetch_filtered_data(f"SELECT * FROM {self.database}.{self.table} where status=1;")
        logging.info(f"Number of qualified data : {len(ad_settings)}")
        logging.info(f"Number of unqualified data : {len(self.fetch_all_data())-len(ad_settings)}")
        max_price = 0
        highest_id = 0
        logging.info("\nBidding process start...")
        for i in range(0, len(ad_settings)):
            rdn = (np.random.randint(1,10))
            bid_price = ad_settings[i][2] * (rdn % ad_settings[i][0])
            logging.info(f"creative_id:{ad_settings[i][0]}, status:{ad_settings[i][1]}, bidding_price:{ad_settings[i][2]}")
            logging.info(f"creative_id {ad_settings[i][0]}'s bid_price = {bid_price}, strategy->({ad_settings[i][2]}(bidding_cpm) * ({rdn}(random) % {ad_settings[i][0]}(creative_id))))")
            logging.info("-------------------------------------------------------------------------------------------")
            if bid_price > max_price:
                max_price = bid_price
                highest_id = ad_settings[i][0]

        if max_price < bid_floor:
            logging.info("\nAll bidding prices are lower than bid_floor!")
            logging.info("Bidding process end...")
            return None
        else:
            logging.info("Bidding process end...")
            logging.info(f"Highest qualified price={max_price}, creative_id={highest_id}, send response to SSP-client!")
            return {"price" : max_price, "creative_id" : highest_id}

if __name__ == "__main__":
    sql = MySQL(db_settings)
    sql.fetch_all_data()