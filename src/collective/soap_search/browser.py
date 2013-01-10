# -*- coding: utf-8 -*-

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
        import ipdb;ipdb.set_trace()
        results = super(Search, self).results(query, batch, b_size, b_start)
        return [{'id': i.id,
                 'title': i.Title} for i in results]
