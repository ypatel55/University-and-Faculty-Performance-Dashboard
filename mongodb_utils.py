from pymongo import MongoClient
import pandas as pd

# Connect to MongoDB Database
def connect():
    host = 'localhost'
    port = 27017
    client = MongoClient(host, port)
    db = client["academicworld"]
    return db

db = connect()
publication = db["publications"]
faculty = db["faculty"]


# Returns faculty members associated with a given keyword
def get_fac_from_kw(uni, keyword):
    query = [
        {'$match': {'affiliation.name': uni, 'keywords.name': keyword}},
        {'$unwind': '$keywords'},
        {'$match': {'keywords.name': keyword}},
        {'$group': {
            '_id': '$name',
            'email': {'$first': '$email'},
            'position': {'$first': '$position'},
            'photoUrl': {'$first': '$photoUrl'}
        }}
    ]

    result = faculty.aggregate(query)
    facs = pd.DataFrame(list(result))
    
    return facs.to_dict('records')

# Returns publications given a university and faculty member
def get_pubs_from_fac(uni, faculty_name):
    query = [
        {'$match': {'name': faculty_name, 'affiliation.name': uni}},
        {'$lookup': {
            'from': 'publications',
            'localField': 'publications',
            'foreignField': 'id',
            'as': 'publications'}},
        {'$unwind': '$publications'},
        {'$project': {
            '_id': 0,
            'Publication ID': '$publications.id',
            'Title': '$publications.title',
            'Number of Citations': '$publications.numCitations',
            'Year': '$publications.year'}}, {'$sort': {'Year': -1}}
            ]

    result = faculty.aggregate(query)
    return list(result)
