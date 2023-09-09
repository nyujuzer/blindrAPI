import requests

class NativeNotifyAPI:
    '''
    '''
    def __init__(self, appid, apptoken) -> None:
        self.app_id = appid
        self.app_token = apptoken
    def send_notificationToSpecUser(self, sub_id, title, message):
        url = "https://app.nativenotify.com/api/indie/notification"
        payload = {
            "subID": sub_id,
            "appId": self.app_id,
            "appToken": self.app_token,
            "title": title,
            "message": message
        }
        print(sub_id)
        response = requests.post(url, json=payload)
        print(response.text)
        return response
    
    def registerMasterFollowNotif(self, dom):
        pass