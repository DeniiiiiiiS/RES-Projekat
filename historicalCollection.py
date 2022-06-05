import receiverProperty

class HistoricalCollection:
    def  __init__(self):
        self.nizReceiverProperty = []

    def dodaj(self,a):
        self.nizReceiverProperty.append(a)
    
    def isprazni(self):
        self.nizReceiverProperty.clear()