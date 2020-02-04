from bankAppConfig import db



class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    paid_callback = db.Column(db.String(150), nullable=False)
    client_callback = db.Column(db.String(150), nullable=False)
    paid = db.Column(db.Boolean, nullable=False)


