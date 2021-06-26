# from src.db.models import Book
#
#
# def test_is_ok(db_session):
#     data = [('name', None, 1234), ('name', None, 1234)]
#     objects = [
#         Book(name=name, author_id=None, year=year)
#         for name, author, year in data
#     ]
#     a = db_session.bulk_save_objects(objects)
#
#     db_session.commit()
#     b = db_session.query(Book).all()
#     print(b)
#     assert False
