import os
import pymongo
import src.Player as Player


class DAO:

    def __init__(self):
        CONNECTION_STRING=os.getenv('BDD_STRING')
        client = pymongo.MongoClient(CONNECTION_STRING)
        db = client['profils']
        collection = db['profils_collec']
        self.db = collection

    def get_all(self):
        results = self.db.find()
        return results
        
    def find_by_name(self, name):
        query = {"name": name}
        result = self.db.find_one(query)
        if result is not None:
            return Player(result["name"], result["wallet"], result["games_played"], result["games_won"], result["nb_bankrupt"])
        return None
    
    def insert(self, player):
        # Impossibilité de faire un insert si le joueur existe déjà
        if self.find_by_name(player.get_name()) is not None:
            return False
        self.db.insert_one(player.to_dict())

    def update(self, player):
        obj = player.to_dict()
        query = {"name": player.get_name()}
        new_values = {"$set": obj}
        return self.db.update(new_values, query)

    def delete(self, player):
        query = {"name": player.get_name()}
        self.db.delete_one(query)

    def get_nb_documents(self):
        return self.db.count_documents({})