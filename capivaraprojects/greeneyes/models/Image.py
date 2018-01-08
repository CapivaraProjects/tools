from capivaraprojects.greeneyes.models.Disease import Disease
class Image:
    def __init__(self, id=0, disease=Disease(), url="", description="", source=""):
        self.id = id
        self.disease = disease
        self.url = url
        self.description = description
        self.source = source
