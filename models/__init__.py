from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models here so they register
from .user import User
from .expense import Expense
