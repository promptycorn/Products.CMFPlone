from zope.event import notify
from zope.component import queryUtility
from zope.interface import implementer
from zope.component.hooks import setSite

from plone.i18n.interfaces import ILanguageSchema
from plone.registry.interfaces import IRegistry
from Products.GenericSetup.interfaces import IBody
from Products.GenericSetup.tool import SetupTool
from Products.GenericSetup.ZCatalog.exportimport import ZCatalogXMLAdapter
from zope.component import queryMultiAdapter

from Products.CMFPlone.events import SiteManagerCreatedEvent
from Products.CMFPlone.interfaces import IFilterSchema
from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFPlone.Portal import PloneSite

_TOOL_ID = 'portal_setup'
_DEFAULT_PROFILE = 'Products.CMFPlone:plone'
_CONTENT_PROFILE = 'Products.CMFPlone:plone-content'

# A little hint for PloneTestCase
_IMREALLYPLONE4 = True


def _ensureCatalogConfigured(site, setup_tool, profile_id):
    catalog = getattr(site, 'portal_catalog', None)
    if catalog is None:
        return
    context = setup_tool._getImportContext('profile-%s' % profile_id)
    body = context.readDataFile('catalog.xml')
    if body is None:
        return
    importer = queryMultiAdapter((catalog, context), IBody)
    if importer is None:
        importer = ZCatalogXMLAdapter(catalog, context)
    importer.filename = 'catalog.xml'
    importer.body = body


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        return [_DEFAULT_PROFILE,
                _CONTENT_PROFILE,
                'Products.Archetypes:Archetypes',
                'Products.CMFDiffTool:CMFDiffTool',
                'Products.CMFEditions:CMFEditions',
                'Products.CMFFormController:CMFFormController',
                'Products.CMFPlone:dependencies',
                'Products.CMFPlone:testfixture',
                'Products.CMFQuickInstallerTool:CMFQuickInstallerTool',
                'Products.NuPlone:uninstall',
                'Products.MimetypesRegistry:MimetypesRegistry',
                'Products.PasswordResetTool:PasswordResetTool',
                'Products.PortalTransforms:PortalTransforms',
                'Products.PloneLanguageTool:PloneLanguageTool',
                'Products.PlonePAS:PlonePAS',
                'archetypes.referencebrowserwidget:default',
                'borg.localrole:default',
                'Products.TinyMCE:TinyMCE',
                'Products.TinyMCE:upgrade_10_to_11',
                'Products.TinyMCE:uninstall',
                'plone.browserlayer:default',
                'plone.keyring:default',
                'plone.outputfilters:default',
                'plone.portlet.static:default',
                'plone.portlet.collection:default',
                'plone.protect:default',
                'plonetheme.sunburst:uninstall',
                'plone.app.blob:default',
                'plone.app.blob:file-replacement',
                'plone.app.blob:image-replacement',
                'plone.app.blob:sample-type',
                'plone.app.discussion:default',
                'plone.app.folder:default',
                'plone.app.imaging:default',
                'plone.app.jquery:initial-upgrade',
                'plone.app.search:default',
                'plone.resource:default',
                'collective.z3cform.datetimewidget:default',
                ]


def zmi_constructor(context):
    """This is a dummy constructor for the ZMI."""
    url = context.DestinationURL()
    request = context.REQUEST
    return request.response.redirect(url + '/@@plone-addsite?site_id=Plone')


def addPloneSite(context, site_id, title='Plone site', description='',
                 create_userfolder=True, email_from_address='',
                 email_from_name='', validate_email=True,
                 profile_id=_DEFAULT_PROFILE, snapshot=False,
                 extension_ids=(), setup_content=True, default_language='en'):
    """Add a PloneSite to the context."""
    context._setObject(site_id, PloneSite(site_id))
    site = context._getOb(site_id)
    site.setLanguage(default_language)
    # Set the accepted language for the rest of the request.  This makes sure
    # the front-page text gets the correct translation also when your browser
    # prefers non-English and you choose English as language for the Plone
    # Site.
    request = context.REQUEST
    request['HTTP_ACCEPT_LANGUAGE'] = default_language

    site[_TOOL_ID] = SetupTool(_TOOL_ID)
    setup_tool = site[_TOOL_ID]

    notify(SiteManagerCreatedEvent(site))
    setSite(site)

    setup_tool.setBaselineContext('profile-%s' % profile_id)
    setup_tool.runAllImportStepsFromProfile('profile-%s' % profile_id)
    registry = queryUtility(IRegistry, context=site)
    if registry is not None:
        if 'plone.default_language' not in registry:
            registry.registerInterface(ILanguageSchema, prefix='plone')
        if 'plone.disable_filtering' not in registry:
            registry.registerInterface(IFilterSchema, prefix='plone')
        registry['plone.default_language'] = default_language
        registry['plone.available_languages'] = [default_language]
    if setup_content:
        setup_tool.runAllImportStepsFromProfile(
                        'profile-%s' % _CONTENT_PROFILE)

    props = dict(
        title=title,
        description=description,
        email_from_address=email_from_address,
        email_from_name=email_from_name,
        validate_email=validate_email,
    )
    # Do this before applying extension profiles, so the settings from a
    # properties.xml file are applied and not overwritten by this
    site.manage_changeProperties(**props)

    for extension_id in extension_ids:
        setup_tool.runAllImportStepsFromProfile('profile-%s' % extension_id)

    _ensureCatalogConfigured(site, setup_tool, profile_id)

    if snapshot is True:
        setup_tool.createSnapshot('initial_configuration')

    return site
