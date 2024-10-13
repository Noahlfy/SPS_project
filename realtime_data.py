# Envoie des données en temps réel

from flask import Flask, render_template
from flask_socketio import SocketIO
import pandas as pd
import time
import json