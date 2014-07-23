from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata
from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.content.publication import PublicationSchema
from recensio.contenttypes.content.publication import Publication
from recensio.contenttypes.interfaces import IPublication
from zope.interface import implements


JournalSchema = (
    PublicationSchema.copy() +
    atapi.Schema((
        atapi.StringField(
            'issn',
            storage=atapi.AnnotationStorage(),
            widget=atapi.StringWidget(
                label=_(u"ISSN"),
                description=_(
                    u'description_issn',
                    default=(u"With or without hyphens.")
                ),
            ),
        ),
        atapi.StringField(
            'shortnameJournal',
            storage=atapi.AnnotationStorage(),
            widget=atapi.StringWidget(
                label=_(u"Shortname"),
            ),
        ),
        atapi.StringField(
            'yearOfPublication',
            storage=atapi.AnnotationStorage(),
            widget=atapi.StringWidget(
                label=_(u"Year of publication"),
            ),
        ),
        atapi.StringField(
            'placeOfPublication',
            storage=atapi.AnnotationStorage(),
            widget=atapi.StringWidget(
                label=_(u"Place of publication"),
            ),
        ),
        atapi.StringField(
            'publisher',
            storage=atapi.AnnotationStorage(),
            widget=atapi.StringWidget(
                label=_(u"Publisher"),
            ),
            searchable=True,
        ),
    ))
)

schemata.finalizeATCTSchema(
    JournalSchema,
    folderish=True,
    moveDiscussion=False
)


class IJournal(IPublication):
    """A publication with extended metadata."""


class Journal(Publication):
    """A publication with extended metadata."""
    implements(IJournal)

    meta_type = "Publication"
    schema = JournalSchema

atapi.registerType(Journal, 'philrom.policy')
