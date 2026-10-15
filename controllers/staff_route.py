from app import app
from flask import render_template,request,url_for,redirect,session,flash,abort
from flask_login import login_user, logout_user, login_required ,current_user
from controllers.model import User,Staff,Beneficiary,Donation,Attendance
from controllers.database import db
from datetime import datetime ,date
from functools import wraps

def staff_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if not current_user.is_authenticated:
            abort(401)

        if current_user.is_admin:
            abort(403)

        return f(*args, **kwargs)

    return decorated_function

@app.route('/staff/dashboard/<int:staff_id>')
@login_required
@staff_required
def staff_dashboard(staff_id):

    staff = Staff.query.get_or_404(staff_id)

    total_beneficiaries = Beneficiary.query.count()

    active_beneficiaries = Beneficiary.query.filter_by(
        status='Active'
    ).count()

    return render_template(
        'staff_dashboard.html',
        staff=staff,
        total_beneficiaries=total_beneficiaries,
        active_beneficiaries=active_beneficiaries
    )
    

@app.route('/staff-attendance')
@login_required
@staff_required
def staff_attendance():

    today = date.today()

    staffs = Staff.query.filter_by(status="Active").all()

    attendance_data = []

    for staff in staffs:

        attendance = Attendance.query.filter_by(
            staff_id=staff.id,
            date=today
        ).first()

        attendance_data.append({
            "staff": staff,
            "attendance": attendance
        })

    return render_template(
        "staff_attendance_list.html",
        attendance_data=attendance_data,
        today=today
    )

@app.route('/mark-attendance/<int:staff_id>')
@login_required
@staff_required
def mark_attendance(staff_id):

    today = date.today()

    attendance = Attendance.query.filter_by(
        staff_id=staff_id,
        date=today
    ).first()

    # Morning Check In
    if attendance is None:

        attendance = Attendance(
            staff_id=staff_id,
            date=today,
            status="Present",
            check_in=datetime.now().time()
        )

        db.session.add(attendance)
        db.session.commit()

    # Evening Check Out
    elif attendance.check_out is None:

        attendance.check_out = datetime.now().time()

        db.session.commit()

    return redirect(url_for("staff_attendance"))

@app.route("/attendance/close")
@login_required
@staff_required
def close_attendance():

    today = date.today()

    staffs = Staff.query.filter_by(status="Active").all()

    for staff in staffs:

        attendance = Attendance.query.filter_by(
            staff_id=staff.id,
            date=today
        ).first()

        if attendance is None:

            attendance = Attendance(
                staff_id=staff.id,
                date=today,
                status="Absent"
            )

            db.session.add(attendance)

    db.session.commit()

    flash("Attendance closed successfully.")

    return redirect(url_for("staff_attendance"))

@app.route('/my-profile')
@login_required
@staff_required
def my_profile():

    staff = current_user.staff

    return render_template(
        'my_profile.html',
        staff=staff
    )


@app.route('/beneficiary/add', methods=['GET', 'POST'])
@login_required
@staff_required
def add_beneficiary():

    if request.method == 'POST':

        # Generate Beneficiary ID
        last_beneficiary = Beneficiary.query.order_by(
            Beneficiary.id.desc()
        ).first()

        if last_beneficiary:
            next_no = last_beneficiary.id + 1
        else:
            next_no = 1

        beneficiary_code = f"BE{next_no:04d}"
        beneficiary_category=request.form.get(
                'beneficiary_category'
            )

        if beneficiary_category == 'Student':
                status='INActive'
        else:
             status ='Active'

        beneficiary = Beneficiary(

            beneficiary_id=beneficiary_code,

            name=request.form.get('name'),

            dob=datetime.strptime(
                request.form.get('dob'),
                '%Y-%m-%d'
            ).date(),

            beneficiary_category=beneficiary_category,

            gender=request.form.get('gender'),

            category=request.form.get('category'),

            caste=request.form.get('caste'),

            email=request.form.get('email'),

            phone=request.form.get('phone'),

            proof_id=request.form.get('proof_id'),

            id_no=request.form.get('id_no'),

            blood_group=request.form.get('blood_group'),

            pincode=request.form.get('pincode'),

            village=request.form.get('village'),

            address=request.form.get('address'),

            guardian_name=request.form.get(
                'guardian_name'
            ),

            guardian_relation=request.form.get(
                'guardian_relation'
            ),

            monthly_fee=request.form.get(
                'monthly_fee'
            ),

            remarks=request.form.get(
                'remarks'
            ),

            admission_date=date.today(),

            status = status


        )

        db.session.add(beneficiary)
        db.session.commit()

        flash(
            f"Beneficiary {beneficiary_code} admitted successfully",
            "success"
        )

        return redirect(url_for('staff_dashboard',staff_id=current_user.staff.id))

    return render_template(
        'add_beneficiary.html'
    )

@app.route('/students')
@login_required
@staff_required
def student_list():

    students = Beneficiary.query.filter_by(
        beneficiary_category="Student"
    ).all()

    return render_template(
        'student_list.html',
        students=students
    )

@app.route('/staffbeneficiaries')
@login_required
@staff_required
def staff_beneficiary():

    beneficiaries = Beneficiary.query.filter(
        Beneficiary.beneficiary_category != "Student"
    ).all()

    return render_template(
        'beneficiary_list.html',
        beneficiaries=beneficiaries
    )

@app.route('/beneficiary/edit/<int:beneficiary_id>', methods=['GET', 'POST'])
@login_required
@staff_required
def edit_beneficiary(beneficiary_id):
    print("ben")

    beneficiary = Beneficiary.query.get_or_404(beneficiary_id)

    if request.method == 'POST':

        beneficiary.name = request.form.get('name')

        beneficiary.dob = datetime.strptime(
            request.form.get('dob'),
            "%Y-%m-%d"
        ).date()

        beneficiary.beneficiary_category = request.form.get('beneficiary_category')

        beneficiary.gender = request.form.get('gender')

        beneficiary.category = request.form.get('category')

        beneficiary.caste = request.form.get('caste')

        beneficiary.email = request.form.get('email')

        beneficiary.phone = request.form.get('phone')

        beneficiary.proof_id = request.form.get('proof_id')

        beneficiary.id_no = request.form.get('id_no')

        beneficiary.blood_group = request.form.get('blood_group')

        beneficiary.pincode = request.form.get('pincode')

        beneficiary.village = request.form.get('village')

        beneficiary.address = request.form.get('address')

        beneficiary.guardian_name = request.form.get('guardian_name')

        beneficiary.guardian_relation = request.form.get('guardian_relation')

        beneficiary.monthly_fee = request.form.get('monthly_fee')

        beneficiary.status = request.form.get('status')

        beneficiary.remarks = request.form.get('remarks')

        completion_date = request.form.get('completion_date')

        beneficiary.completion_date = datetime.strptime(
            completion_date,
            "%Y-%m-%d"
        ).date() if completion_date else None

        db.session.commit()

        flash("Beneficiary updated successfully.", "success")

        if beneficiary.beneficiary_category != 'Student':
            return redirect(url_for('staff_beneficiary'))
        else:
            return redirect(url_for('student_list'))


    return render_template(
        "staff_edit_beneficiary.html",
        beneficiary=beneficiary
    )

@app.route("/beneficiary/view/<int:beneficiary_id>")
@login_required
@staff_required
def view_beneficiary(beneficiary_id):

    beneficiary = Beneficiary.query.get_or_404(beneficiary_id)

    return render_template(
        "staff_view_beneficiary.html",
        beneficiary=beneficiary
    )