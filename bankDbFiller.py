from bankAppConfig import *
from bankAppModels import Payment
from datetime import datetime

with app.app_context():
    db.create_all() #Tworzy się baza danych - na podstawie wszystkich modeli
    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(table.delete())  ####Kasowanie poprzednich rekordów z bazy dancyh
    db.session.commit()

    payments = [
        (50, 'paid_cb', 'client_cb', False),
        (75, 'paid_cb', 'client_cb', True)

    ]
    for payment in payments:
        db.session.add(Payment(amount=payment[0], paid_callback=payment[1], client_callback=payment[2], paid=payment[3]))
        db.session.commit()



    print(Payment.query.all())
