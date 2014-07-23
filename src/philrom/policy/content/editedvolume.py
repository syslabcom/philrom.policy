from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata
from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.content.publication import PublicationSchema
from recensio.contenttypes.content.publication import Publication
from recensio.contenttypes.interfaces import IPublication
from zope.interface import implements


EditedVolumeSchema = (
    PublicationSchema.copy() +
    atapi.Schema((
        atapi.StringField(
            'isbn',
            storage=atapi.AnnotationStorage(),
            widget=atapi.StringWidget(
                label=_(u"ISBN"),
                description=_(
                    u'description_isbn',
                    default=(
                        u"With or without hyphens. In case of several numbers please "
                        "choose the hard cover edition.")
                ),
            ),
        ),
        DataGridField(
            'editorial',
            storage=atapi.AnnotationStorage(),
            columns=("lastname", "firstname"),
            default=[{'lastname':'', 'firstname':''}],
            widget=DataGridWidget(
                label=_(u"label_editorial"),
                columns={"lastname": Column(_(u"Last name")),
                         "firstname": Column(_(u"First name")),}
            ),
            searchable=True,
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
    EditedVolumeSchema,
    folderish=True,
    moveDiscussion=False
)


class IEditedVolume(IPublication):
    """A publication with extended metadata."""


class EditedVolume(Publication):
    """A publication with extended metadata."""
    implements(IEditedVolume)

    meta_type = "Publication"
    schema = EditedVolumeSchema

atapi.registerType(EditedVolume, 'philrom.policy')
