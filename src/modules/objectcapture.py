"""A module for detecting in-game objects."""

from src.common import config, utils
import time
import os
import cv2
# import pygame
import threading
import numpy as np
import keyboard as kb


RANGES = (
    ((0, 245, 215), (10, 255, 255)),
)
other_filtered = utils.filter_color(cv2.imread('assets/other_template.png'), RANGES)
OTHER_TEMPLATE = cv2.cvtColor(other_filtered, cv2.COLOR_BGR2GRAY)

class ObjectCapture:
    """
    This class is responsible for capturing in-game events and updating the GUI.
    """

    def __init__(self):
        """initialize the capture class."""
        config.objectcapture = self
        self.frame = None
        self.ready = False
        self.thread = threading.Thread(target=self._main)
        self.thread.daemon = True

    def start(self):
        """Start the capture thread."""
        self.thread.start()

    def _main(self):
        """Main loop for the capture thread."""
        pass