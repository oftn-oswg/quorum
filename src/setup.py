#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup, find_packages


setup(
        name = "Quorum",
        version = "0.1",
        description = "A flexible proposal/voting workflow system for teams of people.",
        author = "Alice Bevan-McGregor and contributors",
        author_email = "alice@gothcandy.com",
        url = "http://oftn.org/",
        
        install_requires = ['WebCore < 2.0'],
        packages = find_packages(),
        
        zip_safe = False,
        include_package_data = True,
        package_data = {
                '': ['README.textile', 'LICENSE'],
                'quorum': ['templates/*', 'public/*']
            },
        
        paster_plugins = ['PasteScript', 'WebCore'],
    )
