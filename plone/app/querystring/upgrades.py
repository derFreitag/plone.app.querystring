# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getUtility
from plone.registry.interfaces import IRegistry


def upgrade_1_to_2_typo_in_registry(context):
    registry = getUtility(IRegistry)
    name = 'plone.app.querystring.field.getObjPositionInParent.operations'
    wrong_value = 'plone.app.querystring.operation.int.greaterThan'
    right_value = 'plone.app.querystring.operation.int.largerThan'
    values = registry.get(name)
    if not values:
        return
    if wrong_value in values:
        del values[values.index(wrong_value)]
    if right_value not in values:
        values.append(right_value)
    registry[name] = values


def fix_select_all_existing_collections(context):

    indexes_to_fix = [
        u'portal_type',
        u'review_state',
        u'Creator'
    ]
    old_operator = u"plone.app.querystring.operation.selection.is"
    new_operator = u"plone.app.querystring.operation.selection.any"

    catalog = context.portal_catalog
    brains = catalog.unrestrictedSearchResults(
        portal_type="Collection"
    )

    for brain in brains:
        changed = False
        obj = brain.getObject()
        fixed_querystring = list()
        for querystring in obj.query:
            if querystring['i'] in indexes_to_fix \
                    and querystring['o'] == old_operator:
                querystring['o'] = new_operator
                changed = True
            fixed_querystring.append(querystring)

        if changed:
            obj.query = fixed_querystring
            obj.reindexObject()
