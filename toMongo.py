'''
For each line of parsed WordNet files, send it to MongoDB

Lucas Zanella, 13/02/2017
'''

import wordnetToAnything as WN
from pymongo import MongoClient

client = MongoClient()
databaseName = 'wordnet'

def toMongo(line, args):
    fileName = args[0]
    #We pop the counters as we don't need them in json
    if 'index' in fileName: #if it's an index file
        line.pop('p_cnt', None)
        line.pop('synset_cnt', None)
        line.pop('sense_cnt', None)
        line.pop('tagsense_cnt', None)
    client[databaseName][replacePointWithUnderscore(args[0])].insert_one(line)

def replacePointWithUnderscore(string):
    return string.replace('.','_')


print('working...\n')
#erases collection in case you have written something there before
fileName = 'index.verb'
client[databaseName].drop_collection(replacePointWithUnderscore(fileName))
WN.forEachLineOfFileDo(fileName, WN.CallbackWrapper(toMongo, fileName))
