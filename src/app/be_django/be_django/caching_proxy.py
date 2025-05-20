class SearchEngineProxy:
    def __init__(self, real_search_func):
        self.real_search_func = real_search_func
        self.cache = {}

    def search(self, query, exact_match, json_format):
        key = (query, exact_match, json_format)
        if key in self.cache:
            print("Cache hit:", key)
            return self.cache[key]

        print("Cache miss:", key)
        result = self.real_search_func(query, exact_match, json_format)
        self.cache[key] = result
        return result