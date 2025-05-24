from .widget_interface import Widget

class DocumentPreviewWidget(Widget):
    def should_activate(self, context):
        q = context.get('query', '').lower()
        for kw in ('text', 'application'):
            if kw in q:
                return True

        results = context.get('results', [])
        total = len(results)
        if total == 0:
            return False

        doc_extensions = ('.txt', '.md', '.rtf')
        count = 0

        for item in results:
            name = item.get('name', '').lower()
            if name.endswith(doc_extensions):
                count += 1
                if count > total / 2:
                    return True

        return False

    def render_payload(self, context):
        return {
            'widget_id': 'doc_preview',
            'title': 'Open in Document Viewer',
            'message': 'Most results are documents. You can preview them as text.',
            'action_url': '/docs',
        }