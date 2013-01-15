# -*- coding: utf-8 -*-
from DateTime import DateTime

try:
    from plone.app.search.browser import Search as BaseSearch
except:
    from collective.soap_search.backward_search import Search as BaseSearch

from soaplib.service import SoapServiceBase

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
        query = params.get('query', None)
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
        results = super(Search, self).results(query, batch, b_size, b_start)
        return [{'id': i.id,
                 'title': i.Title} for i in results]
