from flask import Flask
app = Flask(__name__)
import codeitsuisse.routes.square
import codeitsuisse.routes.optopt
import codeitsuisse.routes.asteroid
import codeitsuisse.routes.parasite
import codeitsuisse.routes.tictactoe
import codeitsuisse.routes.stonks
import codeitsuisse.routes.stockhunter
import codeitsuisse.routes.quoridor
import codeitsuisse.routes.cipher
import codeitsuisse.routes.decode