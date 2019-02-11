"""
A module containing command-line tool
"""
import logging

from os import path


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-20s %(levelname)-8s %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S"
)

# input file
INPUT_FILE = path.realpath(path.join(
    path.dirname(__file__),
    '../../data',
    'kvf.log.gz'
))
