# from datetime import datetime
# import sqlalchemy
#
# # Текущее время в UTC
# utc_now = datetime.utcnow()
# print(f"Текущее время UTC: {utc_now}")
# print(sqlalchemy.__version__)

# a = [1, 2]
# b = a.copy()
#
# print(id(a), id(b))
# print(id(a[0]), id(b[0]))

def func(*args, **kwargs):
    print(args)
    print(kwargs)

func('a', 1, x=7, y='go')
