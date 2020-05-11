class Database:
    def __init__(self):
        self.url_mappings = {}
        self.id = 0

    def delete_mappings(self):
        """Deletes all mappings stored in the memory"""
        self.url_mappings.clear()
        self.id = 0

    def delete_mapping(self, idx):
        """Deletes single mapping identified by the ID (parameter)"""
        self.url_mappings.pop(idx)

    def add_mapping(self, url):
        """Adds a new URL to the data set, assigning first consecutive unassigned integer as the ID. If URL already
        exists, throws Exception.
        Function returns assigned ID and increments the counter used to track assigned IDs"""
        if url in self.url_mappings.values():
            raise Exception("Mapping already exists")
        self.url_mappings[self.id] = url
        self.id += 1
        return self.id - 1

    def get_url_id(self, url):
        """Returns ID for a given URL. If URL does not exist in the dictionary, function raises ValueError """
        if url not in self.url_mappings.values():
            raise ValueError()
        return [k for k, v in self.url_mappings.items() if v == url][0]

    def get_mapping(self, idx):
        """Returns actual URL for a given ID"""
        return self.url_mappings[idx]

    def get_mappings(self):
        """Returns the dictionary of mappings between IDs (elements of short URLs) and actual URLs"""
        return self.url_mappings
