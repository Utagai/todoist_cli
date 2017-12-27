from app.objects import Project

class CLIState:
    def __init__(self):
        self.listing = []
        self.listing_map = {}
        self.active_project = None

    def set_state(self, listing):
        self.listing = listing
        self._gen_listing_map(listing)

    def clear_state(self):
        self.listing = []
        self.listing_map = {}

    def set_project(self, project_id):
        self.active_project = Project(project_id)

    def _gen_listing_map(self, listing):
        for item in listing:
            self.listing_map[item.name.lower()] = item

    def fetch(self, identifier, hint=None):
        if hint == '%p' or not hint:
            try:
                return self.listing[int(identifier)]
            except ValueError:
                pass
        if hint == '%s' or not hint:
            try:
                return self.listing_map[identifier.lower()]
            except KeyError:
                pass
        if hint == '%c' or not hint:
            try:
                return self.active_project
            except AttributeError:
                pass
        return None
