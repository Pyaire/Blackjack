#%% Make env
import os
import pymongo
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING=os.getenv('BDD_STRING')




#%% Connect to the MongoDB server
client = pymongo.MongoClient(CONNECTION_STRING)

# Access a specific database
db = client['profils']

# Access a specific collection
collection = db['profils_collec']




#%% Find all documents
results = collection.find()
for result in results:
    print(result)



#%% Get the number of documents
nb_documents = collection.count_documents({})
print(nb_documents)



#%% Find a document
query = {"name": "aynost"}
result = collection.find_one(query)
print(result)






# %% Insert a document
doc = {"name": "Justin",
        "wallet": 20000,
        "games_played": 0,
        "games_won": 0,
        "nb_bankrupt": 0}
collection.insert_one(doc)







# %% Modify a document
query = {"name": "Justin"}
new_values = {"$set": {"wallet": 50}}
collection.update_one(query, new_values)






# %% Delete a document
query = {"name": "pyaire"}
collection.delete_one(query)








# %% Delete all documents
query = {}
collection.delete_many(query)


#%%
#create a player from the Player class  
from src.classes.Player import Player

player = Player("Justin", 20000, 0, 0, 0)






# %% Use DAO
from classes.DAO import DAO
from src.classes.Player import Player

pyaire = Player("pyaire", 50, 0, 0, 0)
bdd = DAO()
bdd.insert(pyaire)
# %%
