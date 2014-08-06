# -*- coding: utf-8 -*-
from Products.Archetypes import atapi
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from cgi import escape
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

    def get_citation_string(self, obj):
        """
        Either return the custom citation or the generated one
        >>> from mock import Mock
        >>> at_mock = Mock()
        >>> at_mock.customCitation = ''
        >>> at_mock.get = lambda x: None
        >>> at_mock.formatted_authors_editorial = lambda: u"Gerken\u2665, Patrick\u2665 / Pilz, Alexander"
        >>> at_mock.title = "Plone 4.0♥?"
        >>> at_mock.subtitle = "Das Benutzerhandbuch♥"
        >>> at_mock.reviewAuthors = [{'firstname' : 'Cillian♥', 'lastname' : 'de Roiste♥'}]
        >>> at_mock.yearOfPublication = '2009♥'
        >>> at_mock.publisher = 'SYSLAB.COM GmbH♥'
        >>> at_mock.placeOfPublication = 'München♥'
        >>> at_mock.get_issue_title = lambda :'Open Source Mag 1♥'
        >>> at_mock.get_volume_title = lambda :'Open Source Mag Vol 1♥'
        >>> at_mock.get_publication_title = lambda :'Open Source♥'
        >>> at_mock.portal_url = lambda :'http://www.syslab.com'
        >>> at_mock.UID = lambda :'12345'
        >>> at_mock.canonical_uri = ''
        >>> at_mock.page_start_end_in_print = '11-21'
        >>> review = ReviewMonographNoMagic(at_mock)
        >>> review.directTranslate = lambda m: m.default
        >>> review.get_citation_string()
        u'de Roiste\u2665, Cillian\u2665: review of: Gerken\u2665, Patrick\u2665 / Pilz, Alexander, Plone 4.0\u2665? Das Benutzerhandbuch\u2665, M\\xfcnchen\u2665: SYSLAB.COM GmbH\u2665, 2009\u2665, in: Open Source\u2665, Open Source Mag Vol 1\u2665, Open Source Mag 1\u2665, p. 11-21, <a href="http://syslab.com/r/12345">http://syslab.com/r/12345</a>'


        Original Spec:

        [Rezensent Nachname], [Rezensent Vorname]: review of: [Werkautor Nachname], [Werkautor Vorname], [Werktitel]. [Werk-Untertitel], [Erscheinungsort]: [Verlag], [Jahr], in: [Zs-Titel], [Nummer], [Heftnummer (Erscheinungsjahr)], p.[pageStart]-[pageEnd] URL recensio.

        Werkautoren kann es mehrere geben, die werden dann durch ' / ' getrennt alle aufgelistet.
        Note: gezähltes Jahr entfernt.
        Da es die Felder Zs-Titel, Nummer und Heftnummer werden die Titel der Objekte magazine, volume, issue genommen, in dem der Review liegt

        Müller, Klaus: review of: Meier, Hans, Geschichte des Abendlandes. Ein Abriss, München: Oldenbourg, 2010, in: Zeitschrift für Geschichte, 39, 3 (2008/2009), www.recensio.net/##

        """
        if obj.customCitation:
            return scrubHTML(obj.customCitation).decode('utf8')

        args = {
            'review_of' : translate_message(Message(
                    u"text_review_of", "recensio", default="review of:")),
            'in'        : translate_message(Message(
                    u"text_in", "recensio", default="in:")),
            'page'      : translate_message(Message(
                    u"text_pages", "recensio", default="p.")),
            ':'         : ",",
            #translate_message(Message(u"text_colon", "recensio", default=":")),
            }
        if obj.title[-1] in '!?:;.,':
            title_subtitle = getFormatter(u' ')
        else:
            title_subtitle = getFormatter(u'. ')
        rev_details_formatter = getFormatter(
            u', ', u', ', u'%(:)s ' % args, u', ')
        rezensent_string = get_formatted_names(
            u' / ', ', ', obj.reviewAuthors, lastname_first = True)
        authors_string = obj.formatted_authors_editorial()
        title_subtitle_string = '<span class="title">%s</span>' % (
            title_subtitle(obj.title, obj.subtitle))
        item_string = rev_details_formatter(
            authors_string, title_subtitle_string,
            obj.placeOfPublication, obj.publisher,
            obj.yearOfPublication)
        mag_year_string = obj.yearOfPublication.decode('utf-8')
        mag_year_string = mag_year_string and u'(' + mag_year_string + u')' \
            or None

        mag_number_formatter = getFormatter(u', ', u', ')
        mag_number_string = mag_number_formatter(
            obj.get_publication_title(), obj.get_volume_title(),
            obj.get_issue_title())

        location = obj.getUUIDUrl()
        if getattr(obj, "canonical_uri", False): #3102
            location = translate_message(
                Message(u"label_downloaded_via_recensio","recensio"))

        citation_formatter = getFormatter(
            u'%(:)s %(review_of)s ' % args, ', %(in)s ' % args, ', %(page)s ' % args, u', ')

        citation_string = citation_formatter(
            escape(rezensent_string), item_string,
            escape(mag_number_string),
            obj.page_start_end_in_print, location)

        return citation_string


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

    def get_citation_string(self, obj):
        """
        >>> from mock import Mock
        >>> at_mock = Mock()
        >>> at_mock.get = lambda x: None
        >>> at_mock.customCitation = ''
        >>> at_mock.title = "Plone Mag♥"
        >>> at_mock.reviewAuthors = [{'firstname' : 'Cillian♥', 'lastname'  : 'de Roiste♥'}]
        >>> at_mock.yearOfPublication = '2009♥'
        >>> at_mock.officialYearOfPublication = '2010♥'
        >>> at_mock.publisher = 'SYSLAB.COM GmbH♥'
        >>> at_mock.placeOfPublication = 'München♥'
        >>> at_mock.volumeNumber = '1♥'
        >>> at_mock.issueNumber = '3♥'
        >>> at_mock.get_issue_title = lambda :'Open Source Mag 1♥'
        >>> at_mock.get_volume_title = lambda :'Open Source Mag Vol 1♥'
        >>> at_mock.get_publication_title = lambda :'Open Source♥'
        >>> at_mock.portal_url = lambda :'http://www.syslab.com'
        >>> at_mock.UID = lambda :'12345'
        >>> at_mock.canonical_uri = ''
        >>> at_mock.page_start_end_in_print = '11-21'
        >>> review = ReviewJournalNoMagic(at_mock)
        >>> review.directTranslate = lambda m: m.default
        >>> review.get_citation_string()
        u'de Roiste\u2665, Cillian\u2665: review of: Plone Mag\u2665, 1\u2665, 3\u2665 (2010\u2665/2009\u2665), in: Open Source\u2665, Open Source Mag Vol 1\u2665, Open Source Mag 1\u2665, p. 11-21, <a href="http://syslab.com/r/12345">http://syslab.com/r/12345</a>'


        Return the citation according to this schema:
        [Rezensent Nachname], [Rezensent Vorname]: review of: [Zs-Titel der rez. Zs.], [Nummer], [Heftnummer (gezähltes Jahr/Erscheinungsjahr)], in: [Zs-Titel], [Nummer], [Heftnummer (gezähltes Jahr/Erscheinungsjahr)], p.[pageStart]-[pageEnd] URL recensio.

        The years of the magazine article reviewing the other magazine does
        not exist.
        """
        if obj.customCitation:
            return scrubHTML(obj.customCitation).decode('utf8')

        rev_details_formatter = getFormatter(u', ', u', ', u' ')
        mag_year = getFormatter('/')(obj.officialYearOfPublication,
                                     obj.yearOfPublication)
        mag_year = mag_year and '(' + mag_year + ')' or None
        item_string = '<span class="title">%s</span>' % escape(
            rev_details_formatter(obj.title, obj.volumeNumber, obj.issueNumber, mag_year))

        reference_mag = getFormatter(', ',  ', ')
        reference_mag_string = reference_mag(
            obj.get_publication_title(), obj.get_volume_title(), obj.get_issue_title())

        location = obj.getUUIDUrl()
        if getattr(obj, "canonical_uri", False): #3102
            location = translate_message(
                Message(u"label_downloaded_via_recensio", "recensio"))

        rezensent_string = get_formatted_names(
            u' / ', ', ', obj.reviewAuthors, lastname_first = True)
        args = {
            'review_of' : translate_message(Message(
                    u"text_review_of", "recensio", default="review of:")),
            'in'        : translate_message(Message(
                    u"text_in", "recensio", default="in:")),
            'page'      : translate_message(Message(
                    u"text_pages", "recensio", default="p.")),
            ':'         : ",",
            #translate_message(Message(u"text_colon", "recensio", default=":")),
            }
        citation_formatter = getFormatter(
            u'%(:)s %(review_of)s ' % args, ', %(in)s ' % args, ', %(page)s '
            % args, u', ')
        citation_string = citation_formatter(
            escape(rezensent_string), item_string,
            escape(reference_mag_string), obj.page_start_end_in_print,
            location)
        return citation_string
