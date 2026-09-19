try:
    from Products.CMFPlone import patches  # noqa
except ImportError:
    pass

from Products.CMFCore.RegistrationTool import RegistrationTool
addMember = getattr(RegistrationTool.addMember, '__func__',
                    RegistrationTool.addMember)
if hasattr(addMember, '__doc__'):
    del addMember.__doc__
