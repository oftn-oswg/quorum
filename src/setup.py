#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup, find_packages


setup(
        name = "Project",
        version = "0.1",
        description = "",
        author = "Your Name Here",
        author_email = "you@example.com",
        url = "http://example.com/",
        
        install_requires = ['WebCore < 2.0'],
        packages = find_packages(),
        
        zip_safe = False,
        include_package_data = True,
        package_data = {
                '': ['README.textile', 'LICENSE'],
                'project': ['templates/*']
            },
        
        paster_plugins = ['PasteScript', 'WebCore'],
    )
