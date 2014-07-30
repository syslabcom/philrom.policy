from Products.Archetypes import atapi
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from metadataformat import BaseMetadataFormat
from philrom.policy.content.common import PhilromSchema
from recensio.contenttypes.citation import getFormatter
from recensio.contenttypes.helperutilities import get_formatted_names
from recensio.contenttypes.helperutilities import translate_message
from recensio.contenttypes.interfaces.reviewjournal import IReviewJournal
from recensio.contenttypes.interfaces.reviewmonograph import IReviewMonograph
from zope.component import adapts
from zope.i18nmessageid import Message
from zope.interface import implements


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


class ReviewMonographExtender(ReviewExtenderBase):
    adapts(IReviewMonograph)
    implements(IOrderableSchemaExtender)


class ReviewMonographMetadataFormat(BaseMetadataFormat):
    pass


class ReviewJournalExtender(ReviewExtenderBase):
    adapts(IReviewJournal)
    implements(IOrderableSchemaExtender)


class ReviewJournalMetadataFormat(BaseMetadataFormat):

    def getDecoratedTitle(self, obj, lastname_first=False):
        item = getFormatter(', ', ' ', ', ')
        mag_year = getFormatter('/')(obj.officialYearOfPublication, obj.yearOfPublication)
        mag_year = mag_year and '(' + mag_year + ')' or None
        item_string = u'<span class="title">%s</span>' % item(
            obj.title, obj.volumeNumber, mag_year, obj.issueNumber)

        if lastname_first:
            reviewer_string = get_formatted_names(
                u' / ', ', ', obj.reviewAuthors, lastname_first=lastname_first)
        else:
            reviewer_string = get_formatted_names(
                u' / ', ' ', obj.reviewAuthors, lastname_first=lastname_first)

        if reviewer_string:
            reviewer_string = "(%s)" % translate_message(
                Message(u"reviewed_by", "recensio",
                        mapping={u"review_authors": reviewer_string}))

        return ' '.join((item_string, reviewer_string))
