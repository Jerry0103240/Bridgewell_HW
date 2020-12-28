import mysql.connector
import numpy as np
import datetime
from fastlogging import LogInit
import logging
import time

db_settings = {"host":"LAPTOP-KVNAQ9AK",
               "account":"root",
               "password":"MySQL",
               "database":"dsp_rtb",
               "table":"ad_settings_100"}

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

    def execute(self, query):
        """
        MySQL execution

            Parameters
            ---------
            query : MySQL statements
        """
        self.cursor.execute(query)

    def commit(self):
        self.connection.commit()

    def delete(self, database, table, creative_id):
        """
        MySQL execution

            Parameters
            ---------
            database : MySQL database
            table : MySQL table
            creative_id : Delete data of chosen id from chosen table
        """
        ad_settings = self.fetch_all_data(database, table)
        if len(ad_settings) >= creative_id:
            self.execute(f"DELETE FROM `{database}`.`{table}` WHERE creative_id={creative_id};")
            self.commit()
        else:
            print(f"creative_id {creative_id} does not exist!")

    def fetch_all_data(self, database, table):
        """
        Return all data from chosen table.

            Parameters
            ---------
            database : MySQL database
            table : MySQL table
        """
        self.execute(f"SELECT * FROM {database}.{table};")
        record = self.cursor.fetchall()
        return record

    def fetch_id_data(self, database, table, creative_id):
        """
        Return id data from chosen table.
        """
        ad_settings = self.fetch_all_data(database, table)
        if len(ad_settings) >= creative_id:
            self.execute(f"SELECT * FROM {database}.{table} WHERE creative_id={creative_id};")
            record = self.cursor.fetchone()
            return record
        else:
            print(f"creative_id {creative_id} does not exist!")

    def fetch_filtered_data(self, query):
        """
        Return filtered data from chosen table.

            Parameters
            ---------
            query : MySQL statements
        """
        self.execute(query)
        record = self.cursor.fetchall()
        return record

    def bidding_process(self, bid_floor):
        """
        Return highest bidding price & creative_id
        """
        all_data = self.fetch_all_data(database=self.database, table=self.table)
        ad_settings = self.fetch_filtered_data(f"SELECT * FROM {self.database}.{self.table} where status=1;")
        print(f"{datetime.datetime.now()}")
        print(f"Number of all ad_settings : {len(all_data)}")
        print(f"Number of qualified ad_settings : {len(ad_settings)}")
        print(f"Number of unqualified ad_settings : {len(all_data)-len(ad_settings)}")
        max_price = 0
        highest_id = 0
        print("\nBidding process start...")
        for i in range(0, len(ad_settings)):
            rdn = (np.random.randint(1,10))
            bid_price = ad_settings[i][2] * (rdn % ad_settings[i][0])
            print(f"creative_id:{ad_settings[i][0]}, status:{ad_settings[i][1]}, bidding_cpm:{ad_settings[i][2]}")
            print(f"creative_id {ad_settings[i][0]}'s bid_price = {bid_price}, strategy->({ad_settings[i][2]}(bidding_cpm) * ({rdn}(random) % {ad_settings[i][0]}(creative_id))))")
            print("-------------------------------------------------------------------------------------------")
            if bid_price > max_price:
                max_price = bid_price
                highest_id = ad_settings[i][0]
        if max_price < bid_floor:
            print("\nAll bidding prices are lower than bid_floor!")
            print("Bidding process end...")
            return None
        else:
            print("Bidding process end...")
            print(f"Highest qualified price={max_price}, creative_id={highest_id}, send response to SSP-client!")
            return {"price" : max_price, "creative_id" : highest_id}

    # def bidding_process(self, bid_floor):
    #     """
    #     Return highest bidding price & creative_id
    #     """
    #     logging.basicConfig(level=logging.INFO,
    #                         format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    #                         datefmt="%Y-%m-%d %H:%M",
    #                         handlers=[logging.FileHandler('DSP.log')])
    #     all_data = self.fetch_all_data(database=self.database, table=self.table)
    #     ad_settings = self.fetch_filtered_data(f"SELECT * FROM {self.database}.{self.table} where status=1;")
    #     logging.info(f"Number of all ad_settings : {len(all_data)}")
    #     logging.info(f"Number of qualified ad_settings : {len(ad_settings)}")
    #     logging.info(f"Number of unqualified ad_settings : {len(all_data)-len(ad_settings)}")
    #     max_price = 0
    #     highest_id = 0
    #     logging.info("\nBidding process start...")
    #     for i in range(0, len(ad_settings)):
    #         rdn = (np.random.randint(1,10))
    #         bid_price = ad_settings[i][2] * (rdn % ad_settings[i][0])
    #         logging.info(f"creative_id:{ad_settings[i][0]}, status:{ad_settings[i][1]}, bidding_cpm:{ad_settings[i][2]}")
    #         logging.info(f"creative_id {ad_settings[i][0]}'s bid_price = {bid_price}, strategy->({ad_settings[i][2]}(bidding_cpm) * ({rdn}(random) % {ad_settings[i][0]}(creative_id))))")
    #         logging.info("-------------------------------------------------------------------------------------------")
    #         if bid_price > max_price:
    #             max_price = bid_price
    #             highest_id = ad_settings[i][0]
    #     if max_price < bid_floor:
    #         logging.info("\nAll bidding prices are lower than bid_floor!")
    #         logging.info("Bidding process end...")
    #         return None
    #     else:
    #         logging.info("Bidding process end...")
    #         logging.info(f"Highest qualified price={max_price}, creative_id={highest_id}, send response to SSP-client!")
    #         return {"price" : max_price, "creative_id" : highest_id}

    # def bidding_process(self, bid_floor):
    #     """
    #     Return highest bidding price & creative_id
    #     """
    #     with open("history.txt", "w") as output:
    #         all_data = self.fetch_all_data(database=self.database, table=self.table)
    #         ad_settings = self.fetch_filtered_data(f"SELECT * FROM {self.database}.{self.table} where status=1;")
    #         output.write(f"Number of all ad_settings : {len(all_data)}\n")
    #         output.write(f"Number of qualified ad_settings : {len(ad_settings)}\n")
    #         output.write(f"Number of unqualified ad_settings : {len(all_data)-len(ad_settings)}\n")
    #         max_price = 0
    #         highest_id = 0
    #         output.write("Bidding process start...\n")
    #         for i in range(0, len(ad_settings)):
    #             rdn = (np.random.randint(1,10))
    #             bid_price = ad_settings[i][2] * (rdn % ad_settings[i][0])
    #             output.write(f"creative_id:{ad_settings[i][0]}, status:{ad_settings[i][1]}, bidding_cpm:{ad_settings[i][2]}\n")
    #             output.write(f"creative_id {ad_settings[i][0]}'s bid_price = {bid_price}, strategy->({ad_settings[i][2]}(bidding_cpm) * ({rdn}(random) % {ad_settings[i][0]}(creative_id))))\n")
    #             output.write("-------------------------------------------------------------------------------------------\n")
    #             if bid_price > max_price:
    #                 max_price = bid_price
    #                 highest_id = ad_settings[i][0]
    #         if max_price < bid_floor:
    #             output.write("All bidding prices are lower than bid_floor!\n")
    #             output.write("Bidding process end...\n")
    #             return None
    #         else:
    #             output.write("Bidding process end...\n")
    #             output.write(f"Highest qualified price={max_price}, creative_id={highest_id}, send response to SSP-client!\n")
    #             return {"price" : max_price, "creative_id" : highest_id}

    # def bidding_process(self):
    #     """
    #     Return highest bidding price & creative_id
    #     """
    #     with open("history.txt", "w") as output:
    #         all_data = self.fetch_all_data(database=self.database, table=self.table)
    #         ad_settings = self.fetch_filtered_data(f"SELECT * FROM {self.database}.{self.table} where status=1;")
    #         output.write(f"Number of all ad_settings : {len(all_data)}\n")
    #         output.write(f"Number of qualified ad_settings : {len(ad_settings)}\n")
    #         output.write(f"Number of unqualified ad_settings : {len(all_data)-len(ad_settings)}\n")
    #         max_price = 0
    #         highest_id = 0
    #         output.write("Bidding process start...\n")
    #         for i in range(0, len(ad_settings)):
    #             rdn = (np.random.randint(1,10))
    #             bid_price = ad_settings[i][2] * (rdn % ad_settings[i][0])
    #             output.write(f"creative_id:{ad_settings[i][0]}, status:{ad_settings[i][1]}, bidding_cpm:{ad_settings[i][2]}\n")
    #             output.write(f"creative_id {ad_settings[i][0]}'s bid_price = {bid_price}, strategy->({ad_settings[i][2]}(bidding_cpm) * ({rdn}(random) % {ad_settings[i][0]}(creative_id))))\n")
    #             output.write("-------------------------------------------------------------------------------------------\n")
    #             if bid_price > max_price:
    #                 highest_price = bid_price
    #                 highest_id = ad_settings[i][0]
    #                 random_int = rdn
    #                 bidding_cpm = ad_settings[i][2]
    #         self.execute(f"INSERT INTO `Id_Price` (`creative_id`, `bidding_price`, `random_int`, `bidding_cpm`) VALUES ({highest_price}, {highest_id}, {random_int}, {bidding_cpm})")
    #         self.commit()

    # def bidding_process(self):
    #     self.execute(f"CALL bidding_process()")
    #     self.commit()

    # def bidding_strategy(self, bid_floor):
    #     id_pirces = self.fetch_filtered_data(query=f"SELECT * FROM Id_Price WHERE `bidding_price`=(SELECT MAX(`bidding_price`) FROM Id_Price);")
    #     if id_pirces[0][1] < bid_floor:
    #         with open("history.txt", "a") as output:
    #             output.write(f"All bidding prices are lower than bid_floor!")
    #             return None
    #     else:
    #         with open("history.txt", "a") as output:
    #             output.write(f"Response to SSP with price:{id_pirces[0][1]} & creative_id:{id_pirces[0][0]}")
    #             return {"price":id_pirces[0][1], "creative_id":id_pirces[0][0]}

if __name__ == "__main__":
    sql = MySQL(db_settings)
    # sql.bidding_process()