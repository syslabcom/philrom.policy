# -*- coding: utf-8 -*-
from cgi import escape
from metadataformat import BaseMetadataFormat
from recensio.contenttypes.citation import getFormatter
from recensio.contenttypes.helperutilities import translate_message
from zope.i18nmessageid import Message


class PresentationMonographMetadataFormat(BaseMetadataFormat):

    def getDecoratedTitle(self, obj):
        rezensent_string = getFormatter(' ')(
            obj.reviewAuthors[0]["firstname"], obj.reviewAuthors[0]["lastname"])
        if rezensent_string:
            rezensent_string = "(%s)" % translate_message(
                Message(u"presented_by", "recensio", mapping={u"review_authors": rezensent_string}))
        titles = "<span class='title'>%s</span>" % obj.punctuated_title_and_subtitle
        full_citation = getFormatter(', ', ' ')
        return full_citation(obj.formatted_authors_editorial(), titles, rezensent_string)

    def get_citation_string(self, obj):
        """
        I think the in... part does not make sense for this content type
        Either return the custom citation or the generated one
        >>> from mock import Mock
        >>> at_mock = Mock()
        >>> at_mock.get = lambda x: None
        >>> at_mock.formatted_authors_editorial = lambda: u"Gerken\u2665, Patrick\u2665 / Pilz, Alexander"
        >>> at_mock.title = "Plone 4.0♥?"
        >>> at_mock.subtitle = "Das Benutzerhandbuch♥"
        >>> at_mock.reviewAuthors = [{'firstname' : 'Cillian♥', 'lastname'  : 'de Roiste♥'}]
        >>> at_mock.yearOfPublication = '2009♥'
        >>> at_mock.publisher = 'SYSLAB.COM GmbH♥'
        >>> at_mock.placeOfPublication = 'München♥'
        >>> at_mock.portal_url = lambda :'http://www.syslab.com'
        >>> at_mock.UID = lambda :'12345'
        >>> presentation = PresentationMonographNoMagic(at_mock)
        >>> presentation.directTranslate = lambda m: m.default
        >>> presentation.get_citation_string()
        u'de Roiste\u2665, Cillian\u2665: presentation of: Gerken\u2665, Patrick\u2665 / Pilz, Alexander, Plone 4.0\u2665? Das Benutzerhandbuch\u2665, M\\xfcnchen\u2665: SYSLAB.COM GmbH\u2665, 2009\u2665, <a href="http://syslab.com/r/12345">http://syslab.com/r/12345</a>'


        [Präsentator Nachname], [Präsentator Vorname]: presentation of: [Werkautor Nachname], [Werkautor Vorname], [Werktitel]. [Werk-Untertitel], [Erscheinungsort]: [Verlag], [Jahr], URL recensio.

        Big chunk removed, since it is not a review from a mag in: [Zs-Titel], [Nummer], [Heftnummer (gezähltes Jahr/Erscheinungsjahr)],

        Meier, Hans: presentation of: Meier, Hans, Geschichte des Abendlandes. Ein Abriss, München: Oldenbourg, 2010, in: Zeitschrift für Geschichte, 39, 3 (2008/2009), www.recensio.net/##

        """
        args = {
            'presentation_of' : translate_message(Message(
                    u"text_presentation_of", "recensio",
                    default="presentation of:")),
            'in'              : translate_message(Message(
                    u"text_in", "recensio", default="in:")),
            'page'            : translate_message(Message(
                    u"text_pages", "recensio", default="p.")),
            ':'               : ",",
            #translate_message(Message(u"text_colon", "recensio", default=":")),
            }
        rezensent = getFormatter(u', ')
        if obj.title[-1] in '!?:;.,':
            title_subtitle = getFormatter(u' ')
        else:
            title_subtitle = getFormatter(u'. ')

        item = getFormatter(u', ', u', ', u'%(:)s ' % args, u', ')
        mag_number_and_year = getFormatter(u', ', u', ', u' ')
        if False:
            _("presentation of")
        full_citation_inner = getFormatter(
            u'%(:)s %(presentation_of)s ' % args, u', ')
        rezensent_string = rezensent(
            obj.reviewAuthors[0]["lastname"],
            obj.reviewAuthors[0]["firstname"])
        authors_string = obj.formatted_authors_editorial()
        title_subtitle_string = '<span class="title">%s</span>' % escape(
            title_subtitle(obj.title, obj.subtitle))
        item_string = item(
            escape(authors_string),
            title_subtitle_string,
            escape(obj.placeOfPublication),
            escape(obj.publisher),
            escape(obj.yearOfPublication),
        )
        return full_citation_inner(escape(rezensent_string), item_string, obj.getUUIDUrl())


class PresentationOnlineResourceMetadataFormat(BaseMetadataFormat):

    def getDecoratedTitle(self, obj):
        rezensent_string = getFormatter(' ')(
            obj.reviewAuthors[0]["firstname"], obj.reviewAuthors[0]["lastname"])
        if rezensent_string:
            rezensent_string = "(%s)" % translate_message(
                Message(u"presented_by", "recensio",
                        mapping={u"review_authors": rezensent_string}))
        full_citation = getFormatter(' ')
        title = "<span class='title'>%s</span>" % obj.title.decode('utf-8')
        return full_citation(title, rezensent_string)

    def get_citation_string(self, obj):
        """
        >>> from mock import Mock
        >>> at_mock = Mock()
        >>> at_mock.reviewAuthors = [{'firstname' : 'Manuel♥', 'lastname'  : 'Reinhard♥'}]
        >>> at_mock.title = 'Homepage of SYSLAB.COM GmbH♥'
        >>> at_mock.portal_url = lambda :'http://www.syslab.com'
        >>> at_mock.UID = lambda :'12345'
        >>> at_mock.uri = 'http://www.syslab.com/home♥'
        >>> presentation = PresentationOnlineResourceNoMagic(at_mock)
        >>> presentation.directTranslate = lambda m: m.default
        >>> presentation.get_citation_string()
        u'Reinhard\u2665, Manuel\u2665: presentation of: Homepage of SYSLAB.COM GmbH\u2665, http://www.syslab.com/home\u2665, <a href="http://syslab.com/r/12345">http://syslab.com/r/12345</a>'


        Original Specification

        [Präsentator Nachname], [Präsentator Vorname]: presentation of: [Titel online resource], [URL online resource], URL recensio.

        Meier, Hans: presentation of:  perspectivia.net – Publikationsplattform für die Geisteswissenschaften, www.perspectivia.net, www.recensio.net/##
        """
        args = {
            'presentation_of' : translate_message(Message(
                    u"text_presentation_of", "recensio",
                    default="presentation of:")),
            'in'              : translate_message(Message(
                    u"text_in", "recensio", default="in:")),
            'page'            : translate_message(Message(
                    u"text_pages", "recensio", default="p.")),
            ':'               : ',',
            #translate_message(Message(u"text_colon", "recensio", default=":")),
        }
        rezensent = getFormatter(u', ')
        full_citation = getFormatter(u'%(:)s %(presentation_of)s ' % args)
        rezensent_string = rezensent(obj.reviewAuthors[0]["lastname"],
                                     obj.reviewAuthors[0]["firstname"])
        item = getFormatter(u', ')
        item_string = '<span class="title">%s</span>' % item(escape(obj.title), escape(obj.uri))
        item_string = item(item_string, obj.getUUIDUrl())
        return full_citation(escape(rezensent_string), item_string)
