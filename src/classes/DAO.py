import os
import pymongo
from src.classes.Player import Player


class DAO:
    """
    DAO is a class that allows to interact with a MongoDB database by using Player objects
    """

    def __init__(self):
        """
        __init__ is a method that initializes the DAO object
        """
        CONNECTION_STRING = os.getenv("BDD_STRING")
        self.client = pymongo.MongoClient(CONNECTION_STRING)
        db = self.client["profils"]
        collection = db["profils_collec"]
        self.db = collection

    def get_all(self) -> list[Player]:
        """
        get_all is a method that returns all the players in the database

        Returns
        -------
        list[Player]
            The list of all the players in the database
        """
        results = self.db.find()
        return results

    def find_by_name(self, name: str) -> Player:
        """
        find_by_name is a method that returns a player find by it's name

        Parameters
        ----------
        name : str
            The name of the player to find

        Returns
        -------
        Player
            The player found with the class Player
        """
        query = {"name": name}
        result = self.db.find_one(query)
        if result is not None:
            joueur = Player.from_dict(result)
            return joueur
        return None

    def insert(self, player: Player) -> bool:
        """
        insert is a method that inserts a player in the database

        Parameters
        ----------
        player : Player
            The player to insert in the database

        Returns
        -------
        bool
            True if the player has been inserted, False if the player already exists or if an error occured
        """
        if self.find_by_name(player.get_name()) is not None:
            return False
        self.db.insert_one(player.to_dict())
        return True

    def update(self, player: Player):
        """
        update is a method that updates a player in the database based on the class Player

        Parameters
        ----------
        player : Player
            The player to update in the database
        """
        obj = player.to_dict()
        query = {"name": obj["name"]}
        new_values = {"$set": {"wallet": obj["wallet"]}}
        self.db.update_one(query, new_values)

    def delete(self, player: Player):
        """
        delete is a method that deletes a player in the database based on the class Player

        Parameters
        ----------
        player : Player
            The player to delete in the database
        """
        query = {"name": player.get_name()}
        self.db.delete_one(query)

    def close(self):
        """
        close is a method that closes the connection to the database
        """
        self.client.close()
        print("Connection closed")

    def get_nb_documents(self) -> int:
        """
        get_nb_documents is a method that returns the number of documents in the database

        Returns
        -------
        int
            The number of documents in the database
        """
        return self.db.count_documents({})
