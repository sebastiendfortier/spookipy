# -*- coding: utf-8 -*-

def pytest_itemcollected(item):
    node = item.obj
    doc = str(node.__doc__.strip()) if node.__doc__ else str('')
    doc = doc.encode("ascii","replace")
    item._nodeid = ' : '.join([item._nodeid,str(doc)])
