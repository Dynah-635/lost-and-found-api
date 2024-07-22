from app.extensions import db, bcrypt
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    lost_reports = db.relationship('LostReport', backref='user', lazy=True)
    found_reports = db.relationship('FoundReport', backref='user', lazy=True)
    claims = db.relationship('Claim', backref='user', lazy=True)  
    rewards_received = db.relationship('Reward', foreign_keys='Reward.receiver_id', backref='receiver', lazy=True)
    rewards_paid = db.relationship('Reward', foreign_keys='Reward.payer_id', backref='payer', lazy=True)
    role = db.Column(db.String(50), default='user')  

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'