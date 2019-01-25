# -*- coding: utf-8 -*-
import logging

def outPrint():
    print "hello"
    logger = logging.getLogger("django")
    logger.info("hello")
