from . import mongoClientLink

collection = mongoClientLink["trumo"]["users"]

class UsersStore():
    def upsert(id, data):
        filter_query = {"_id": id}
        update_data = {"$set": data} 
        result = collection.update_one(filter_query, update_data, upsert=True)

    def getAll():
        return collection.find()

    def delete(id):
        collection.delete_one({'_id': id})
