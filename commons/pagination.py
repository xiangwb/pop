"""Simple helper to paginate query
"""
import math
from mongoengine.queryset import QuerySet

DEFAULT_PAGE_SIZE = 10
DEFAULT_PAGE_NUMBER = 1

__all__ = ("Pagination",)


class Pagination(object):
    """
    This is class for paginate
    """

    def __init__(self, iterable, page=None, per_page=None):

        self.iterable = iterable
        page = page if page and page > 0 else DEFAULT_PAGE_NUMBER
        per_page = per_page if per_page else DEFAULT_PAGE_SIZE
        self.page = page
        self.per_page = per_page

        if isinstance(iterable, QuerySet):
            self.total = iterable.count()
        else:
            self.total = len(iterable)

        start_index = (page - 1) * per_page
        end_index = page * per_page

        self.items = iterable[start_index:end_index]
        if isinstance(self.items, QuerySet):
            self.items = self.items.select_related()
        if not self.items and page != 1:
            raise Exception

    @property
    def pages(self):
        """The total number of pages"""
        return int(math.ceil(self.total / float(self.per_page)))

    def prev(self, error_out=False):
        """Returns a :class:`Pagination` object for the previous page."""
        assert self.iterable is not None, ('an object is required '
                                           'for this method to work')
        iterable = self.iterable
        if isinstance(iterable, QuerySet):
            iterable._skip = None
            iterable._limit = None
        return self.__class__(iterable, self.page - 1, self.per_page)

    @property
    def prev_num(self):
        """Number of the previous page."""
        return self.page - 1

    @property
    def has_prev(self):
        """True if a previous page exists"""
        return self.page > 1

    def next(self, error_out=False):
        """Returns a :class:`Pagination` object for the next page."""
        assert self.iterable is not None, ('an object is required '
                                           'for this method to work')
        iterable = self.iterable
        if isinstance(iterable, QuerySet):
            iterable._skip = None
            iterable._limit = None
        return self.__class__(iterable, self.page + 1, self.per_page)

    @property
    def has_next(self):
        """True if a next page exists."""
        return self.page < self.pages

    @property
    def next_num(self):
        """Number of the next page"""
        return self.page + 1

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in range(1, self.pages + 1):
            if (
                    num <= left_edge or
                    num > self.pages - right_edge or
                    (self.page - left_current <= num <= self.page + right_current)
            ):
                if last + 1 != num:
                    yield None
                yield num
                last = num
        if last != self.pages:
            yield None

    def paginate(self, schema):
        return schema.dump(self.items, many=True), {
            "total": self.total,
            "total_page": self.pages,
            "page": self.page,
            "limit": self.per_page
        }
