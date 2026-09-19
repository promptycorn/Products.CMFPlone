from .basetool import IPloneBaseTool
from zope import schema
from zope.interface import Interface


class IControlPanel(IPloneBaseTool):
    """ Interface for the ControlPanel """

    def registerConfiglet(id, name, action, condition='', permission='',
                          category='Plone', visible=1, appId=None,
                          imageUrl=None, description='', REQUEST=None):
        """ Registration of a Configlet """

    def unregisterConfiglet(id):
        """ unregister Configlet """

    def unregisterApplication(appId):
        """ unregister Application with all configlets """

    def getGroupIds():
        """ list of the group ids """

    def getGroups():
        """ list of groups as dicts with id and title """

    def enumConfiglets(group=None):
        """ lists the Configlets of a group, returns them as dicts by
            calling .getAction() on each of them """


class ISiteSchema(Interface):
    """BBB subset used by newer Plone support packages in the Py3 stage."""

    no_thumbs_portlet = schema.Bool(
        title=u'Suppress thumbs in portlets',
        required=False,
        default=False)

    thumb_scale_portlet = schema.TextLine(
        title=u'Portlet thumb scale',
        required=False,
        default=u'tile')
