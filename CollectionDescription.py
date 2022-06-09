import historicalCollection

class CollectionDescription:
    def __init__(self, id, data_set):
        self.id = id
        self.data_set = data_set
        self.historical_collection = historicalCollection.HistoricalCollection()

    def dodaj_u_HistoricalCollection(self, cd):
        self.historical_collection.dodaj(cd)

    def  isprazniHistoricalCollection(self):
        self.historical_collection.isprazni()

    def getId(self):
        return self.id

    def getDataset(self):
        return self.data_set

    def getHistoricalCollection(self):
        return self.historical_collection
        


