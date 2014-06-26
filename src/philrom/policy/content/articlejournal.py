from Products.ATVocabularyManager import NamedVocabulary
from Products.Archetypes import atapi
from recensio.contenttypes.content.presentationarticlereview import PresentationArticleReview
from recensio.contenttypes.content.presentationarticlereview import PresentationArticleReviewSchema
from recensio.contenttypes.interfaces.presentationarticlereview import IPresentationArticleReview
from zope.interface import implements

from philrom.policy import _


ArticleJournalSchema = (
    PresentationArticleReviewSchema.copy() +
    atapi.Schema(
        (
            atapi.LinesField(
                'medievalAuthorsWorks',
                schemata="presented_text",
                storage=atapi.AnnotationStorage(),
                vocabulary=NamedVocabulary("medieval_authors_works"),
                widget=atapi.MultiSelectionWidget(
                    label=_(u"Medieval authors/works"),
                    size=10,
                ),
            ),
        )
    )
)
ArticleJournalSchema.moveField('languageReviewedText',
                               before='medievalAuthorsWorks')


class IArticleJournal(IPresentationArticleReview):
    """ """


class ArticleJournal(PresentationArticleReview):
    implements(IArticleJournal)

    schema = ArticleJournalSchema


atapi.registerType(ArticleJournal, 'philrom.policy')
