## Script (Python) "sort_modified_ascending"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=catalog_sequence
##title=

sorted = catalog_sequence[:]
sorted.sort(key=lambda x: x.modified())
return sorted
