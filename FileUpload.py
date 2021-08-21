""" FileUpload class for file upload end point
"""
from Common import *
from werkzeug.datastructures import FileStorage
import re
import os
from CeleryTasks import Update_Scores



class FileUpload(Resource):
    """ FileUpload class for file upload end point
    """

    def __UpdateDB(self, filename, save_path, filesize):
        """ Updates database with the file information provided
        Args:
            filename : name of file
            save_path : path where the file is saved on the server
            filesize : size of the file in bytes

        Returns:
            message : Message Object containing if the operation was successful
        """
        conn = dbObject.GetConnection()
        cur = conn.cursor()
        try:
            res = cur.execute("INSERT INTO files (filename, filepath, filesize) VALUES(%s, %s, %s)", 
            (filename, save_path, filesize))
            if res is None:
                conn.commit()
                return Message(True, "File Successfully uploaded", {
                    "Size" : filesize
                })
            else:
                raise Exception("Insert user data to database failed") 
        except (Exception, psycopg2.DatabaseError) as error:
            conn.rollback()
            return Message(False, error)

    def post(self):
        """ POST request handler for FileUpload endpoint

        Request Parameters:
            token : JWT of the user
            file : file uploaded from client

        Returns:
            message : Message Object containing if the operation was successful
        """

        #parse parameters
        parser = reqparse.RequestParser()
        parser.add_argument('token')
        parser.add_argument('file', type=FileStorage, location='files')
        args = parser.parse_args()

        #check for missing parameters
        check = CheckArgs(['token', 'file'], args)
        if check is not True:
            return check

        #verify token
        res = User.CheckToken(args['token'])

        if res == True:

            #check if file is .txt
            upload_file = args.get("file")
            is_text = bool(re.match("^.*\.(txt)$", upload_file.filename))

            if not is_text:
                return Message(False, "Only text files supported")

            #generate the filename to be saved
            save_filename = upload_file.filename[:-4] + '_' + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + '.txt'

            print('Saving %s' % save_filename)

            #save file and get data for db insertion
            save_path = os.path.join(UPLOAD_DIR, save_filename)
            upload_file.save(save_path)
            filesize = os.stat(save_path).st_size

            #insert to db
            Update_Scores.apply_async(args=[], countdown = 5)

            return self.__UpdateDB(upload_file.filename, save_path, filesize)
        else:
            return Message(False, res)

if __name__ == '__main__':
    pass


