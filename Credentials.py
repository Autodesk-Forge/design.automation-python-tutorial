#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ApiAuth Container class"""

class Credentials():
    clientId = None
    clientSecret = None
    def __init__(self, **kwords):
        self.clientId = kwords.get('clientId', None)
        self.clientSecret = kwords.get('clientSecret', None)
        if None in [self.clientId, self.clientSecret]:
            raise ValueError('clientId and clientSecret must be defined')