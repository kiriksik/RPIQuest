from enum import IntFlag


class WindowFlags(IntFlag):
    """
    Bitmap flags for window options.
    """
    WN_CONTROLS = 1     # no minimize/maximize
    WN_DRAGABLE = 2     # no dragging
    WN_RESIZABLE = 4    # no resizing
