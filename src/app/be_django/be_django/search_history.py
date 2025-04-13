import json, re

class SearchSubject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, search_data):
        for observer in self._observers:
            observer.update(search_data)

class SearchHistoryManager:
    def __init__(self):
        self.search_history = []
        self.load_history()

    def load_history(self):
        try:
            with open("report.json", "r") as f:
                self.search_history = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.search_history = []

    def update(self, search_data):
        self.search_history.append(search_data)
        self._save_to_file(search_data)

    def _save_to_file(self, data):
        with open("report.json", "w") as f:
            json.dump(self.search_history, f, indent=2)

    def get_popular_terms(self, limit=5):
        term_counts = {}
        for entry in self.search_history:
            terms = re.findall(r'\b\w+\b', entry.get('query', '').lower())
            for term in terms:
                term_counts[term] = term_counts.get(term, 0) + 1
        return sorted(term_counts.items(), key=lambda x: x[1], reverse=True)[:limit]

search_subject = SearchSubject()
history_manager = SearchHistoryManager()
search_subject.attach(history_manager)