from flask import Flask
import logging
sw = Flask(__name__)
# This import has to be below the initialization of sw
from signageWebpage import routes
