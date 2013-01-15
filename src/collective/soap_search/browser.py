# -*- coding: utf-8 -*-
from DateTime import DateTime

try:
    from plone.app.search.browser import Search as BaseSearch
except:
    from collective.soap_search.backward_search import Search as BaseSearch

from soaplib.service import SoapServiceBase

from plone.z3cform import layout
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.browser.navtree import getNavigationRoot
from Products.CMFPlone.PloneBatch import Batch
from Products.ZCTextIndex.ParseTree import ParseError

from collective.soap_search.interfaces import ISettings


class Search(BaseSearch, SoapServiceBase):

    def __init__(self, context, request):
        BaseSearch.__init__(self, context, request)
        SoapServiceBase.__init__(self)

    def wsdl(self):
        res = self.request.RESPONSE
        res.setHeader('Content-Type, text/xml; charset="utf-8"')
        return SoapServiceBase.wsdl(self, self.context.absolute_url())

    def results(self, params):
        """ Get properly wrapped search results from the catalog.
        Everything in Plone that performs searches should go through this view.
        'query' should be a dictionary of catalog parameters.
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        query = params.get('query', None)
        query.pop('batch', None)
        query.pop('b_size', None)
        query.pop('b_start', None)
        batch = params.get('batch', True)
        b_size = params.get('b_size', 10)
        b_start = params.get('b_start', 0)
        date_keys = ('start', 'end')
        for k in date_keys:
            if query.has_key(k):
                v = query.get(k)
                if v and isinstance(v, dict):
                    dt_str = "%s/%s/%s %s:%s:%s" % (v['query'][0],
                                                    v['query'][1],
                                                    v['query'][2],
                                                    v['query'][3],
                                                    v['query'][4],
                                                    v['query'][5])
                    v['query'] = DateTime(dt_str)
                else:
                    dt_str = "%s/%s/%s %s:%s:%s" % (v[0],
                                                    v[1],
                                                    v[2],
                                                    v[3],
                                                    v[4],
                                                    v[5])
                    v = DateTime(dt_str)
        if query is None:
            query = {}
        if batch:
            query['b_start'] = b_start = int(b_start)
            query['b_size'] = b_size
        query = self.filter_query(query)

        if query is None:
            brains = []
        else:
            catalog = getToolByName(self.context, 'portal_catalog')
            try:
                brains = catalog(**query)
            except ParseError:
                return []

        if batch:
            brains = Batch(brains, b_size, b_start)
        schema = catalog.schema()
        results = []
        for brain in brains:
            entry = dict()
            for k in schema:
                entry[k] = brain[k] and brain[k] or ""
                if isinstance(entry[k], DateTime):
                    entry[k] = entry[k].parts()
                if isinstance(entry[k], unicode):
                    entry[k] = entry[k].encode()
            results.append(entry)
        return results

    def filter_query(self, query):
        request = self.request

        catalog = getToolByName(self.context, 'portal_catalog')
        valid_indexes = tuple(catalog.indexes())
        valid_keys = self.valid_keys + valid_indexes

        text = query.get('SearchableText', None)
        if text is None:
            text = request.form.get('SearchableText', '')
        if not text:
            # Without text, must provide a meaningful non-empty search
            valid = set(valid_indexes).intersection(query.keys())
            if not valid:
                return

        for k, v in request.form.items():
            if v and ((k in valid_keys) or k.startswith('facet.')):
                query[k] = v
        if text:
            query['SearchableText'] = quote_chars(text)

        # don't filter on created at all if we want all results
        created = query.get('created')
        if created:
            if created.get('query'):
                if created['query'][0] <= EVER:
                    del query['created']

        # respect `types_not_searched` setting
        types = query.get('portal_type', [])
        if 'query' in types:
            types = types['query']
        query['portal_type'] = self.filter_types(types)
        # respect effective/expiration date
        query['show_inactive'] = False
        # respect navigation root
        if 'path' not in query:
            query['path'] = getNavigationRoot(self.context)

        return query


class SettingsEditForm(RegistryEditForm):
    """
    Define form logic
    """
    schema = ISettings
    label = u"collective.soap_search settings"


SettingsEditFormView = layout.wrap_form(SettingsEditForm, ControlPanelFormWrapper)
>>>>>>> 2dba3c3eebac239848c88b5d50414babf52aa528
