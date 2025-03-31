from flask import Flask, render_template, request,session,send_file,flash,url_for,redirect
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

#---------------------------------------------------------------------------------------------------------------#

#---------------------------------login-process---------------------------------------------------------------#

#login user
@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        con = None   
        try:
            con = sqlite3.connect("spm_db.db")
            cur = con.cursor()
                
            username = request.form.get('username')
            password = request.form.get('password')
            userid = request.form.get('userid')
            
            if username == "admin" and password == "123" and userid =="1":
                session['userid'] = 1
                session['username'] = "admin"
                flash("Login Successfull..!!","success")
                con = sqlite3.connect("spm_db.db")
                cur = con.cursor()
                cur.execute("SELECT * FROM users_tb")
                total_staff = len(cur.fetchall()) 
    
                cur.execute("SELECT * FROM classes_tb")
                total_classes = len(cur.fetchall()) 
                return render_template("admin/admin_panel.html",total_staff=total_staff,total_classes=total_classes)
            else:
                cur.execute("SELECT * FROM users_tb WHERE username=? AND pass=? and userid=?", (username, password,userid))
                data = cur.fetchone()
                
                if data:
                        session['userid'] = int(userid)
                        session['username'] = username
                        flash("Login Successfull..!!","success")
                        return render_template("/staff/staff_panel.html") 
                else:
                    flash("Login Failed..!!","danger")
                    return redirect(url_for('login'))
                
        except Exception as e:
            flash(f"Error in Insertion: {str(e)}", "danger")
        finally:
            if con:
                con.close()
        
    else:
        return render_template("login.html")
    
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
            
            create_table_query = f"CREATE TABLE IF NOT EXISTS {classname} (slno INTEGER, rollno INTEGER,name VARCHAR(50),present INTEGER, absent INTEGER,date VARCHAR(50),day VARCHAR(50))"
            cur.execute(create_table_query)
        
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
        con.commit()
        
        df = pd.read_excel(file)
        df = df[['rollno','name','email']] 
        df['dept'] = new_dept
        df['year'] = new_year
        df['classid'] = classid
        df['classname'] = new_classname
    
        df.to_sql("students_tb", con, if_exists='append', index=False)
        con.commit()
        flash("Class Updated success...!!","success")
    except Exception as e:
        flash(f"Error Updating Class: {str(e)}", "danger")
    finally:
        con.close()
    return redirect(url_for('view_class'))    





@app.route("/class_schedule", methods=["POST", "GET"])
def class_schedule():
    con = sqlite3.connect('spm_db.db')
    cur = con.cursor()
    
    if request.method == "POST":
        try:
            days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
            for day in days:
                for period in range(1, 9):
                    subject = request.form.get(f"{day}_p{period}_subject")
                    staff = request.form.get(f"{day}_p{period}_staff")
                    
                    if subject and staff:
                        cur.execute("""
                            INSERT OR REPLACE INTO timetable_tb 
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
            return redirect(url_for('class_schedule'))
    
    else:
        try:
            cur.execute("SELECT username FROM users_tb")
            staffs_names = [row[0] for row in cur.fetchall()]
            
            cur.execute('SELECT subjectname FROM subjects_tb')
            subjectnames = [row[0] for row in cur.fetchall()]
            
            return render_template("admin/class_schedule_form.html",
                                staffs_names=staffs_names,
                                subjectnames=subjectnames)
        except Exception as e:
            flash(f"Error loading form: {str(e)}", "danger")
            return redirect(url_for('admin_dashboard'))
        finally:
            con.close()
    
    
        
        
    

#----------------------------------end-admin-processes-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#









#--------------------------------------staff-processes-------------------------------------------------------------------------------------------------#


#---------------------------------------end-staff-processes-----------------------------------------------------------------------------------------------------#

if __name__ == '__main__':
    app.run(debug=True)
    
    
    
    

'''def init_db():
   init_db()
    con = sqlite3.connect('spm_db.db')
    cur = con.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS timetable_tb (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                day TEXT NOT NULL,
                period INTEGER NOT NULL,
                subject TEXT NOT NULL,
                staff TEXT NOT NULL,
                UNIQUE(day, period)
            )
        """)
        con.commit()
    finally:
        con.close()

'''