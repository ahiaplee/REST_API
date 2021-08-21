""" ListFiles class for listing files endpoint
"""
from Common import *

class ListFiles(Resource):
    """ ListFiles class for listing files endpoint
    """
    def __GetFiles(self):
        """ Retrieves the list of files in the database and return it

        Returns:
            message : Message Object containing if the operation was successful
                      along with array of file data
        """

        #grab data from db
        conn = dbObject.GetConnection()
        cur = conn.cursor()
        
        try:
            cur.execute('SELECT * FROM files')
            res = cur.fetchall()

            if res is not None:

                files = []

                for record in res:

                    #break up the file name for information
                    infos = record[3].split('_')
                    filename = record[1] 
                    filedate = infos[1]
                    filetime = infos[2][:-4]

                    file_datetime = datetime.datetime.strptime(filedate + filetime, "%Y%m%d%H%M%S")
                    print("asd")
                    #add information to
                    files.append({
                        "filename": filename,
                        "upload_date": file_datetime.strftime("%d/%m/%Y %H:%M:%S"),
                        "filesize" : record[2],
                        "sensitivity_score" : record[4],
                        "last_updated" : record[5].strftime("%d/%m/%Y %H:%M:%S")
                    })

                return Message(True, "Files Retrieved", files)

        except (Exception, psycopg2.DatabaseError) as error:
                return Message(False, error)

    def post(self):
        """ POST request handler for ListFiles endpoint

        Request Parameters:
            token : JWT of the user

        Returns:
            message : Message Object containing if the operation was successful
        """
        parser = reqparse.RequestParser()
        parser.add_argument('token')
        args = parser.parse_args()

        check = CheckArgs(['token'], args)
        if check is not True:
            return check

        res = User.CheckToken(args['token'])

        if res == True:
            return self.__GetFiles()
        else:
            return Message(False, res)

if __name__ == '__main__':
    pass