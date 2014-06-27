from Products.ATVocabularyManager import NamedVocabulary
from Products.Archetypes import atapi

from philrom.policy import _


PhilromSchema = atapi.Schema(
    (
        atapi.LinesField(
            'manuscriptsShelfmark',
            schemata="presented_text",
            storage=atapi.AnnotationStorage(),
            vocabulary=NamedVocabulary("manuscripts_shelfmark"),
            widget=atapi.MultiSelectionWidget(
                label=_(u"Manuscripts (Shelfmark)"),
                size=10,
            ),
        ),
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
