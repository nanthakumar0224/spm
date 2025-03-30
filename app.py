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
    row_count = len(cur.fetchall()) 
    return render_template("admin/admin_panel.html",total_staff=row_count)

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
                row_count = len(cur.fetchall()) 
                return render_template("admin/admin_panel.html",total_staff=row_count)
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
        subjectid    = request.form.get('subid')
        subjectname = request.form.get('subname')
        dept = request.form.get('dept')
        year = request.form.get('year')
        semester = request.form.get('sem')
        selected_staffs = request.form.getlist('staffs')
        staffs_str = ",".join(selected_staffs)
        if not subjectid or not subjectname or not dept or not year or not semester:
            flash("All values are required","danger")
            return redirect(url_for('insert_sub'))
            
        try:
            cur.execute("INSERT INTO subjects_tb (subjectid,subjectname, dept,year,sem,staffs) VALUES (?, ?,?, ?,?, ?)",(subjectid,subjectname, dept, year,semester,staffs_str))
            con.commit()
            flash("Subject Added Successfully!", "success")
            
        except sqlite3.IntegrityError:
            flash("Subject Name or Id already exists!", "danger") 
        except Exception as e:
            flash(f"Error in Insertion: {str(e)}", "danger")
        finally:
            con.close()
            return redirect(url_for('insert_sub'))
    else:
        cur.execute('SELECT deptname FROM dept_tb')
        data = cur.fetchall()
        departments = [row[0] for row in data] 
        con.close
        return render_template("admin/subject_entry_form.html",departments=departments)
        

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
    con.close()
    return render_template("admin/update_subject_form.html",subjectid = subjectid,subjectname=subjectname,dept=dept,year=year,sem=sem,departments=departments)


@app.route('/update_subject', methods=['GET', 'POST'])
def update_subject():
    subjectid = request.form.get('subid')
    new_subjectname = request.form.get('subname')
    new_dept = request.form.get('dept')
    new_year   = request.form.get('year')
    new_sem    = request.form.get('sem')
    if not subjectid or not new_subjectname or not new_dept  or not new_year or not new_sem:
        flash("All values are required","danger")
        return redirect(url_for('view_subject'))  
    try:
        con = sqlite3.connect('spm_db.db')
        cur = con.cursor()
        cur.execute("UPDATE subjects_tb SET subjectname = ?,dept = ?,year=?, sem=? WHERE subjectid =?", (new_subjectname, new_dept,new_year,new_sem,int(subjectid)))
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

@app.route("/create_class_form")
def create_class_form():
    return render_template("admin/class_entry_form.html")





#----------------------------------end-admin-processes-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#















#--------------------------------------staff-processes-------------------------------------------------------------------------------------------------#


#---------------------------------------end-staff-processes-----------------------------------------------------------------------------------------------------#

if __name__ == '__main__':
    app.run(debug=True)