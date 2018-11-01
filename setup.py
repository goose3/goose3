from setuptools import setup, find_packages

setup(
    name='vklabs.goose3',
    version='0.0.9',
    python_requires='>=3.6',
    packages=find_packages(exclude=['tests']),
    package_data={'vklabs.goose3': ['resources/images/*.txt', 'resources/text/*.txt']},
    install_requires=[
        'beautifulsoup4>=4.6.3',
        'certifi>=2018.10.15',
        'chardet>=3.0.4',
        'cssselect>=1.0.3',
        'idna>=2.7',
        'jieba>=0.39',
        'lxml>=4.2.5',
        'nltk>=3.3',
        'Pillow>=5.3.0',
        'python-dateutil>=2.7.3',
        'requests>=2.20.0',
        'six>=1.11.0',
        'urllib3>=1.24'
    ],
    setup_requires=['pytest-runner'],
    tests_require=[
        'flake8==3.6.0',
        'requests-mock==1.5.2',
    ],
    entry_points='''
    ''',
)
