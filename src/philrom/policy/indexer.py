from plone.indexer.interfaces import IIndexer
from zope.interface import implements


class PhilromIndexer(object):

    implements(IIndexer)

    def __init__(self, context, catalog):
        self.context = context
        self.catalog = catalog


class GetManuscriptsShelfmark(PhilromIndexer):
    def __call__(self):
        obj = self.context
        return obj.Schema()['manuscriptsShelfmark'].get(obj)


class GetMedievalAuthorsWorks(PhilromIndexer):
    def __call__(self):
        obj = self.context
        return obj.Schema()['medievalAuthorsWorks'].get(obj)


class TextForm(PhilromIndexer):
    def __call__(self):
        obj = self.context
        return obj.Schema()['textForm'].get(obj)
