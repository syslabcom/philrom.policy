import pkg_resources
from Products.ATVocabularyManager.utils.vocabs import createSimpleVocabs
from Products.CMFCore.utils import getToolByName

vocabularies = {
    'text_form': {
        'prose': 'Prose',
        'poetry': 'Poetry',
        'prosimetre': 'Prosimetre',
    }
}


def importVocabularies(self):
    if self.readDataFile('philrom.policy_marker.txt') is None:
        return
    path_tmpl = '../../../vocabularies/%s'
    site = self.getSite()
    pvm = getToolByName(site, 'portal_vocabularies')
    for (filenamepart, vocabname) in (
            ('area.vdex', 'region_values'),
            ('periodo.vdex', 'epoch_values'),
            ('temi.vdex', 'topic_values'),
    ):
        if vocabname in pvm:
            pvm.manage_delObjects([vocabname])
        pvm.invokeFactory('VdexFileVocabulary', vocabname, showLeafsOnly=False)
        pvm[vocabname].importXMLBinding(pkg_resources.resource_string(
            __name__, path_tmpl % filenamepart))

        for simple_vocabname in vocabularies:
            if simple_vocabname in pvm:
                pvm.manage_delObjects([simple_vocabname])
            createSimpleVocabs(
                pvm,
                {simple_vocabname: vocabularies[simple_vocabname].items()})
