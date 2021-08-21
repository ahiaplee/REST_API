""" Registration Class for Registration end point
"""
from Common import *

class Registration(Resource):
    """ Registration Class for Registration end point
    """
    def __RegisterUser(self, username, password):
        """ Check if username already exist and inserts new data if not

        Args:
            username : username to be registered
            password : password of the account to be hashed

        Returns:
            message : Message Object containing if the operation was successful
        """

        #if user already exist return message
        if(User.CheckExist(dbObject, username)):
            return Message(False, "Username already exist")

        else:
            #hash the password and save the record
            pass_hash = generate_password_hash(password)
            conn = dbObject.GetConnection()
            cur = conn.cursor()
            try:
                res = cur.execute("INSERT INTO users (username, password) VALUES(%s, %s)", (username, pass_hash))
                if res is None:
                    conn.commit()
                    return Message(True, "User account created")
                else:
                    raise Exception("Insert user data to database failed") 
            except (Exception, psycopg2.DatabaseError) as error:
                conn.rollback()
                return Message(False, error)
            

    def post(self):
        """ POST request handler for FileUpload endpoint

        Request Parameters:
            username : username of client
            password : password of client

        Returns:
            message : Message Object containing if the operation was successful
        """

        #grab parameters
        parser = reqparse.RequestParser()
        parser.add_argument('username')
        parser.add_argument('password')
        args = parser.parse_args()

        #check for missing args
        check = CheckArgs(['username', 'password'], args)
        if check is not True:
            return check

        #insert to db
        return self.__RegisterUser(args['username'], args['password'])

if __name__ == '__main__':
    pass