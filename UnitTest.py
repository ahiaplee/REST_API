import requests
import sys
import datetime

def UnitTest(host):

    #Register a new user
    username = "new_user_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    password = "password1234"
    new_password = "password1234_new"

    print("Register a new user")
    res = requests.post(host + 'Register', {
        "username" : username,
        "password" : password
    })

    print(res.json())

    #Register a dupliate user
    print("Register a dupliate user")
    res = requests.post(host + 'Register', {
        "username" : username,
        "password" : password
    })

    print(res.json())

    #login
    print("Login with wrong password")
    res = requests.post(host + 'Login', {
        "username" : username,
        "password" : "password12345"
    })

    print(res.json())

    print("Login with correct password")
    res = requests.post(host + 'Login', {
        "username" : username,
        "password" : password
    })

    data = res.json()
    print(data)

    token = data['data']['token']

    #Test Upload File

    print("Uploading non text file")
    res = requests.post(host + 'FileUpload', 
                        {"token" : token }, 
                        files= {'file': open("app.ini", 'rb')}
                        )
    print(res.json())

    print("Uploading text file")
    res = requests.post(host + 'FileUpload', 
                            {"token" : token }, 
                            files= {'file': open("Test.txt", 'rb')}
                            )
    print(res.json())
    

    #test list file
    print("Test list files")
    res = requests.post(host + 'ListFiles', {"token" : token})
    data = res.json()
    print(data)
    for filedata in data['data']:
        print(filedata)


    print("request with invalid token")
    res = requests.post(host + 'FileUpload', 
                            {"token" : "asdad" }, 
                            files= {'file': open("Test.txt", 'rb')}
                            )
    print(res.json())
    res = requests.post(host + 'ListFiles', {"token" : "asdad"})
    print(res.json())


    print("Change password with wrong password")
    res = requests.post(host + 'ChangePassword', {
        "username" : username,
        "old_password" : "password_wrong",
        "new_password" : new_password
    })
    print(res.json())

    print("Change password with correct password")
    res = requests.post(host + 'ChangePassword', {
        "username" : username,
        "old_password" : password,
        "new_password" : new_password
    })
    print(res.json())

    print("Login with new password")
    res = requests.post(host + 'Login', {
        "username" : username,
        "password" : new_password
    })

    data = res.json()
    print(data)

if __name__ == '__main__':
    n = len(sys.argv)
    if(n < 2):
        pass
    else:
        UnitTest(sys.argv[1])
    pass