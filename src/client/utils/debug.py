"""Helper class to see the camera feed with annotations"""
import cv2
from .image_transform import scale_to
from ..config import config

class Debugger:
    def __init__(self, enabled=False):
        self.enabled = enabled
        self.show = True
        self.x = 640
        self.y = 360
        self.annotations = {}
        self.images = {
            'camera': {
                'key': ord('1'),
                'image': None,
            },
            'threshold': {
                'key': ord('2'),
                'image': None,
            }
        }
        self.current_image_key = 'camera'
        self.variables = {}
        self.show_variables = True

    def set_enabled(self, enabled):
        self.enabled = enabled

    def set_window_size(self, x, y):
        self.x = x
        self.y = y

    def _draw_labels(self, image):
        for annotation in self.annotations:
            annotation_rect = self.annotations.get(annotation)
            cv2.rectangle(
                image,
                (annotation_rect.get('x'), annotation_rect.get('y')),
                (annotation_rect.get('x') + annotation_rect.get('w'),
                 annotation_rect.get('y') + annotation_rect.get('h')),
                (255, 0, 255),  # bgr
                2
            )
            cv2.putText(
                image,
                annotation,
                (annotation_rect.get('x'), annotation_rect.get('y')),
                config.get_global_cv2_font(),
                1.5,
                (255, 0, 255),
                2
            )

        return image

    def update_image(self, image, tag):
        # Main debug window handler
        if self.enabled and self.show:
            self.images[tag]['image'] = self._draw_labels(image)

        key = cv2.waitKey(1)
        for k in self.images:
            if self.images.get(k).get('key') == key:
                self.current_image_key = k

        # Variables list
        if self.show_variables:
            line_spacing = 50
            for key in self.variables:
                text = f'{key}: {self.variables.get(key)}'
                cv2.putText(
                    self.images.get(self.current_image_key).get('image'),
                    text,
                    (50, line_spacing),
                    # make a global config object
                    config.get_global_cv2_font(),
                    1.5,
                    (255, 0, 255),
                    2
                )
                line_spacing += 50

        cv2.imshow('Debug', scale_to(self.images.get(self.current_image_key).get('image'), self.x, self.y))
        if key == 27:
            # ESC
            self.destroy()
        elif key == ord('d'):
            # d key - debug toggle
            self.show = not self.show
        elif key == ord('v'):
            # v key - variable list toggle
            self.show_variables = not self.show_variables

        # TODO this seems to crash on ESC
        is_open = cv2.getWindowProperty('Debug', cv2.WND_PROP_VISIBLE)
        if not self.show and not is_open:
            cv2.destroyWindow('Debug')

    def update_annotation(self, label, anchor, size):
        x, y = anchor
        w, h = size
        self.annotations[label] = {
            'x': int(x),
            'y': int(y),
            'w': int(w),
            'h': int(h)
        }

    def add_temporary_annotation(self, image_key, anchor, size, color=(255, 0, 0)):
        x, y = anchor
        w, h = size
        cv2.rectangle(
            self.images.get(image_key).get('image'),
            (int(x), int(y)),
            (int(w), int(h)),
            color,  # bgr
            2
        )

    def update_variables(self, key, value):
        self.variables[key] = value

    def destroy(self):
        cv2.destroyAllWindows()


debugger = Debugger()
