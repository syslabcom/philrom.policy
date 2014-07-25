from plone.indexer.decorator import indexer
from recensio.contenttypes.interfaces.review import IReview


@indexer(IReview)
def textForm(obj):
    return obj.Schema()['textForm'].get(obj)


@indexer(IReview)
def getMedievalAuthorsWorks(obj):
    return obj.Schema()['medievalAuthorsWorks'].get(obj)


@indexer(IReview)
def getManuscriptsShelfmark(obj):
    return obj.Schema()['manuscriptsShelfmark'].get(obj)
