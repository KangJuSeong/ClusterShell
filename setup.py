from setuptools import setup

setup(
        name='clsh',
        version='0.1',
        py_module=['clsh'],
        install_requires=[
                'Click',
            ],
        entry_points='''
            [console_scripts]
            clsh=clsh:clsh
        '''
        )
