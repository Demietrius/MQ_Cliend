import json
import os
from datetime import datetime, timedelta, timezone

import cglogging as cgl
import psycopg2
from secret_manager import secret_manager

logger_Class = cgl.cglogging()
logger = logger_Class.setup_logging()


# noinspection SqlNoDataSourceInspection
class DatabaseConnector:

    def __init__(self):
        self.database_key = os.environ.get('CAG_DATABASE_CREDENTIALS')
        self.region = os.environ.get('CAG_region')
        self.host = ""
        self.user = ""
        self.password = ""
        self.database = "CharterAndGO"
        self.port = ""
        self.databaseConnection = None
        self.databaseCursor = None
        self.engine = ""

    def connect_to_database(self):
        return_code, return_type, secret = secret_manager.get_secrets(self.database_key)
        if return_code != 0:
            return return_code, " ", " "

        logger.debug("inside database connector")
        if 'username' in secret['SecretString']:
            extracted_secret = json.loads(secret['SecretString'])
            self.user = extracted_secret['username']
            self.password = extracted_secret['password']
            self.host = extracted_secret["host"]
            self.port = extracted_secret['port']
            self.engine = extracted_secret['engine']
            self.database = extracted_secret["dbname"]

        try:
            self.databaseConnection = psycopg2.connect(user=self.user, password=self.password, database=self.database,
                                                       host=self.host, port=self.port)
            return 0, " "
        except (Exception, psycopg2.Error) as error:
            self.databaseConnection.rollback()
            print(40, "sql failed".format(error))
            return 40, " "

    # ---------------------crew--------------------------------------

    def create(self):
        pass

    def read(self):
        user = None
        try:
            sql = """
             SELECT
               FROM public.name
                WHERE
            """

            cursor = self.databaseConnection.cursor()
            cursor.execute(sql, )
            result = cursor.fetchall()
            for value in result:
                user = self.get_resposne(result)
            if user is not None:
                return 0, user
            else:
                self.databaseConnection.rollback()
                return 41, None

        except (Exception, psycopg2.Error) as error:
            self.databaseConnection.rollback()
            logger.debug(error)
            return 42, "FATAL"

    def update(self, updated, userid):
        new_user = None
        today = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f%z")
        updated["lastUpdatedDate"] = today
        try:
            sql = """
                    UPDATE public.name
                    SET
                    WHERE
                    RETURNING
                              """

            cursor = self.databaseConnection.cursor()
            cursor.execute(sql, )
            result = cursor.fetchall()
            for value in result:
                new_user = self.get_response(value)
            if new_user is not None:
                self.databaseConnection.commit()
                return 0, new_user
            else:
                self.databaseConnection.rollback()
            return 43, None

        except (Exception, psycopg2.Error) as error:
            self.databaseConnection.rollback()
            logger.debug(error)
            return 43, "FATAL", {}

    def delete(self):
        pass

    # --------------------helper functions-----------------------------------

    def get_response(self, result):
        return {
            "lastUpdatedBy": result[7] if result[7] is not None else 0,
        }
