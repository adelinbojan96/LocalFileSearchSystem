from .image_analyzer import ImageGalleryWidget
from .log_analyzer  import LogAnalyzerWidget
from .docs_analyzer import DocumentPreviewWidget

class WidgetFactory:
    def __init__(self):
        self._registry = [
            ImageGalleryWidget(),
            LogAnalyzerWidget(),
            DocumentPreviewWidget(),
        ]

    def create_widgets(self, context: dict) -> list[dict]:
        active = []
        for widget in self._registry:
            if widget.should_activate(context):
                active.append(widget.render_payload(context))
        return active

widget_factory = WidgetFactory()
