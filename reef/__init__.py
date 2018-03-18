from flask import Flask

app = Flask(__name__)
app.config.from_object('websiteconfig')

from reef import utils

from model import *

from reef import routes
from reef import errorhandlers