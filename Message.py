""" Helper function to construct message of object
"""
def Message(success, msg, data = None):
    return {
        "success" : success,
        "message" : str(msg),
        "data" : None if data is None else (data)
    }
