from flask import Flask, render_template, request,session,flash,url_for,redirect
import sqlite3
import pandas as pd
import datetime
app = Flask(__name__)
app.secret_key = '123' 

#-------------------------------------home-page----------------------------------------------------------------#

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/admin_dashboard")
def admin_dashboard():
    con = sqlite3.connect("spm_db.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM users_tb")
    total_staff = len(cur.fetchall()) 
    
    cur.execute("SELECT * FROM classes_tb")
    total_classes = len(cur.fetchall()) 
    return render_template("admin/admin_panel.html",total_staff=total_staff,total_classes=total_classes)


@app.route("/staff_dashboard")
def staff_dashboard():
    return render_template("staff/staff_panel.html")
    
   
@app.route("/student_dashboard")
def student_dashboard(): 
    return render_template("student/student_panel.html")
#---------------------------------------------------------------------------------------------------------------#

#---------------------------------login-process---------------------------------------------------------------#
#admin login
@app.route('/admin_login', methods=["POST", "GET"])
def admin_login():
    if request.method == "POST":
        try:
            con = sqlite3.connect("spm_db.db")
            cur = con.cursor()
                
            username = request.form.get('username')
            password = request.form.get('password')
            userid = request.form.get('userid')
            
            cur.execute("SELECT * FROM admin_tb WHERE username=? AND password=? and userid=?", (username, password,userid))
            data = cur.fetchall()
                
            if data:
                session['userid'] = int(userid)
                session['username'] = username
                cur.execute("SELECT * FROM users_tb")
                total_staff = len(cur.fetchall()) 
    
                cur.execute("SELECT * FROM classes_tb")
                total_classes = len(cur.fetchall()) 
                flash("Login Successful..!!","success")
                return render_template("admin/admin_panel.html",total_staff=total_staff,total_classes=total_classes)
                
            else:
                flash("Login Failed..!!","danger")
                return redirect(url_for('admin_login'))
                
        except Exception as e:
            flash(f"Error in Login: {str(e)}", "danger")
        finally:
            con.close()
    else:
        return render_template("admin/admin_login_form.html")
    

#staff login
@app.route('/staff_login', methods=["POST", "GET"])
def staff_login():
    if request.method == "POST":
        try:
            con = sqlite3.connect("spm_db.db")
            cur = con.cursor()
                
            username = request.form.get('username')
            password = request.form.get('password')
            userid = request.form.get('userid')
            
            cur.execute("SELECT * FROM users_tb WHERE username=? AND pass=? and userid=?", (username, password,userid))
            data = cur.fetchall()
                
            if data:
                session['userid'] = int(userid)
                session['username'] = username
                flash("Login Successful..!!","success")
                return render_template("staff/staff_panel.html") 
            else:
                flash("Login Failed..!!","danger")
                return redirect(url_for('staff_login'))
                
        except Exception as e:
            flash(f"Error in Login: {str(e)}", "danger")
        finally:
            con.close()
    else:
        return render_template("staff/staff_login_form.html")
    
    
#student login
@app.route("/student_login")
def student_login():
    flash("Login Successful..!!","success")
    return render_template("student/student_panel.html")

 
#----------------------------------------------------------------------------------------------------------------------------#



#-------------------------------------------admin-processes------------------------------------------------------------------#

#---------------------------------------department-view,insert,delete,update---------------------------------------------------------------------#
    
#insert department
@app.route("/insert_dept", methods=["POST","GET"])
def insert_dept():
    if request.method == "POST":
        
        deptid = request.form.get('deptid')
        deptname = request.form.get('deptname')
        
        if not deptid or not deptname:
            flash("Both values are required","danger")
            return redirect(url_for('insert_dept'))
        
        try:
            con = sqlite3.connect("spm_db.db")
            cur = con.cursor()
            cur.execute("INSERT INTO dept_tb (deptid, deptname) VALUES (?,?)", (deptid, deptname))
            con.commit()
            flash("Department Added Successfully!", "success")
            
        except sqlite3.IntegrityError:
            flash("Department or ID already exists!", "danger")
            
        except Exception as e:
            flash(f"Error in Insertion: {str(e)}", "danger")
            
        finally:
            con.close()
            return redirect(url_for('insert_dept'))
    else:
        return render_template("admin/dept_entry_form.html")  
    

#view all department
@app.route('/view_dept')
def view_dept():
    con = sqlite3.connect('spm_db.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM dept_tb")
    departments = cur.fetchall()
    con.close()
    return render_template('admin/view_dept.html', departments=departments)


#delete department
@app.route('/delete_dept/<int:deptid>')
def delete_dept(deptid):
    con = sqlite3.connect('spm_db.db')
    cursor = con.cursor()
    try:
        cursor.execute("DELETE FROM dept_tb WHERE deptid = ?", (deptid,))
        con.commit()
        flash("Department deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting department: {str(e)}", "danger")
    finally:
        con.close()
        return redirect(url_for('view_dept'))

#update department
@app.route("/update_dept_form/<int:deptid>/<string:deptname>",methods=["POST","GET"])
def update_dept_form(deptid,deptname):
    return render_template("admin/update_dept_form.html",deptid = deptid,deptname=deptname)


@app.route('/update_dept', methods=['GET', 'POST'])
def update_dept():
    deptid = request.form.get('deptid')
    new_deptname = request.form.get('deptname')
    if not deptid or not new_deptname:
        flash("both values are required","danger")
        return redirect(url_for('view_dept'))
            
    con = sqlite3.connect('spm_db.db')
    cur = con.cursor()
    
    try:    
        cur.execute("UPDATE dept_tb SET deptname = ? WHERE deptid = ?", (new_deptname, int(deptid)))
        con.commit()
        flash("Department Updated successfully!", "success")
    except Exception as e:
        flash(f"Error Updating department: {str(e)}", "danger")
    finally:
        con.close()
        return redirect(url_for('view_dept'))



#------------------------------------------------------------------------------------------------------------------------------------#




#-----------------------------------------staff-insert,view,delete,update------------------------------------------------#

# Insert staffs
@app.route("/insert_staff", methods=["POST","GET"])
def insert_staff():
    con = sqlite3.connect("spm_db.db")
    cur = con.cursor() 
    if request.method == "POST":
        userid = request.form.get('userid')
        username = request.form.get('username')
        dept = request.form.get('dept')
        password = request.form.get('password')
            
        if not userid or not username or not dept or not password:
            flash("All values are required","danger")
            return redirect(url_for('insert_staff'))
        try:    
            cur.execute("INSERT INTO users_tb (userid, username, dept, pass) VALUES (?, ?, ?, ?)",(userid, username, dept, password))
            con.commit()
            flash("Staff Added Successfully!", "success")
            
        except sqlite3.IntegrityError:
            flash("User ID already exists!", "danger") 
        except Exception as e:
            flash(f"Error in Insertion: {str(e)}", "danger")
        finally:
            con.close()
            return redirect(url_for('insert_staff'))
    else:
        cur.execute('SELECT deptname FROM dept_tb')
        data = cur.fetchall()
        departments = [row[0] for row in data] 
        con.close()
        return render_template("admin/staff_entry_form.html",departments=departments)
    

#view staff
@app.route('/view_staff')
def view_staff():
    con = sqlite3.connect('spm_db.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM users_tb")
    data = cur.fetchall()
    con.close()
    return render_template('admin/view_staff.html', data = data)


#delete staff
@app.route('/delete_staff/<int:userid>')
def delete_staff(userid):
    con = sqlite3.connect('spm_db.db')
    cursor = con.cursor()
    try:
        cursor.execute("DELETE FROM users_tb WHERE userid = ?", (userid,))
        con.commit()
        flash("Staff deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting Staff: {str(e)}", "danger")
    finally:
        con.close()
        return redirect(url_for('view_staff'))

#update staff
@app.route("/update_staff_form/<int:userid>/<string:username>/<string:dept>/<string:password>",methods=["POST","GET"])
def update_staff_form(userid,username,dept,password):
    con = sqlite3.connect("spm_db.db")
    cur = con.cursor()
    cur.execute('SELECT deptname FROM dept_tb')
    data = cur.fetchall()
    departments = [row[0] for row in data] 
    con.close()
    return render_template("admin/update_staff_form.html",userid = userid,username=username,dept=dept,password=password,departments=departments)


@app.route('/updat_staff', methods=['GET', 'POST'])
def updat_staff():
    userid = request.form.get('userid')
    new_username = request.form.get('username')
    new_password = request.form.get('password')
    new_dept    = request.form.get('dept')
    if not userid or not new_username or not new_password or not new_dept:
        flash("All values are required","danger")
        return redirect(url_for('view_staff'))  
        
    con = sqlite3.connect('spm_db.db')
    cur = con.cursor()
    try:
        cur.execute("UPDATE users_tb SET username = ?,dept = ?, pass=? WHERE userid =?", (new_username, new_dept,new_password,int(userid)))
        con.commit()
        flash("Staff Updated successfully!", "success")
    except Exception as e:
        flash(f"Error Updating Staff: {str(e)}", "danger")
    finally:
        con.close()
        return redirect(url_for('view_staff'))    
    
    
#-------------------------------------------------------------------------------------------------------------------------------------------------------#






#-------------------------------subject-insert,view,delete,update------------------------------------------#    
  
# Insert subject
@app.route("/insert_sub", methods=["POST","GET"])
def insert_sub():
    con = sqlite3.connect("spm_db.db")
    cur = con.cursor()    
    
    if request.method == "POST":
        subjectid = request.form.get('subid')
        subjectname = request.form.get('subname')
        dept = request.form.get('dept')
        year = request.form.get('year')
        semester = request.form.get('sem')
        selected_staffsid = request.form.getlist('staffsid')  
        
        if not subjectid or not subjectname or not dept or not year or not semester or not selected_staffsid :
            flash("All subject values are required", "danger")
            return redirect(url_for('insert_sub'))
            
        try:
            
            cur.execute("""
                INSERT INTO subjects_tb (subjectid, subjectname, dept, year, sem, staffsid) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (subjectid, subjectname, dept, year, semester, ",".join(selected_staffsid)))
            
            con.commit()
            flash("Subject Added Successfully..!!", "success")
            
        except sqlite3.IntegrityError:
            flash("Subject Name or Id already exists!", "danger") 
        except Exception as e:
            flash(f"Error in Insertion: {str(e)}", "danger")
        finally:
            con.close()
            return redirect(url_for('insert_sub'))
    else:
        cur.execute('SELECT deptname FROM dept_tb')
        departments = [row[0] for row in cur.fetchall()]
   
        cur.execute('SELECT userid, username FROM users_tb')
        staff_list = cur.fetchall()
        
        con.close()
        return render_template("admin/subject_entry_form.html", departments=departments,staff_list=staff_list)
        

#view subject
@app.route('/view_subject')
def view_subject():
    con = sqlite3.connect('spm_db.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM subjects_tb")
    data = cur.fetchall()
    con.close()
    return render_template('admin/view_subject.html', data = data)


#delete subject
@app.route('/delete_subject/<int:subjectid>')
def delete_subject(subjectid):
    con = sqlite3.connect('spm_db.db')
    cursor = con.cursor()
    try:
        cursor.execute("DELETE FROM subjects_tb WHERE subjectid = ?", (subjectid,))
        con.commit()
        flash("Subject deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting Subject: {str(e)}", "danger")
    finally:
        con.close()
        return redirect(url_for('view_subject'))

#update subject
@app.route("/update_subject_form/<int:subjectid>/<string:subjectname>/<string:dept>/<string:year>/<string:sem>",methods=["POST","GET"])
def update_subject_form(subjectid,subjectname,dept,year,sem):
    con = sqlite3.connect("spm_db.db")
    cur = con.cursor()
    cur.execute('SELECT deptname FROM dept_tb')
    data = cur.fetchall()
    departments = [row[0] for row in data] 

   
    cur.execute('SELECT userid, username FROM users_tb')
    staff_list = cur.fetchall()
    con.close()
    return render_template("admin/update_subject_form.html",subjectid = subjectid,subjectname=subjectname,dept=dept,year=year,sem=sem,departments=departments,staff_list=staff_list)


@app.route('/update_subject', methods=['GET', 'POST'])
def update_subject():
    subjectid = request.form.get('subid')
    new_subjectname = request.form.get('subname')
    new_dept = request.form.get('dept')
    new_year   = request.form.get('year')
    new_sem    = request.form.get('sem')
    selected_staffsid = request.form.getlist('staffsid')
    staffs_id = ",".join(selected_staffsid)
    
    if not subjectid or not new_subjectname or not new_dept  or not new_year or not new_sem or not staffs_id:
        flash("All values are required","danger")
        return redirect(url_for('view_subject'))  
    try:
        con = sqlite3.connect('spm_db.db')
        cur = con.cursor()
        cur.execute("UPDATE subjects_tb SET subjectname = ?,dept = ?,year=?, sem=?,staffsid =? WHERE subjectid =?", (new_subjectname, new_dept,new_year,new_sem,staffs_id,int(subjectid)))
        con.commit()
        flash("Subject Updated successfully!", "success")
    except Exception as e:
        flash(f"Error Updating Subject: {str(e)}", "danger")
    finally:
        con.close()
    return redirect(url_for('view_subject'))    

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#




#-------------------------------------------create-class-attendance------------------------------------------------------------------#

#create attendance
@app.route("/insert_class", methods=["GET", "POST"])
def insert_class():
    con = sqlite3.connect('spm_db.db')
    cur = con.cursor()
    if request.method == "POST":
        classid = request.form.get('classid')
        classname = request.form.get('classname')
        dept = request.form.get('dept')
        year = request.form.get('year')
        semester = request.form.get('sem')
        file = request.files.get('file')
        selected_staffsid = request.form.getlist('staffsid')
        
        if not all([classid, classname, dept, year, semester, selected_staffsid, file]):
            flash("All fields are required", "danger")
            return redirect(url_for('insert_class'))
            
        try:
            cur.execute("""
                INSERT INTO classes_tb (classid, classname, dept, year, sem, staffsid) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (classid, classname, dept, year, semester, ",".join(selected_staffsid)))
            
            create_table_query = f"CREATE TABLE IF NOT EXISTS {classname} (rollno INTEGER,name VARCHAR(50),p1 INTEGER,p2 INTEGER,p3 INTEGER,p4 INTEGER,p5 INTEGER,p6 INTEGER,p7 INTEGER,p8 INTEGE,present INTEGER, absent INTEGER,date VARCHAR(50),day VARCHAR(50))"
            cur.execute(create_table_query)
    
            create_table_time_schedule = f"""
            CREATE TABLE IF NOT EXISTS {classname}_timetable_schedule_tb (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                day TEXT NOT NULL,
                period INTEGER NOT NULL,
                subject TEXT NOT NULL,
                staff TEXT NOT NULL,
                UNIQUE(day, period)
            )"""
            
            cur.execute(create_table_time_schedule)
            con.commit()
            df = pd.read_excel(file)
            df = df[['rollno','name','email']] 
            df['dept'] = dept
            df['year'] = year
            df['classid'] = classid
            df['classname'] = classname
    
            df.to_sql("students_tb", con, if_exists='append', index=False)
            con.commit()
            
            flash("Class Added Successfully!", "success")
            
        except sqlite3.IntegrityError:
            flash("Class Name or Id already exists!", "danger") 
        except Exception as e:
            flash(f"Error in Insertion: {str(e)}", "danger")
        finally:
            con.close()
            return redirect(url_for('insert_class'))

    else:
        cur.execute('SELECT deptname FROM dept_tb')
        departments = [row[0] for row in cur.fetchall()]
    
        cur.execute('SELECT userid, username FROM users_tb')
        staff_list = cur.fetchall()
        con.close()
        return render_template("admin/class_entry_form.html", departments=departments,staff_list=staff_list)
    
#view subject
@app.route('/view_class')
def view_class():
    con = sqlite3.connect('spm_db.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM classes_tb")
    data = cur.fetchall()
    con.close()
    return render_template('admin/view_class.html', data = data)


#delete class
@app.route('/delete_class/<int:classid>/<string:classname>')
def delete_class(classid,classname):
    con = sqlite3.connect('spm_db.db')
    cur = con.cursor()
    try:
        cur.execute("DELETE FROM classes_tb WHERE classid = ?", (classid,))
        query = f"DROP TABLE {classname}"
        cur.execute(query)
        delete_timetable_query = f"DROP TABLE {classname}_timetable_schedule_tb"
        con.execute(delete_timetable_query)
        cur.execute("DELETE FROM students_tb WHERE classid=?", (classid,))
        con.commit()
        flash("Class deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting Class: {str(e)}", "danger")
    finally:
        con.close()
        return redirect(url_for('view_class'))

#update class
@app.route("/update_class_form/<int:classid>/<string:classname>/<string:dept>/<string:year>/<string:sem>",methods=["POST","GET"])
def update_class_form(classid,classname,dept,year,sem):
    con = sqlite3.connect("spm_db.db")
    cur = con.cursor()
    cur.execute('SELECT deptname FROM dept_tb')
    data = cur.fetchall()
    departments = [row[0] for row in data] 

   
    cur.execute('SELECT userid, username FROM users_tb')
    staff_list = cur.fetchall()
    con.close()
    return render_template("admin/update_class_form.html",classid = classid,classname=classname,dept=dept,year=year,sem=sem,departments=departments,staff_list=staff_list)


@app.route('/update_class', methods=['GET', 'POST'])
def update_class():
    classid = request.form.get('classid')
    new_classname = request.form.get('classname')
    old_classname  = request.form.get('oldclassname')
    new_dept = request.form.get('dept')
    new_year   = request.form.get('year')
    new_sem    = request.form.get('sem')
    selected_staffsid = request.form.getlist('staffsid')
    staffs_id = ",".join(selected_staffsid)
    file = request.files.get('file')
    
    if not classid or not new_classname or not new_dept  or not new_year or not new_sem or not staffs_id:
        flash("All values are required","danger")
        return redirect(url_for('view_class'))  
    try:
        con = sqlite3.connect('spm_db.db')
        cur = con.cursor()
        cur.execute("UPDATE classes_tb SET classname = ?,dept = ?,year=?, sem=?,staffsid =? WHERE classid =?", (new_classname, new_dept,new_year,new_sem,staffs_id,int(classid)))

        cur.execute("DELETE FROM students_tb WHERE classid=?", (classid,))
        
        query = f"ALTER TABLE '{old_classname}' RENAME TO '{new_classname}'"
        cur.execute(query)
        
        rename_time_table_schedule = f"ALTER TABLE {old_classname}_timetable_schedule_tb RENAME TO '{new_classname}_timetable_schedule_tb'"
        cur.execute(rename_time_table_schedule)
        con.commit()
        
        df = pd.read_excel(file)
        df = df[['rollno','name','email']] 
        df['dept'] = new_dept
        df['year'] = new_year
        df['classid'] = classid
        df['classname'] = new_classname
    
        df.to_sql("students_tb", con, if_exists='append', index=False)
        con.commit()
        flash("Class Updated successful...!!","success")
    except Exception as e:
        flash(f"Error Updating Class: {str(e)}", "danger")
    finally:
        con.close()
    return redirect(url_for('view_class'))    



    
        
@app.route("/class_schedule/<string:classname>")
def class_schedule(classname):
    con = sqlite3.connect('spm_db.db')
    cur = con.cursor()
    try:
        # Get staff and subject lists
        cur.execute("SELECT username FROM users_tb")
        staffs_names = [row[0] for row in cur.fetchall()]
            
        cur.execute('SELECT subjectname FROM subjects_tb')
        subjectnames = [row[0] for row in cur.fetchall()]

        # Check if timetable exists for this class
        cur.execute(f"""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='{classname}_timetable_schedule_tb'
        """)
        table_exists = cur.fetchone()

        timetable_data = {}
        if table_exists:
            # Fetch existing timetable data
            cur.execute(f"""
                SELECT day, period, subject, staff 
                FROM {classname}_timetable_schedule_tb
                ORDER BY 
                    CASE day
                        WHEN 'monday' THEN 1
                        WHEN 'tuesday' THEN 2
                        WHEN 'wednesday' THEN 3
                        WHEN 'thursday' THEN 4
                        WHEN 'friday' THEN 5
                        WHEN 'saturday' THEN 6
                        ELSE 7
                    END,
                    period
            """)
            
            for row in cur.fetchall():
                day = row[0]
                period = row[1]
                subject = row[2]
                staff = row[3]
                
                if day not in timetable_data:
                    timetable_data[day] = {}
                timetable_data[day][period] = {
                    'subject': subject,
                    'staff': staff
                }
            
        return render_template(
            "admin/class_schedule_form.html",
            staffs_names=staffs_names,
            subjectnames=subjectnames,
            classname=classname,
            timetable_data=timetable_data
        )
    except Exception as e:
        flash(f"Error loading form: {str(e)}", "danger")
        return redirect(url_for('view_class'))
    finally:
        con.close()

@app.route("/class_schedule_insert", methods=["POST", "GET"])
def class_schedule_insert():
    con = sqlite3.connect('spm_db.db')
    cur = con.cursor()
    
    if request.method == "POST":
        try:
            classname = request.form.get('classname')
            days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday','saturday']
            for day in days:
                for period in range(1, 9):
                    subject = request.form.get(f"{day}_p{period}_subject")
                    staff = request.form.get(f"{day}_p{period}_staff")
                    
                    if subject and staff:
                        cur.execute(f"""
                            INSERT OR REPLACE INTO {classname}_timetable_schedule_tb
                            (day, period, subject, staff) 
                            VALUES (?, ?, ?, ?)
                        """, (day, period, subject, staff))
            
            con.commit()
            flash("Class schedule saved successfully!", "success")
        except Exception as e:
            con.rollback()
            flash(f"Error saving schedule: {str(e)}", "danger")
        finally:
            con.close()
            return redirect(url_for('view_class'))


#manage admin
@app.route("/update_admin", methods=["GET", "POST"])
def update_admin():
    con = sqlite3.connect("spm_db.db")
    cur = con.cursor()
    
    if request.method == "POST":
        adminid = request.form.get("adminid")
        adminname = request.form.get("adminname")
        password = request.form.get("password")
        
        if not all([adminname, password]):
            flash("All fields are required", "danger")
            return redirect(url_for('update_admin'))
            
        try:
            cur.execute("UPDATE admin_tb SET username = ?, password = ? WHERE userid = ?",
                       (adminname, password, adminid))
            con.commit()
            flash("Admin details updated successfully", "success")
        except sqlite3.Error as e:
            con.rollback()
            flash(f"Database error: {str(e)}", "danger")
        finally:
            con.close()
        return redirect(url_for('update_admin'))
    else:
        cur.execute("SELECT * FROM admin_tb LIMIT 1")
        admin = cur.fetchone()
        con.close()
        return render_template("admin/update_admin.html", admin=admin)   
    
#----------------------------------end-admin-processes-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#





#--------------------------------------staff-processes-------------------------------------------------------------------------------------------------#
#view all attendance    
@app.route('/view_all_attendance')
def view_all_attendance():
    if 'userid' not in session:
        return redirect(url_for('login'))  
    
    user_id = str(session['userid']) 
    conn = sqlite3.connect('spm_db.db')
    conn.row_factory = sqlite3.Row  
    cursor = conn.cursor()
    
    
    cursor.execute("SELECT classname, classid, staffsid FROM classes_tb")
    all_classes = cursor.fetchall()
    

    classes = []
    for cls in all_classes:
        staff_ids = [id.strip() for id in cls['staffsid'].split(',')]
        if user_id in staff_ids:
            classes.append(cls)
    
    cursor.close()
    conn.close()
    
    return render_template('staff/view_attendance.html', classes=classes)

#mark the daily attendance
@app.route('/mark_attendance/<int:classid>/<string:classname>')
def mark_attendance(classid, classname):
    if 'username' not in session or 'userid' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect("spm_db.db")
    conn.row_factory = sqlite3.Row
    
    # Get today's date and day
    today_date = datetime.datetime.now().strftime('%Y-%m-%d')
    #today_day = datetime.datetime.now().strftime("%A").lower()
    today_day = "monday"
    current_staff_username = session['username']
    
    # Get students
    students = conn.execute(
        "SELECT rollno, name FROM students_tb WHERE classid = ?", 
        (classid,)
    ).fetchall()
    
    # Get all periods for today with staff info
    all_periods = conn.execute(
        f"SELECT period, subject, staff FROM {classname}_timetable_schedule_tb WHERE day = ?",
        (today_day,)
    ).fetchall()
    
    # Get attendance for today's date
    attendance_records = conn.execute(
        f"SELECT rollno, p1, p2, p3, p4, p5, p6, p7, p8, present, absent FROM {classname} WHERE date = ?",
        (today_date,)
    ).fetchall()
    
    # Prepare attendance data
    existing_attendance = {}
    for record in attendance_records:
        existing_attendance[record['rollno']] = {
            'p1': record['p1'],
            'p2': record['p2'],
            'p3': record['p3'],
            'p4': record['p4'],
            'p5': record['p5'],
            'p6': record['p6'],
            'p7': record['p7'],
            'p8': record['p8'],
            'present': record['present'],
            'absent': record['absent']
        }
    
    # Prepare timetable data
    subjects = [""] * 8
    staff_periods = {}  # {period_num: staff_username}
    current_staff_periods = set()
    
    for period in all_periods:
        period_num = period['period']
        if 1 <= period_num <= 8:
            subjects[period_num-1] = period['subject']
            staff_periods[period_num] = period['staff']
            if period['staff'] == current_staff_username:
                current_staff_periods.add(period_num)
    
    conn.close()
    
    return render_template('staff/attendance_sheet.html',
                         students=students,
                         subjects=subjects,
                         staff_periods=staff_periods,
                         current_staff_periods=current_staff_periods,
                         existing_attendance=existing_attendance,
                         today_date=today_date,
                         today_day=today_day,
                         classid=classid,
                         classname=classname)



#submit attendance
@app.route('/submit_attendance', methods=['POST'])
def submit_attendance():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect("spm_db.db")
    conn.row_factory = sqlite3.Row
    
    try:
        classid = request.form['classid']
        classname = request.form['classname']
        today_date = datetime.datetime.now().strftime('%Y-%m-%d')
        today_day = datetime.datetime.now().strftime("%A").lower()
        today_day = "monday"
        current_staff_username = session['username']
        
        # Get staff's periods for today
        staff_periods = [row['period'] for row in conn.execute(
            f"SELECT period FROM {classname}_timetable_schedule_tb WHERE day = ? AND staff = ?",
            (today_day, current_staff_username)
        ).fetchall()]
        
        # Get all students
        students = conn.execute(
            "SELECT rollno, name FROM students_tb WHERE classid = ?",
            (classid,)
        ).fetchall()
        
        for student in students:
            rollno = student['rollno']
            name = student['name']
            
            # Check if attendance record exists for today
            existing_record = conn.execute(
                f"SELECT * FROM {classname} WHERE rollno = ? AND date = ?",
                (rollno, today_date)
            ).fetchone()
            
            # Initialize period values
            period_values = {f'p{i}': 0 for i in range(1, 9)}
            
            # If record exists, load existing values
            if existing_record:
                for i in range(1, 9):
                    period_values[f'p{i}'] = existing_record[f'p{i}']
            
            # Update only the periods this staff is responsible for
            for period in staff_periods:
                checkbox_name = f'attendance_{period}_{rollno}'
                period_values[f'p{period}'] = 1 if checkbox_name in request.form else 0
            
            # Calculate totals
            present = sum(period_values.values())
            absent = 8 - present
            
            if existing_record:
                # Update existing record
                conn.execute(
                    f"""UPDATE {classname} SET
                    p1 = ?, p2 = ?, p3 = ?, p4 = ?,
                    p5 = ?, p6 = ?, p7 = ?, p8 = ?,
                    present = ?, absent = ?
                    WHERE rollno = ? AND date = ?""",
                    (period_values['p1'], period_values['p2'], period_values['p3'], period_values['p4'],
                     period_values['p5'], period_values['p6'], period_values['p7'], period_values['p8'],
                     present, absent, rollno, today_date)
                )
            else:
                # Insert new record
                conn.execute(
                    f"""INSERT INTO {classname} 
                    (rollno, name, date, day, p1, p2, p3, p4, p5, p6, p7, p8, present, absent)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (rollno, name, today_date, today_day,
                     period_values['p1'], period_values['p2'], period_values['p3'], period_values['p4'],
                     period_values['p5'], period_values['p6'], period_values['p7'], period_values['p8'],
                     present, absent)
                )
        
        conn.commit()
        flash('Attendance saved successfully!', 'success')
    
    except Exception as e:
        conn.rollback()
        flash(f'Error saving attendance: {str(e)}', 'danger')
        app.logger.error(f"Error in submit_attendance: {str(e)}")
    
    finally:
        conn.close()
    
    return redirect(url_for('mark_attendance', 
                         classid=classid, 
                         classname=classname))









#report generation process

@app.route("/generate_report", methods=["POST", "GET"])
def generate_report():
    con = sqlite3.connect('spm_db.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    
    if request.method == "POST":
        classname = request.form.get('classname')
        startdate = request.form.get('startdate')
        enddate = request.form.get('enddate')
        
        if not all([classname, startdate, enddate]):
            flash("All values are required", "danger")
            return redirect(url_for('generate_report'))
            
        try:
            # Get class ID
            cur.execute("SELECT classid FROM classes_tb WHERE classname = ?", (classname,))
            class_row = cur.fetchone()
            if not class_row:
                flash("Class not found", "danger")
                return redirect(url_for('generate_report'))
            
            classid = class_row['classid']
            
            # Get actual attendance dates between start and end date
            cur.execute(f"""
                SELECT DISTINCT date 
                FROM {classname}
                WHERE date BETWEEN ? AND ?
                ORDER BY date
            """, (startdate, enddate))
            
            attendance_dates = [row['date'] for row in cur.fetchall()]
            total_days = len(attendance_dates)
            total_possible_hours = total_days * 8
            
            # Get student attendance data
            query = f"""
                SELECT s.rollno, s.name, 
                       COALESCE(SUM(a.present), 0) as total_present,
                       COALESCE(SUM(a.absent), 0) as total_absent
                FROM students_tb s
                LEFT JOIN {classname} a ON s.rollno = a.rollno AND a.date BETWEEN ? AND ?
                WHERE s.classid = ?
                GROUP BY s.rollno, s.name
                ORDER BY s.rollno
            """
            cur.execute(query, (startdate, enddate, classid))
            
            students = []
            for row in cur.fetchall():
                total_present = row['total_present']
                percentage = (total_present / total_possible_hours) * 100 if total_possible_hours > 0 else 0
                
                students.append({
                    'rollno': row['rollno'],
                    'name': row['name'],
                    'present': total_present,
                    'absent': row['total_absent'],
                    'percentage': round(percentage, 2)
                })
            
            report_data = {
                'classname': classname,
                'start_date': startdate,
                'end_date': enddate,
                'students': students,
                'report_date': datetime.datetime.now().strftime('%Y-%m-%d'),
                'total_days': total_days,
                'total_hours': total_possible_hours,
                'attendance_dates': attendance_dates  # Optional: include in report if needed
            }
            
            return render_template("admin/report.html", report=report_data)
            
        except Exception as e:
            flash(f"Error generating report: {str(e)}", "danger")
            app.logger.error(f"Report error: {str(e)}", exc_info=True)
            return redirect(url_for('generate_report'))
        finally:
            con.close()
    else:
        # GET request - show form (same as before)
        
        try:
            # Get departments and class list
            cur.execute('SELECT DISTINCT deptname FROM dept_tb')
            departments = [row[0] for row in cur.fetchall()]
       
            cur.execute('SELECT DISTINCT classname FROM classes_tb')
            class_list = [row[0] for row in cur.fetchall()]

            # Get date range for each class
            class_date_ranges = {}
            for classname in class_list:
                try:
                    # Get min and max dates from attendance table
                    cur.execute(f"""
                        SELECT MIN(date) as min_date, MAX(date) as max_date 
                        FROM {classname}
                    """)
                    date_range = cur.fetchone()
                    if date_range and date_range['min_date'] and date_range['max_date']:
                        class_date_ranges[classname] = {
                            'min_date': date_range['min_date'],
                            'max_date': date_range['max_date']
                        }
                except sqlite3.Error as e:
                    # Table might not exist yet
                    continue
            
            return render_template("admin/generate_report_form.html", 
                                departments=departments,
                                class_list=class_list,
                                date_ranges=class_date_ranges)
        except Exception as e:
            flash(f"Error loading form: {str(e)}", "danger")
            return redirect(url_for('generate_report'))
        finally:
            con.close()


        
#---------------------------------------end-staff-processes-----------------------------------------------------------------------------------------------------#



#-----------------------------------student-process----------------------------------------------------------------------------------#

#student search attendance percentage
@app.route('/generate_report_student', methods=['GET', 'POST'])
def generate_report_student():
    con = sqlite3.connect('spm_db.db')
    cur = con.cursor()
    
    if request.method == 'POST':
        rollno = request.form.get("rollno")
        if not rollno:
            flash("Enter your rollno", "danger")
            return render_template('student/generate_report_form.html')
        
        try:
            # Get student's classname
            cur.execute("SELECT classname FROM students_tb WHERE rollno=?", (rollno,))
            class_info = cur.fetchone()
            
            if not class_info:
                flash("Roll number not found", "danger")
                return render_template('student/generate_report_form.html')
            
            classname = class_info[0]
            
            # Get total possible hours (days * 8)
            cur.execute(f"SELECT COUNT(DISTINCT date) FROM {classname}")
            total_days = cur.fetchone()[0]
            total_hours = total_days * 8
            
            # Get student's present hours
            cur.execute(f"SELECT present FROM {classname} WHERE rollno = ?", (rollno,))
            present_hours = cur.fetchall()
            total_present = 0
            for i in present_hours:
                total_present += i[0]
            
            # Calculate percentage
            percentage = (total_present / total_hours) * 100 if total_hours > 0 else 0
            
            # Format the percentage to 2 decimal places
            formatted_percentage = f"{percentage:.2f}%"
            
            return render_template('student/generate_report_form.html',
                                rollno=rollno,
                                percentage=formatted_percentage,
                                present_hours=total_present,
                                total_hours=total_hours)
            
        except sqlite3.Error as e:
            flash(f"Database error: {str(e)}", "danger")
            return render_template('student/generate_report_form.html')
        finally:
            con.close()
    else:
        return render_template('student/generate_report_form.html')
    


#-----------------------------------end-student-process----------------------------------------------------------------------------------#
if __name__ == '__main__':
    app.run(debug=True)