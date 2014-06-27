from Products.Archetypes import atapi
from recensio.contenttypes.content.presentationcollection import PresentationCollection
from recensio.contenttypes.content.presentationcollection import PresentationCollectionSchema
from recensio.contenttypes.interfaces.presentationcollection import IPresentationCollection
from zope.interface import implements

from philrom.policy.content.common import PhilromSchema


ArticleEditedVolumeSchema = (
    PresentationCollectionSchema.copy() + PhilromSchema.copy()
)
ArticleEditedVolumeSchema.moveField('languageReviewedText',
                                    before='medievalAuthorsWorks')


class IArticleEditedVolume(IPresentationCollection):
    """ """


class ArticleEditedVolume(PresentationCollection):
    implements(IArticleEditedVolume)

    schema = ArticleEditedVolumeSchema


atapi.registerType(ArticleEditedVolume, 'philrom.policy')

