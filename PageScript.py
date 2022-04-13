import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from utilities import ScriptHelper

proxy_stores = [3, 4, 7]

class PageScript():

    def get_item_list(self, params):
        res = {'error': False}
        dom = ScriptHelper.get_dom_from_url(params['url'], params['proxyData'][1], False if params['sid'] in proxy_stores else True)
        if type(dom) is not bool and dom is not None:
            res['items'] = dom.xpath(params['xpath'])
            if len(res['items']):
                if params['total'] is not None:
                    total = dom.xpath(params['total'])
                    if len(total):
                        res['total'] = ScriptHelper.onlyNumber(total[0])
                if params['pagination'] is not None:
                    nextPage = dom.xpath(params['pagination'])
                    if len(nextPage):
                        res['next'] = nextPage[0]
            else:
                ids = dom.xpath("//div//@id")
                if ScriptHelper.is_blocked(ids):
                    res['error'] = True
                    res['reason'] = "BLOCKED"
        else:
            res['error'] = True
        return res

    def script_handler(self, params):
        res = self.get_item_list(params)
        res['tid'] = params['tid']
        res['page'] = params['page']
        return res

    def invoke_wrapper(self, payloads):
        res = []
        for response in self.request_parallel(payloads, size=10):
            res.append(response)
        return res

    def request_parallel(self, payloads, size=15):
        items_len = len(payloads)
        max_workers = min(items_len, size)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.script_handler, item) for item in payloads}
            completed_futures = concurrent.futures.as_completed(futures)
            for n, future in enumerate(completed_futures, 1):
                yield future.result()
