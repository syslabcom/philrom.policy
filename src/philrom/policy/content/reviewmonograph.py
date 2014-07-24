from Products.Archetypes import atapi
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.field import ExtensionField
from recensio.contenttypes.interfaces.reviewmonograph import IReviewMonograph
from zope.component import adapts
from zope.interface import implements

from philrom.policy.content.common import PhilromSchema


class SELinesField(ExtensionField, atapi.LinesField):
    """An extension/lines field."""


class ReviewMonographExtender(object):
    adapts(IReviewMonograph)
    implements(IOrderableSchemaExtender)

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
