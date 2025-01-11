# services/__init__.py
from .financial import FinancialService
from .sentiment import SentimentService
from .user import UserService

# Create instances of services
financial = FinancialService()
sentiment = SentimentService()
user = UserService()