import os
import pymongo
from src.classes.Player import Player


class DAO:

    def __init__(self):
        CONNECTION_STRING=os.getenv('BDD_STRING')
        self.client = pymongo.MongoClient(CONNECTION_STRING)
        db = self.client['profils']
        collection = db['profils_collec']
        self.db = collection

    def get_all(self):
        results = self.db.find()
        return results
        
    def find_by_name(self, name):
        query = {"name": name}
        result = self.db.find_one(query)
        if result is not None:
            joueur = Player.from_dict(result)
            return joueur
        return None
    
    def insert(self, player):
        # Impossibilité de faire un insert si le joueur existe déjà
        if self.find_by_name(player.get_name()) is not None:
            return False
        self.db.insert_one(player.to_dict())

    def update(self, player):
        obj = player.to_dict()
        query = {"name": obj["name"]}
        new_values = {"$set": {"wallet": obj["wallet"]}}
        self.db.update_one(query, new_values)

    def delete(self, player):
        query = {"name": player.get_name()}
        self.db.delete_one(query)

    def close(self):
        self.client.close()
        print("Connection closed")

    def get_nb_documents(self):
        return self.db.count_documents({})