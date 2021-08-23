
<h1>TEST REST API</h1>

* Docker is required
* WSL is required if running on Windows

Frameworks:
* Flask
* Celery
* Postgres

**Installation:**
* Go to the root directory of project and run
```shell
docker-compose build
```
or
```shell
docker-compose -f docker-compose.yml build
```

**Configuring**
Take note that in  ```app.ini``` few properties can be changed
* app_secret : change this to your liking or generate in app (Line 27, User.py)
* Please **do not modify** the postgresql section of the ini file, if you do please remember to change the corresponding variables in the docker-compose.yml 
```ini
[app_config]
app_secret=MYRESTAPI1234
```
Update the follow under "db" of docker-compose.yml if you decide to change the postres section
```yml
POSTGRES_USER: postgres
POSTGRES_PASSWORD: postgres
POSTGRES_DB: postgres
```

**To  run:**
* Make sure you built the docker image in the installation step
* Go to the root directory of project and run
```shell
docker-compose up -d
```
* App should now run in http://localhost:5000/

<h2>API</h2>

All requests only support POST as the JWT in this context is not single use.

All requests return a Message Object like this example below:
```json
{
    "success": true,
    "message": "User account created",
    "data": null
}
```

**Endpoints**
 * /**Register** : used for user registration
	 * username : username to be registered
	 * password : password for the user to be registered (hash will be stored)
* /**Login** : used to obtain JWT with given credentials
	 * username : username of client
	 * password : password of client
	 * returns : JWT in the "data" property if login is succesful
* /**FileUpload** : used to obtain JWT with given credentials
	 * token: JWT of the client
	 * file: file to be uploaded as multipart form datal
* /**ListFiles** : used to obtain JWT with given credentials
	 * token: JWT of the clientt
	 * returns : array of files in the "data" property if succesful
Example:
```json
{
    "success": true,
    "message": "Files Retrieved",
    "data": [
        {
            "filename": "Test1.txt",
            "upload_date": "21/08/2021 21:42:16",
            "filesize": 115,
            "sensitivity_score": 20,
            "last_updated": "21/08/2021 21:41:28"
        }
    ]
}
```
* /**ChangePassword** : used to obtain JWT with given credentials
	 * username : username of client
	 * old_password: current password of client
	 * new_password: new password of client


<h2>Notes: </h2>

* Uploaded files are saved with ```<original_name>_<%Y%m%d_%H%M%S>.txt``` e.g ``` Test1_20210821_214216.txt```to allow for same file names without overwriting
* Sensitivity score task is triggered every time a new file is uploaded, periodic update can be activated by uncommenting line 15-22 in CeleryTasks.py
* Simple units tests can be conducted by running the app, opening another terminal window and running ```python3 UnitTest.py hostname:port``` e.g ```python3 UnitTest.py http://127.0.0.1:5000/```

