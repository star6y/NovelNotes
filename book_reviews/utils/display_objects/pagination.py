import math

class Pagination:

    def __init__(self, page, per_page, total_items):
        self.page = page
        self.per_page = per_page
        self.total_items = total_items
        self.total_pages = math.ceil(self.total_items / self.per_page)
    
    @property
    def has_previous(self):
        return self.page > 1
    
    @property
    def has_next(self):
        return self.page < self.total_pages
    
    @property
    def previous_page(self):
        return self.page - 1 if self.has_previous else None
    
    @property
    def next_page(self):
        return self.page + 1 if self.has_next else None
