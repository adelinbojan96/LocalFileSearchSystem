from .widget_interface import Widget

class ImageGalleryWidget(Widget):
    def should_activate(self, context):
        q = context.get('query', '').lower()
        if 'image' in q:
            return True

        results = context.get('results', [])
        total = len(results)
        if total == 0:
            return False

        img_extensions = ('.jpg', '.jpeg', '.png', '.gif')
        count = 0

        for item in results:
            name = item.get('name', '').lower()
            if name.endswith(img_extensions):
                count += 1
                if count > total / 2:
                    return True
        return False

    def render_payload(self, context):
        return {
            'widget_id': 'image_gallery',
            'title': 'View Picture names',
            'message': 'This search contains many images. You can view their paths.',
            'action_url': '/images',
        }