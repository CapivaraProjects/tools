class Plant:
    def __init__(self, id, scientificName, commonName, diseases=list()):
        self.id = id
        self.scientificName = scientificName
        self.commonName = commonName
        self.diseases = diseases


