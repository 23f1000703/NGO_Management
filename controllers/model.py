from controllers.database import db 
from datetime import datetime
from flask_login import UserMixin

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50),unique=True,nullable=False)

    email = db.Column(db.String(120), unique=True,nullable=False)
    password = db.Column(db.String(255),nullable=False)
    email_verified = db.Column(db.Boolean,default=False)
    is_admin=db.Column(db.Boolean,default=False)
    staff = db.relationship( 'Staff', back_populates='user', uselist=False, cascade='all, delete-orphan' )

class Beneficiary(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    beneficiary_id = db.Column(db.String(20), unique=True)

    name = db.Column(db.String(100),nullable=False)
    dob = db.Column(db.Date,nullable=False)
    beneficiary_category = db.Column(db.String(150),nullable=False)

    gender = db.Column(db.String(20),nullable=False)
    category = db.Column(db.String(50),nullable=False)
    caste = db.Column(db.String(50))
    email = db.Column(db.String(150))
    phone = db.Column(db.String(15),nullable=False)
    proof_id = db.Column(db.String(20),nullable=False)
    id_no = db.Column(db.String(50),nullable=False)
    blood_group = db.Column(db.String(10),nullable =False)
    pincode = db.Column(db.String(100),nullable=False)
    village = db.Column(db.String(100),nullable=False)
    address = db.Column(db.Text,nullable=False)

    guardian_name = db.Column(db.String(100))
    guardian_relation = db.Column(db.String(50))

    admission_date = db.Column(db.Date)
    completion_date = db.Column(db.Date)
    monthly_fee = db.Column(db.String(10))
    status = db.Column(db.String(20), default='InActive')

    remarks = db.Column(db.Text)
    documents = db.relationship('Document',back_populates='beneficiary',cascade='all, delete-orphan')
    donations = db.relationship('Donation',back_populates='beneficiary',cascade='all, delete-orphan')

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column( db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False )


    name = db.Column(db.String(100),nullable=False)
    role = db.Column(db.String(100),nullable=False)

    department = db.Column(db.String(100))

    phone = db.Column(db.String(15),nullable=False)
    proof_id = db.Column(db.String(120),nullable=False)
    id_num = db.Column(db.String(50),nullable=False)
    dob = db.Column(db.Date,nullable=False) 
    blood_group = db.Column(db.String(10),nullable=False)
    salary = db.Column(db.Float)
    gender = db.Column(db.String(10),nullable= False)

    joining_date = db.Column(db.Date,nullable=False)
    completion_date = db.Column(db.Date)
    address = db.Column(db.String(250),nullable=False)
    state = db.Column(db.String(50),nullable=False)
    nationality = db.Column(db.String(50),nullable=False)
    pincode = db.Column(db.String(100),nullable=False)

    status = db.Column(db.String(20),default="Active")
    user = db.relationship( 'User', back_populates='staff' )

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    staff_id = db.Column(db.Integer,db.ForeignKey('staff.id'))

    date = db.Column(db.Date)

    status = db.Column(db.String(20))
    # Present, Absent, Leave

    check_in = db.Column(db.Time)
    check_out = db.Column(db.Time)

    staff = db.relationship('Staff',backref='attendance_records')
    __table_args__ = (db.UniqueConstraint('staff_id','date',name='unique_staff_attendance'),)

class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    beneficiary_id = db.Column(db.Integer,db.ForeignKey('beneficiary.id'))

    donor_name = db.Column(db.String(100),nullable=False)

    donor_phone = db.Column(db.String(100))
    donor_email = db.Column(db.String(100))
    dob = db.Column(db.Date) 
    proof_id = db.Column(db.String(150),nullable=False)
    id_no = db.Column(db.String(50),nullable=False)
    address = db.Column(db.String(200),nullable=False)

    amount = db.Column(db.Float)

    donation_type = db.Column(db.String(50))

    purpose = db.Column(db.String(100))

    donation_date = db.Column(db.Date)

    remarks = db.Column(db.Text)
    beneficiary = db.relationship('Beneficiary',back_populates='donations')

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    voucher_no = db.Column(db.String(20))

    payee = db.Column(db.String(100))

    category = db.Column(db.String(100))

    amount = db.Column(db.Float)

    payment_mode = db.Column(db.String(50))

    payment_date = db.Column(db.Date)
    
    remarks = db.Column(db.Text)

    donation_id = db.Column(db.Integer,db.ForeignKey('donation.id'),nullable=True)

    staff_id = db.Column(db.Integer,db.ForeignKey('staff.id'),nullable=True)

    beneficiary_id = db.Column(db.Integer,db.ForeignKey('beneficiary.id'),nullable=True)

    status = db.Column(db.String(20),default='Completed')

    donation = db.relationship('Donation',backref='payments')

    staff = db.relationship('Staff',backref='payments')

    beneficiary = db.relationship('Beneficiary',backref='payments')


class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200))

    due_date = db.Column(db.Date)

    priority = db.Column(db.String(20))

    department = db.Column(db.String(100))

    notes = db.Column(db.Text)

    completed = db.Column(db.Boolean,default=False)
    created_at = db.Column( db.DateTime, default=datetime.utcnow )

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    beneficiary_id = db.Column(db.Integer,db.ForeignKey('beneficiary.id'))

    document_name = db.Column(db.String(100))
    file_path = db.Column(db.String(255))
    uploaded_at = db.Column( db.DateTime, default=datetime.utcnow ) 
    beneficiary = db.relationship( 'Beneficiary', back_populates='documents' )
