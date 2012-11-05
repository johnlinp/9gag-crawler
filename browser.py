# -*- coding: utf-8 -*-

import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time

class Browser:
    def __init__(self):
        self._browser = webdriver.Firefox()

