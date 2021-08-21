""" Database connection class definition used to interact with database
"""
from configparser import ConfigParser
import psycopg2

class DatabaseConnection:
    """ Database connection class

    Read the ini file given and create a database connection

    Attributes:
        connected : boolean whether object is connected to a DB
        __config : dictionary of configuration values 

    """
    def __init__(self, filename='app.ini', section='postgresql'):
        """ Inits the object and connects to the database given in the ini file

        Args:
            filename: name of the ini file
            section : section of the file where configuration is stored
        """

        #set default values and read config file
        self.connected = False
        self.__config = self.__readConfig(filename, section)

        # attempt to connect if config reading is successful
        if self.__config is not None:
            try:
                print('Connecting to the PostgreSQL database...')
                self.__conn = psycopg2.connect(**self.__config)
                
                if self.__conn is not None:
                    print("DB connect successful, testing connection")
                    self.TestConnection()
                    connected = True
                else:
                    print("Connection failed with no exception thrown")

            except (Exception, psycopg2.DatabaseError) as error:
                print(error)

    def __del__(self):
        """ closes db connection on destruction
        """
        if self.connected:
            self.__conn.close()

    def GetConnection(self):
        """ Getting for db connection object

        Returns:
            self.__conn: db connection object
        """
        return self.__conn

    def TestConnection(self):
        """ Function to test current db connection
        """
        cur = self.__conn.cursor()
        
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        db_version = cur.fetchone()
        print(db_version)

    def __readConfig(self, filename, section):
        """ Function to read config file construct dictionary

        Args:
            filename: name of the ini file
            section : section of the file where configuration is stored

        Returns:
            db : dictionary of values read from the config file

        """
        parser = ConfigParser()
        parser.read(filename)
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))

        print(db)
        return db

if __name__ == '__main__':
    pass