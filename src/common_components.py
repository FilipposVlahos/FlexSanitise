class DocumentRetrieval:
    fileLocation: str

    def __init__(self):
        self.fileLocation = "data_set/Lease.txt"

    def get_document(self):
        file = open(self.fileLocation, "r")
        return file.read()
