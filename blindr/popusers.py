import requests
import json

data = {
  "display_models": [
    {
      "name": "John's Display",
      "gender": 1,
      "preferences": 2,
      "hobbies": [1, 2],
      "age": "1990-01-01",
      "email": "john@example.com",
      "password": "johnpassword"
    },
    {
      "name": "Jane's Display",
      "gender": 2,
      "preferences": 1,
      "hobbies": [2, 3, 4],
      "age": "1995-05-15",
      "email": "jane@example.com",
      "password": "janepassword"
    },
    {
      "name": "Mike's Display",
      "gender": 1,
      "preferences": 3,
      "hobbies": [1, 3],
      "age": "1988-09-20",
      "email": "mike@example.com",
      "password": "mikepassword"
    },
    {
      "name": "Emily's Display",
      "gender": 2,
      "preferences": 2,
      "hobbies": [4, 5],
      "age": "1992-07-12",
      "email": "emily@example.com",
      "password": "emilypassword"
    },
    {
      "name": "David's Display",
      "gender": 1,
      "preferences": 1,
      "hobbies": [2],
      "age": "1994-03-04",
      "email": "david@example.com",
      "password": "davidpassword"
    }
  ]
}


for i in data['display_models']:
    result = requests.post('http://192.168.43.88:8000/register/',json=i)