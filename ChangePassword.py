""" ChangePassword Class for ChangePassword end point
"""
from Common import *


class ChangePassword(Resource):

    def post(self):
        """ POST request handler for ChangePassword endpoint

        Request Parameters:
            username : username of client
            old_password : current password of client
            new_password : new password of client

        Returns:
            message : Message Object containing if the operation was successful
        """

        #grab parameters
        parser = reqparse.RequestParser()
        parser.add_argument('username')
        parser.add_argument('old_password')
        parser.add_argument('new_password')
        args = parser.parse_args()

        #check for missing args
        check = CheckArgs(['username', 'old_password', 'new_password'], args)
        if check is not True:
            return check

        return User.ChangePassword(dbObject, args['username'], args['old_password'], args['new_password'])