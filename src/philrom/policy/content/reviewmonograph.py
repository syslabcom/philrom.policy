from Products.Archetypes import atapi
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from philrom.policy.content.common import PhilromSchema
from recensio.contenttypes.citation import getFormatter
from recensio.contenttypes.content.review import get_formatted_names
from recensio.contenttypes.helperutilities import translate_message
from recensio.contenttypes.interfaces import IDecoratedTitle
from recensio.contenttypes.interfaces.reviewmonograph import IReviewMonograph
from zope import interface
from zope.component import adapts
from zope.i18nmessageid import Message
from zope.interface import implements


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


class DecoratedTitle(object):
    interface.implements(IDecoratedTitle)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def getDecoratedTitle(self, obj, lastname_first=False):
        authors_string = obj.formatted_authors_editorial

        rezensent_string = get_formatted_names(
            u' / ', ' ', obj.reviewAuthors, lastname_first=lastname_first)
        if rezensent_string:
            rezensent_string = "%s" % translate_message(
                Message(
                    u"reviewed_by", "recensio",
                    mapping={u"review_authors": rezensent_string},
                )
            )

        titles = "<span class='titles'>%s</span>" % obj.punctuated_title_and_subtitle
        pub_year = "(%s)" % obj.yearOfPublication
        full_citation = getFormatter(', ', ' ', ', ')
        return full_citation(authors_string, titles, pub_year, rezensent_string)
