from . import addzmiplonesite          # Add an explicit link to add a new Plone
                                # site to the ZMI for faster access

from . import addzmisecuritywarning    # Add a warning to the ZMI security tab
                                # that you shouldn't use it

from . import dateIndexPatch           # Avoid OverflowErrors in Date*Indexes

from . import unicodeFallbackPatch     # Makes the TAL engine in Zope 2.10+ accept
                                # utf-8 encoded strings as well as Unicode

from . import csrf                     # Protects most important methods from
csrf.applyPatches()             # CSRF attacks

from . import speed                    # Various caching patches to improve speed

from . import securemailhost           # SecureMailHost BBB, remove in Plone 5.0
securemailhost.applyPatches()

from . import iso8601                  # use `DateTime.ISO8601` for `DateTime.ISO`
iso8601.applyPatches()

from . import security					# misc security fixes

from . import sendmail
sendmail.applyPatches()

try:
    # kupu may not be installed
    from . import kupu
except ImportError:
    pass

from . import addMember
from . import publishing

from . import z3c_form
