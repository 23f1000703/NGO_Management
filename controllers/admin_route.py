from app import app
from flask import render_template,request,url_for,redirect,session , abort,flash
from flask_login import login_user, logout_user, login_required,current_user
from controllers.model import User,Staff,Beneficiary,Donation,Attendance,Payment
from controllers.database import db
from datetime import datetime,date
from calendar import monthrange
from sqlalchemy import or_
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

def admin_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if not current_user.is_authenticated:
            abort(401)

        if not current_user.is_admin:
            abort(403)

        return f(*args, **kwargs)

    return decorated_function

@app.route('/admin')
@login_required
@admin_required
def admin():

    total_beneficiary = Beneficiary.query.count()

    active_beneficiary = Beneficiary.query.filter_by(
        status="Active"
    ).count()

    total_staff = Staff.query.count()

    total_donation = db.session.query(
        db.func.sum(Donation.amount)
    ).scalar() or 0

    recent_beneficiaries = Beneficiary.query\
        .order_by(
            Beneficiary.admission_date.desc()
        )\
        .limit(5)\
        .all()

    return render_template(
        "admin_Dashboard.html",
        total_beneficiary=total_beneficiary,
        active_beneficiary=active_beneficiary,
        total_staff=total_staff,
        total_donation=total_donation,
        recent_beneficiaries=recent_beneficiaries
    )

@app.route('/adminbeneficiary')
@admin_required
@login_required
def admin_beneficiary():
    search = request.args.get("search", "")
    query = Beneficiary.query.filter(
        Beneficiary.beneficiary_category != "Student")
    if search:

        query = query.filter(
            or_(
                Beneficiary.beneficiary_id.ilike(f"%{search}%"),
                Beneficiary.name.ilike(f"%{search}%"),
                Beneficiary.phone.ilike(f"%{search}%"),
                Beneficiary.email.ilike(f"%{search}%"),
                Beneficiary.category.ilike(f"%{search}%")
            )
        )

    beneficiaries = query.all()
    return render_template('beneficiary.html',beneficiaries=beneficiaries)

@app.route('/adminstudent')
@login_required
def admin_student():
    search = request.args.get("search", "")
    query = Beneficiary.query.filter_by(
        beneficiary_category="Student")
    if search:

        query = query.filter(
            or_(
                Beneficiary.beneficiary_id.ilike(f"%{search}%"),
                Beneficiary.name.ilike(f"%{search}%"),
                Beneficiary.phone.ilike(f"%{search}%"),
                Beneficiary.email.ilike(f"%{search}%"),
                Beneficiary.category.ilike(f"%{search}%")
            )
        )

    students = query.all()
    return render_template('admin_student.html',students=students)



@app.route('/staff')
@admin_required
@login_required
def staff_list():
    search = request.args.get("search", "").strip()

    query = Staff.query

    if search:
        total_staff = query.filter(
            or_(
                Staff.name.ilike(f"%{search}%"),
                Staff.id.ilike(f"%{search}%"),
                Staff.role.ilike(f"%{search}%")
            )
        )
    else:
        total_staff = Staff.query.all()

    return render_template(
        'staff_list.html',
        staffs=total_staff
    )

    

@app.route("/staff/add", methods=['GET', 'POST'])
@admin_required
@login_required
def add_staff():

 if request.method == 'POST':

    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    name = request.form.get('name')
    role = request.form.get('role')
    department = request.form.get('department')
    phone = request.form.get('phone')
    blood_group =request.form.get('blood_group')
    dob =request.form.get('dob')
    proof_id = request.form.get('proof_id')
    id_num = request.form.get('id_num')
    gender =request.form.get('gender')
    pincode = request.form.get('pincode')
    state = request.form.get('state')
    nationality = request.form.get('nationality')
    address = request.form.get('address')

    salary = request.form.get('salary')

    joining_date = request.form.get('joining_date')

    existing_user = User.query.filter(
        (User.username == username) |
        (User.email == email)
    ).first()

    if existing_user:
        return "Username or Email already exists"

    user = User(
        username=username,
        email=email,
        password=generate_password_hash(password)
    )

    db.session.add(user)
    db.session.flush()

    staff = Staff(
        user_id=user.id,
        name=name,
        role=role,
        department=department,
        phone=phone,
        proof_id=proof_id,
        blood_group = blood_group,
        id_num=id_num,
        gender = gender,
        dob=datetime.strptime(
            dob,
            "%Y-%m-%d"
        ).date() if dob else None,
        state=state,
        nationality=nationality,
        pincode=pincode,
        address=address,
        salary=float(salary) if salary else None,
        joining_date=datetime.strptime(
            joining_date,
            "%Y-%m-%d"
        ).date() if joining_date else None
    )

    db.session.add(staff)

    db.session.commit()

    return redirect(url_for('staff_list'))

 return render_template("add_staff.html")

@app.route("/staff/edit/<int:staff_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_staff(staff_id):

    staff = Staff.query.get_or_404(staff_id)
    user = staff.user

    if request.method == "POST":

        user.username = request.form.get("username")
        user.email = request.form.get("email")

        password = request.form.get("password")
        if password:
            user.password = generate_password_hash(password)

        staff.name = request.form.get("name")
        staff.role = request.form.get("role")
        staff.department = request.form.get("department")
        staff.phone = request.form.get("phone")
        staff.proof_id = request.form.get("proof_id")
        staff.id_num = request.form.get("id_num")
        staff.gender = request.form.get("gender")
        staff.blood_group = request.form.get("blood_group")
        staff.state = request.form.get("state")
        staff.nationality = request.form.get("nationality")
        staff.address = request.form.get("address")
        staff.pincode = request.form.get("pincode")
        staff.status = request.form.get("status")

        salary = request.form.get("salary")
        staff.salary = float(salary) if salary else None

        dob = request.form.get("dob")
        staff.dob = datetime.strptime(
            dob, "%Y-%m-%d"
        ).date() if dob else None

        joining = request.form.get("joining_date")
        staff.joining_date = datetime.strptime(
            joining, "%Y-%m-%d"
        ).date() if joining else None

        completion = request.form.get("completion_date")
        staff.completion_date = datetime.strptime(
            completion, "%Y-%m-%d"
        ).date() if completion else None

        db.session.commit()

        flash("Staff updated successfully.", "success")
        return redirect(url_for("staff_list"))

    return render_template(
        "edit_staff.html",
        staff=staff,
        user=user
    )


@app.route('/staff/view/<int:staff_id>')
@admin_required
@login_required
def view_staff(staff_id):

    staff = Staff.query.get_or_404(staff_id)

    total_payment = db.session.query(
        db.func.sum(Payment.amount)
    ).filter(
        Payment.staff_id == staff.id
    ).scalar() or 0

    attendance_count = Attendance.query.filter_by(
        staff_id=staff.id,
        status='Present'
    ).count()

    return render_template(
        'view_staff.html',
        staff=staff,
        total_payment=total_payment,
        attendance_count=attendance_count
    )

@app.route('/donations')
@admin_required
@login_required
def donation_list():

    donations = Donation.query.order_by(
        Donation.donation_date.desc()
    ).all()

    total_amount = db.session.query(
        db.func.sum(Donation.amount)
    ).scalar() or 0

    return render_template(
        'donation_list.html',
        donations=donations,
        total_amount=total_amount
    )

@app.route('/donation/add', methods=['GET', 'POST'])
@admin_required
@login_required
def add_donation():

    if request.method == 'POST':

        donation = Donation(

            donor_name=request.form.get('donor_name'),
            donor_phone=request.form.get('donor_phone'),
            donor_email=request.form.get('donor_email'),

            dob=datetime.strptime(
                request.form.get('dob'),
                "%Y-%m-%d"
            ).date() if request.form.get('dob') else None,

            proof_id=request.form.get('proof_id'),
            id_no=request.form.get('id_no'),
            address=request.form.get('address'),

            amount=float(request.form.get('amount')),

            donation_type=request.form.get('donation_type'),

            purpose=request.form.get('purpose'),

            donation_date=datetime.strptime(
                request.form.get('donation_date'),
                "%Y-%m-%d"
            ).date(),

            remarks=request.form.get('remarks')

        )

        db.session.add(donation)
        db.session.commit()

        return redirect(url_for('donation_list'))

    return render_template('add_donation.html')



@app.route('/attendance')
@admin_required
@login_required
def attendance():

    today = date.today()

    total_staff = Staff.query.count()

    present_today = Attendance.query.filter_by(
        date=today,
        status='Present'
    ).count()


    leave_today = Attendance.query.filter_by(
        date=today,
        status='Leave'
    ).count()

    today_attendance = Attendance.query.filter_by(
        date=today
    ).all()

    attended_staff_ids = [
        a.staff_id for a in today_attendance
    ]

    if attended_staff_ids:
        missing_staff = Staff.query.filter(
            ~Staff.id.in_(attended_staff_ids)
        ).all()
    else:
        missing_staff = Staff.query.all()

    absent_today = len(missing_staff)

    month_start = date(
        today.year,
        today.month,
        1
    )

    month_end = date(
        today.year,
        today.month,
        monthrange(
            today.year,
            today.month
        )[1]
    )

    working_days = 0

    for day in range(1, month_end.day + 1):

        weekday = date(
            today.year,
            today.month,
            day
        ).weekday()

        if weekday != 6:
            working_days += 1

    staff_report = []

    staffs = Staff.query.all()

    for staff in staffs:

        present = Attendance.query.filter(
            Attendance.staff_id == staff.id,
            Attendance.status == "Present",
        ).count()
        pres = Attendance.query.filter(
            Attendance.staff_id == staff.id,
            Attendance.check_in.is_not(None),
            Attendance.check_out != "NULL"
        ).count()
        print(pres)

        leave = Attendance.query.filter(
            Attendance.staff_id == staff.id,
            Attendance.status == "Leave",
            Attendance.date >= month_start,
            Attendance.date <= month_end
        ).count()

        absent = Attendance.query.filter(
            Attendance.staff_id == staff.id,
            Attendance.status == "Absent",
            Attendance.date >= month_start,
            Attendance.date <= month_end
        ).count()

        attendance_percent = 0

        if working_days > 0:
            attendance_percent = round(
                (pres / working_days) * 100,
                2
            )

        staff_report.append({
            "name": staff.name,
            "role": staff.role,
            "department": staff.department,
            "present": present,
            "leave": leave,
            "absent": absent,
            "attendance_percent": attendance_percent
        })

    return render_template(
        'attendance.html',
        total_staff=total_staff,
        present_today=present_today,
        absent_today=absent_today,
        leave_today=leave_today,
        today_attendance=today_attendance,
        missing_staff=missing_staff,
        staff_report=staff_report
    )

@app.route('/reminders')
@admin_required
@login_required
def reminder_list():

    today = date.today()

    new_admissions = Beneficiary.query.filter(
        Beneficiary.admission_date == today
    ).count()


    today_attendance = Attendance.query.filter_by(
        date=today,
        status = 'Present'
    ).all()
    total_attendance = len(today_attendance)

    attended_staff_ids = [
        a.staff_id for a in today_attendance
    ]

    if attended_staff_ids:
        missing_staff = Staff.query.filter(
            ~Staff.id.in_(attended_staff_ids)
        ).all()
    else:
        missing_staff = Staff.query.all()

    absent_staff = len(missing_staff)

    donations_month = Donation.query.count()

    pending_payments = Payment.query.filter_by(
        status='Pending'
    ).count()

    fee_pending = 0
    completion_due = 0

    return render_template(
        'reminder_list.html',
        new_admissions=new_admissions,
        total_attendance=total_attendance,
        absent_staff=absent_staff,
        donations_month=donations_month,
        pending_payments=pending_payments,
        fee_pending=fee_pending,
        completion_due=completion_due
    )
@app.route("/adminbeneficiary/view/<int:beneficiary_id>")
@login_required
@admin_required
def adminview_beneficiary(beneficiary_id):

    beneficiary = Beneficiary.query.get_or_404(beneficiary_id)

    return render_template(
        "admin_view_beneficiary.html",
        beneficiary=beneficiary
    )