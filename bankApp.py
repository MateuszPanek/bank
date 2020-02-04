from bankAppConfig import *
from bankAppModels import Payment
from flask import redirect
import requests


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/pay', methods=['POST'])
def pay():
    if request.json is None:
        return "Invalid request type", 404
    # Tworzymy płatność w bazie danych banku (rozpakowujemy poszczególne wartości do listy - możemy zrobić to bezpośrednio
    # linijkę niżej (zastępując amount=payment[0] zapisem amount=request.json['amount']
    # ostatnia wartość - False może zostać zdefiniowana jako default w bazie dancyh (patrz modele), tutaj jednak
    # dodajemy ją w momencie tworzenia rekordu
    payment = [request.json['amount'], request.json['paid_callback'], request.json['client_callback'], False]
    abc = Payment(amount=payment[0], paid_callback=payment[1], client_callback=payment[2], paid=payment[3])
    db.session.add(abc)
    db.session.commit()
    app.logger.info(abc.id)
    # Zapisujemy id obiektu abc (czyli naszej płatnośći pod zmienną id - oczywiście możemy od razu dodać ją do
    # formated stringa bez tworzenia dodatkowej zmiennej.
    id = abc.id
    # Przygotowujemy response który zostanie zwrócony naszej aplikacji PKP - patrz reservationControllers.buy_ticket
    # (odpowiedź trafia pod zmienną a)
    resp = {"redirect_to": f"http://127.0.0.1:5002/pay/{id}"}
    # Zwracamy odpowiedź z banku
    return resp


@app.route('/pay/<int:payment_id>', methods=['POST', 'GET'])
def mark_as_paid(payment_id):
    # Tutaj trafia nasz klient po przekierowaniu - w pierwszej kolejności wyciągamy konkretną płatność (po id) z bazy danych banku
    status = Payment.query.filter_by(id=payment_id).first()
    if status is None:
        return 'Payment not found'
    #zmieniamy status na True
    status.paid = True
    app.logger.info(f'payment_id:{status.id} amount: {status.amount} paid :{status.paid}')
    db.session.commit()
    # 'pod spodem' zwracamy paid callback czyli informację którą przygotowało PKP do zwrotki gdy płatność się powiedzie -
    # ta trafia do naszej reservation App pod /paid/<int:id>
    requests.post(url=status.paid_callback)
    # Client callback zostanie zwrócony jako przekierowanie - klient prosto z banku 'wyląduje' na stronie z biletem
    # patrz reservationApp ticket/<int:ticket_id>
    return redirect(status.client_callback)


if __name__ == '__main__':
    app.run(port=5002, debug=True)
