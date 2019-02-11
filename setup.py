from setuptools import setup, find_packages

VERSION = '0.1.0'

# @see https://packaging.python.org/tutorials/packaging-projects/#creating-setup-py
with open("README.md", "r") as fh:
    long_description = fh.read()

# @see https://github.com/pypa/sampleproject/blob/master/setup.py
setup(
    name='now_playing_graph',
    version=VERSION,
    author='Maciej Brencz',
    author_email='maciej.brencz@gmail.com',
    license='MIT',
    description='Processes "now playing" data from internet radio player for Faroese Útvarp',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/macbre/now-playing-graph',
    packages=find_packages(),
    extras_require={
        'dev': [
            'coverage==4.5.1',
            'pylint==2.1.1',
            'pytest==3.9.3',
        ]
    },
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'render_graph=now_playing_graph.scripts.graph_json:main',
            'get_stats=now_playing_graph.scripts.get_stats:main'
        ],
    }
)
