from datetime import datetime
import sqlalchemy

# Текущее время в UTC
utc_now = datetime.utcnow()
print(f"Текущее время UTC: {utc_now}")
print(sqlalchemy.__version__)