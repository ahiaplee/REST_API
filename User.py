""" Helper class to Authenticate, Create, Check if user exist, Change Password
"""
import datetime
import jwt
import psycopg2
from configparser import ConfigParser
from werkzeug.security import generate_password_hash, check_password_hash
from Message import Message
import base64

class User():
    """ Helper class to Authenticate, Create, Check if user exist, Change Password

    Attributes:
        ___secret : static vairable containg api secret key for encode and decoding JWT 

    """

    __secret = None

    @staticmethod
    def Init():
        """ used to read config file and set api secret key
        """
        if User.__secret is None:
            print("Reading config")
            User.__secret = User.__ReadConfig()


    @staticmethod 
    def __ReadConfig(filename='app.ini', section='app_config'):
        """ used to read config file and find the api secret key

        Args:
            filename : name of the config file
            section : section the file to look for
        
        Returns:
            api secret key if found, None if not found
        """
        parser = ConfigParser()
        parser.read(filename)

        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                if param[0] == "app_secret":
                    return param[1]

        else:
            return None



    @staticmethod
    def CheckExist(dbObject, username):
        """ Checks against the DB if user exist
        
        Args:
            dbObject : DB connection object to use
            username : username to find

        Returns:
            boolean if user is found
        """
        conn = dbObject.GetConnection()
        cur = conn.cursor()
        cur.execute('SELECT username FROM users WHERE username = (%s)', (username,))
        res = cur.fetchone()
        return res is not None


    @staticmethod
    def Auth(dbObject, username, password):
        """ Attempts to Authenticate a user using username and password,
            returns a token if succesful

        Args:
            dbObject : DB connection object to use
            username : username of client
            password : password of client

        Returns:
             message : Message Object containing if the operation was successful
                      and token if authentication was successful
        """
        conn = dbObject.GetConnection()
        cur = conn.cursor()
        try:
            cur.execute('SELECT * FROM users WHERE username = (%s)', (username,))
            res = cur.fetchone()

            if res is not None:
                if(check_password_hash(res[1], password)):

                    #generate JWT if password hash matches
                    token = User.__GenerateJWT(username)

                    return Message(True, "Login Success", { 
                        "token" : token
                    })
                else:
                    return Message(False, "Invalid Credentials")
            else:
                return Message(False, "Invalid Credentials")

        except (Exception, psycopg2.DatabaseError) as error:
                return Message(False, error)


    @staticmethod 
    def ChangePassword(dbObject, username, old_password, new_password):
        """ Change password of current user, updates password if password hash matches
            the old password
        
        Args:
            dbObject : DB connection object to use
            username : username of client
            old_password : old password of client
            new_password : new password of client

        Returns:
            message : Message Object containing if the operation was successful
        """
        conn = dbObject.GetConnection()
        cur = conn.cursor()
        try:
            cur.execute('SELECT * FROM users WHERE username = (%s)', (username,))
            res = cur.fetchone()

            if res is not None:

                #check if old password hash matches the one in db
                if(check_password_hash(res[1], old_password)):
                    pass_hash = generate_password_hash(new_password)
                    
                    #attempt to update db with new password hash
                    try:
                        cur.execute('UPDATE users SET password = (%s) WHERE username = (%s)', (pass_hash, username))
                        if res is not None:
                            conn.commit()
                            return Message(True, "User password changed")
                        else:
                            raise Exception("Updating of password hash failed")
                    except (Exception, psycopg2.DatabaseError) as error:
                        conn.rollback()
                        return Message(False, error)
                    
                else:
                    return Message(False, "Invalid Credentials")
            else:
                return Message(False, "Invalid Credentials")

        except (Exception, psycopg2.DatabaseError) as error:
                return Message(False, error)

    @staticmethod
    def __GenerateJWT(username):
        """ Attempts generate a JWT for the current user

        Args:
            username : username of client

        Returns:
            JWT token is successful, else exception object
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=5),
                'iat': datetime.datetime.utcnow(),
                'sub': username
            }
            return jwt.encode(
                payload,
                User.__secret,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod 
    def __DecodeToken(token):
        """ Attempts to decode a JWT token

        Args:
            token : JWT token of client

        Returns:
            True if token is valid, else a message of the error
        """
        try:
            payload = jwt.decode(token,User.__secret , algorithms="HS256")
            #print(payload)
            return True
        except jwt.ExpiredSignatureError:
            return 'Token expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    @staticmethod
    def CheckToken(token):
        """ Helper function to check token
        Args:
            token : JWT token of client

        Returns:
            True if token is valid, else a message of the error
        """
        res = User.__DecodeToken(token)
        return res
        
User.Init()

if __name__ == '__main__':
    pass