from sqlalchemy_serializer import SerializerMixin
from qrodizio.ext.database import db


class TableSession(db.Model, SerializerMixin):
    __tablename__ = "tables_sessions"
    serialize_rules = ("-demands",)

    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, default=db.func.now())
    url = db.Column(db.String(80), unique=True, nullable=False)
    demands = db.relationship("Demand")
    closed = db.Column(db.Boolean, default=False)
    table_id = db.Column(
        db.Integer, db.ForeignKey("customer_tables.id"), nullable=False
    )
    table = db.relationship("CustomerTable", back_populates="sessions")

    def create(self):
        db.session.add(self)
        db.session.commit()

        return self


class CustomerTable(db.Model, SerializerMixin):
    __tablename__ = "customer_tables"
    serialize_rules = ("-sessions",)

    id = db.Column(db.Integer, primary_key=True)
    qrcode = db.Column(db.String(255), unique=True, nullable=False)
    identifier = db.Column(db.String(80), unique=True, nullable=False)
    sessions = db.relationship("TableSession")

    def create(self):
        db.session.add(self)
        db.session.commit()

        return self
