from flask import Flask

app = Flask(__name__)

#  [ TO CIRCUMVENT `CIRCULAR IMPORT` ERROR ]
from VESTER_AI import routes
