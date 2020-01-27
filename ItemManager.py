import datetime
import json
import os


def getTimestamp(module):
    return '[' + str(datetime.datetime.now()) + '] ' + module + ': '
class ItemManager:
    directory = ''
    # default constructor
    def __init__(self, directory):
        print(getTimestamp('ItemManager')+'ItemManger initialized successfully!')
        self.directory = directory
    # a method for printing data members
    def fileExists(self, productId):
        fileLoc = self.directory + '/'+productId+'.json'
        try:
            f = open(fileLoc)
            return True
        except IOError:
            return False
    def getProductSizes(self,productId):
        fileLoc = self.directory + '/' + productId + '.json'
        exists = self.fileExists(productId)
        if(exists):
            with open(fileLoc) as f:
                d = json.load(f)
                sizes = d['productSizes']
                return sizes
    def createProduct(self,productId, productSizes):
        fileLoc = self.directory + '/' + productId + '.json'
        data = {}
        data['productSizes'] = productSizes
        with open(fileLoc, 'w') as outfile:
            json.dump(data, outfile)
        print(getTimestamp('ItemManager'+'Product with id: '+productId + ' created!'))
    def setSizes(self, productId, productSizes):
        fileLoc = self.directory + '/' + productId + '.json'
        exists = self.fileExists(productId)
        if(exists):
            os.remove(fileLoc)
        self.createProduct(productId,productSizes)


