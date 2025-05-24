from .widget_interface import Widget

class LogAnalyzerWidget(Widget):
    def should_activate(self, context):
        results = context.get('results', [])
        total = len(results)
        if total == 0:
            return False
        threshold = total / 2
        count = 0
        for item in results:
            if item['name'].lower().endswith('.log'):
                count += 1
                if count > threshold:
                    return True
        return False

    def render_payload(self, context):
        return {
            'widget_id': 'log_analyzer',
            'title': 'Analyze Logs',
            'message': 'The results contain many log files. You can analyze their contents here.',
            'action_url': '/logs',
        }