import requests
from random import randint as rnd
def makeGender():
    rand  = rnd(0, 2)
    if rand == 0:return "male"
    elif rand == 1:return "female"
    else: return "enby"
def makepref():
    rand  = rnd(0, 2)
    if rand == 0:return "male"
    elif rand == 1:return "female"
    else: return "any"
def multi_test():
    counter = 0
    while True:
        data = {
        "email": f'test{counter}@email.com',
        "password": 'TestPassword1',
        "conf": 'TestPassword1',
        "name": f'Test {counter}',
        "gender": makeGender(),
        "preferences":makepref(),
        "hobbies": list(set([rnd(1, 12) for i in range(0, rnd(1, 12))])), 
        "age": "2003/03/03"
    }
        print(data["hobbies"])
        response = requests.post(url= "http://192.168.1.9:8000/register/", json=(data))
        print(response.text)
        counter+=1
        if (response.json()["success"] == False):
            input("check")
        if counter == 100:
            return "done" 
#multi_test()
def test_register():
    data = {
    "email": f'test@email.com',
    "password": 'Password1',
    "conf": 'Password1',
    "name": f'TEST_TEST',
    "gender": 'male',
    "preferences":'female',
    "hobbies": list(set([rnd(1, 12) for i in range(0, rnd(1, 12))])), 
    "age": "2003/03/03"
    }
    print(data["hobbies"])
    response = requests.post(url= "http://127.0.0.1:8000/register/", json=(data))
    print(response.text)
    if (response.json()["success"] == False):
        input("check")
    return("done")
def test_login():
     response = requests.get("http://127.0.0.1:8000/login/test3@email.com+TestPassword1")
     print(response.text)
def test_full(*fn):
        for i in fn:
             i()


test_full(test_login)