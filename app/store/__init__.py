from pymongo import MongoClient
import certifi

uri = "mongodb+srv://trumo_backend:sze2kKZ7eHHoikZI@cluster0.eua1zbp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

mongoClientLink = MongoClient(uri, tlsCAFile=certifi.where())
