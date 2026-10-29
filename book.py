from fastapi import FastAPI, Body
from pydantic import BaseModel
from starlette import status

app = FastAPI()

user = [
  {
    "id": 1,
    "name": "Leanne Graham",
    "username": "Bret",
    "email": "Sincere@april.biz",
    "address": {
      "street": "Kulas Light",
      "suite": "Apt. 556",
      "city": "Gwenborough",
      "zipcode": "92998-3874",
      "geo": {
        "lat": "-37.3159",
        "lng": "81.1496"
      }
    },
    "phone": "1-770-736-8031 x56442",
    "website": "hildegard.org",
    "company": {
      "name": "Romaguera-Crona",
      "catchPhrase": "Multi-layered client-server neural-net",
      "bs": "harness real-time e-markets"
    }
  },
  {
    "id": 2,
    "name": "Ervin Howell",
    "username": "Antonette",
    "email": "Shanna@melissa.tv",
    "address": {
      "street": "Victor Plains",
      "suite": "Suite 879",
      "city": "Gwenborough",
      "zipcode": "90566-7771",
      "geo": {
        "lat": "-43.9509",
        "lng": "-34.4618"
      }
    },
    "phone": "010-692-6593 x09125",
    "website": "anastasia.net",
    "company": {
      "name": "Deckow-Crist",
      "catchPhrase": "Proactive didactic contingency",
      "bs": "synergize scalable supply-chains"
    }
  },
  {
    "id": 3,
    "name": "Clementine Bauch",
    "username": "Samantha",
    "email": "Nathan@yesenia.net",
    "address": {
      "street": "Douglas Extension",
      "suite": "Suite 847",
      "city": "McKenziehaven",
      "zipcode": "59590-4157",
      "geo": {
        "lat": "-68.6102",
        "lng": "-47.0653"
      }
    },
    "phone": "1-463-123-4447",
    "website": "ramiro.info",
    "company": {
      "name": "Romaguera-Jacobson",
      "catchPhrase": "Face to face bifurcated interface",
      "bs": "e-enable strategic applications"
    }
  },
  {
    "id": 4,
    "name": "Patricia Lebsack",
    "username": "Karianne",
    "email": "Julianne.OConner@kory.org",
    "address": {
      "street": "Hoeger Mall",
      "suite": "Apt. 692",
      "city": "South Elvis",
      "zipcode": "53919-4257",
      "geo": {
        "lat": "29.4572",
        "lng": "-164.2990"
      }
    },
    "phone": "493-170-9623 x156",
    "website": "kale.biz",
    "company": {
      "name": "Robel-Corkery",
      "catchPhrase": "Multi-tiered zero tolerance productivity",
      "bs": "transition cutting-edge web services"
    }
  },
  {
    "id": 5,
    "name": "Chelsey Dietrich",
    "username": "Kamren",
    "email": "Lucio_Hettinger@annie.ca",
    "address": {
      "street": "Skiles Walks",
      "suite": "Suite 351",
      "city": "Gwenborough",
      "zipcode": "33263",
      "geo": {
        "lat": "-31.8129",
        "lng": "62.5342"
      }
    },
    "phone": "(254)954-1289",
    "website": "demarco.info",
    "company": {
      "name": "Keebler LLC",
      "catchPhrase": "User-centric fault-tolerant solution",
      "bs": "revolutionize end-to-end systems"
    }
  },
]

#initialHealthcheck
@app.get("/", status_code=status.HTTP_200_OK)
def health_check():
    return "Health is okay!"
#basic get api
@app.get("/getuser", status_code=status.HTTP_200_OK)
async def user_list():
    return user

# getapi with param input
@app.get("/userparam/{param}")
async def check_user(param):
    return {"param": param}

#getexact usernamefrom list
@app.get("/user/{username}")
async def find_username(username: str):
    for userslist in user:
        if userslist.get('username').casefold() == username.casefold():
            return userslist

# searchusingqyeryparam
@app.get("/user/")
async def query_user(city: str):
    city_list = []
    for citys in user:
        if citys.get('address').get('city').casefold() == city.casefold():
            city_list.append(citys)
    return city_list

# searchusingqueryparam & param

@app.get("/user/{name}/")
def searchExactPerson(name: str, city:str):
    userupdate = []
    for userdata in user:
        if userdata.get('name').casefold() == name.casefold():
            if userdata.get('address').get('city').casefold() == city.casefold():
                userupdate.append(userdata)
    return userupdate
                
#create user
@app.post("/user/createuser")
def create_user(newuser = Body()):
    user.append(newuser)

#updateUser
@app.put("/user/update_user")
def update_user(updateuser = Body()):
    for i in range(len(user)):
        if user[i].get('name').casefold() == updateuser.get('name').casefold():
            user[i] = updateuser
            

#deleteBook
@app.delete("/user/delete/")
def delete_user(id:int):
    for i in range(len(user)):
        if user[i].get('id') == id:
            return user.pop(i)