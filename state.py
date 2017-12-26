class CLIState:
    def __init__(self):
        self.listing = []
        self.listing_map = {}

    def set_state(self, listing):
        self.listing = listing
        self._gen_listing_map(listing)

    def _gen_listing_map(self, listing):
        for item in listing:
            self.listing_map[item.name] = item

    def fetch(self, identifier, hint=None):
        if hint != '%s':
            try:
                identifier = int(identifier)
                return self.listing[identifier]
            except ValueError:
                pass
        elif hint != '%p':
            try:
                return self.listing_map[identifier]
            except KeyError:
                pass
        else:
            return None
