from Products.Archetypes import atapi
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from philrom.policy.content.common import PhilromSchema
from recensio.contenttypes.interfaces.reviewmonograph import IReviewMonograph
from recensio.contenttypes.interfaces.reviewjournal import IReviewJournal
from zope.component import adapts
from zope.interface import implements
from metadataformat import BaseMetadataFormat


class SELinesField(ExtensionField, atapi.LinesField):
    """An extension/lines field."""


class ReviewExtenderBase(object):

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return [
            SELinesField(
                field.getName(),
                multiValued=1,
                accessor=field.accessor,
                schemata="reviewed_text",
                storage=field.getStorage(),
                vocabulary=field.vocabulary,
                widget=field.widget,
            ) for field in PhilromSchema.fields()
        ]

    def getOrder(self, schematas):
        position = schematas['reviewed_text'].index('languageReviewedText')
        reorder = lambda schema: schema[:position] + schema[position + 1:-1] +\
            ['languageReviewedText'] + schema[-1:]
        schematas['reviewed_text'] = reorder(schematas['reviewed_text'])
        return schematas


class MetadataFormat(BaseMetadataFormat):
    pass


class ReviewMonographExtender(ReviewExtenderBase):
    adapts(IReviewMonograph)
    implements(IOrderableSchemaExtender)


class ReviewJournalExtender(ReviewExtenderBase):
    adapts(IReviewJournal)
    implements(IOrderableSchemaExtender)
