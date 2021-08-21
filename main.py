from Common import *

#import resouces
from Login import Login
from Registration import Registration
from FileUpload import FileUpload
from ListFiles import ListFiles
from ChangePassword import ChangePassword
from CeleryTasks import *

def run():
    """
    main function of the REST API

    Args:
    Returns:
    """

    #add resources
    api.add_resource(Registration, "/Register")
    api.add_resource(Login, "/Login")
    api.add_resource(FileUpload, "/FileUpload")
    api.add_resource(ListFiles, "/ListFiles")
    api.add_resource(ChangePassword, "/ChangePassword")
    app.run(debug=True)

if __name__ == "__main__":
	run()