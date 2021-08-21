<h1>SEIS – TEST REST API</h1>

Developed with Python 3.6.9 using WSL for Windows 10
Native Windows not support as Celery does not have support for Windows since 4.0

**Installation:**

```shell
pip install -r requirements.txt
```

A copy of redis-stable is included but you can delete it and redownload it by running run-redis.sh in a terminal window

**To  run:**

 - **3** Terminal windows are required
 - Start redis with run-redis.sh
 - Start API server with run-server.sh
 - Start Celery worker with run-celery.sh

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



