from Products.Archetypes import atapi
from recensio.contenttypes.content.presentationarticlereview import PresentationArticleReview
from recensio.contenttypes.content.presentationarticlereview import PresentationArticleReviewSchema
from recensio.contenttypes.interfaces.presentationarticlereview import IPresentationArticleReview
from zope.interface import implements


ArticleJournalSchema = PresentationArticleReviewSchema.copy()
ArticleJournalSchema.moveField('languageReviewedText', pos='bottom')


class IArticleJournal(IPresentationArticleReview):
    """ """


class ArticleJournal(PresentationArticleReview):
    implements(IArticleJournal)

    schema = ArticleJournalSchema


atapi.registerType(ArticleJournal, 'philrom.policy')
