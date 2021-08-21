""" Login Class for Login end point
"""
from Common import *


class Login(Resource):
    """ Login Class for Login end point
    """
    def post(self):
        """ POST request handler for FileUpload endpoint

        Request Parameters:
            username : username of client
            password : password of client

        Returns:
            message : Message Object containing if the operation was successful
                      and token if login was successful
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

        #call user helper class to verify

        

        return User.Auth(dbObject, args['username'], args['password'])

if __name__ == '__main__':
    pass