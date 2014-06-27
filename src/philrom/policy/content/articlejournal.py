from Products.Archetypes import atapi
from recensio.contenttypes.content.presentationarticlereview import PresentationArticleReview
from recensio.contenttypes.content.presentationarticlereview import PresentationArticleReviewSchema
from recensio.contenttypes.interfaces.presentationarticlereview import IPresentationArticleReview
from zope.interface import implements

from philrom.policy.content.common import PhilromSchema


ArticleJournalSchema = (
    PresentationArticleReviewSchema.copy() + PhilromSchema.copy()
)
ArticleJournalSchema.moveField('languageReviewedText',
                               before='medievalAuthorsWorks')


class IArticleJournal(IPresentationArticleReview):
    """ """


class ArticleJournal(PresentationArticleReview):
    implements(IArticleJournal)

    schema = ArticleJournalSchema


atapi.registerType(ArticleJournal, 'philrom.policy')
