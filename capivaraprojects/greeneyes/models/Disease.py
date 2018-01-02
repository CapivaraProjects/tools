class Disease:
    def __init__(self, id=0, plant=Plant(), scientificName="", commonName=""):
        self.id = id
        self.plant = plant
        self.scientificName = scientificName
        self.commonName = commonName
