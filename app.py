from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import oracledb

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key

# Configure your Oracle database connection here
connection = oracledb.connect(user='C##AGT', password='AGT_137i_church_4f9nyZ', dsn='192.168.0.185:1521/orcl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    cursor = connection.cursor()
    
    # SQL query to search for data in AGT_RECORDS table
    sql_query = f"""
        SELECT * FROM C##AGT.AGT_RECORDS 
        WHERE FIRST_NAME LIKE :keyword 
           OR LAST_NAME LIKE :keyword 
           OR AGE LIKE :keyword 
           OR GENDER LIKE :keyword
           OR GENDER LIKE :keyword
           OR DATE_OF_BIRTH LIKE :keyword
           OR ADDRESS LIKE :keyword
           OR EMAIL LIKE :keyword
           OR MOBILE_NUMBER LIKE :keyword 
           OR STATUS LIKE :keyword  
           OR DEPARTMENT LIKE :keyword
           OR RELATIONSHIP_STATUS LIKE :keyword
           OR EMPLOYEMENT_STATUS LIKE :keyword
           OR CONSENT LIKE :keyword
    """
    
    # Execute the query with wildcard search
    cursor.execute(sql_query, keyword=f'%{keyword}%')
    
    results = cursor.fetchall()
    
    # Close cursor after fetching results
    cursor.close()
    
    return render_template('index.html', results=results)

@app.route('/get_details', methods=['POST'])
def get_details():
    full_name = request.json['full_name']
    First_name, Last_name = full_name.split(' ')
    cursor = connection.cursor()
    
    # SQL query to get full details based on first and last name
    sql_query = f"""
        SELECT * FROM C##AGT.AGT_RECORDS 
        WHERE FIRST_NAME = :first_name AND LAST_NAME = :last_name
    """
    
    cursor.execute(sql_query, first_name=First_name, last_name=Last_name)
    details = cursor.fetchone()
    cursor.close()
    
    return jsonify(details)

@app.route('/update', methods=['POST'])
def update():
    id = request.form.get('id')
    title = request.form.get('title')
    First_name = request.form.get('first_name')
    Last_name = request.form.get('last_name')
    age = request.form.get('age')
    gender = request.form.get('gender')
    date_of_birth = request.form.get('DATE_OF_BIRTH')
    address = request.form.get('ADDRESS')
    email = request.form.get('EMAIL')
    mobile_number = request.form.get('MOBILE_NUMBER')
    status = request.form.get('STATUS')
    department = request.form.get('DEPARTMENT')
    relationship_status = request.form.get('RELATIONSHIP_STATUS')
    employement_status = request.form.get('EMPLOYEMENT_STATUS')
    consent = request.form.get('CONSENT')

    # Update the record in the database
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE C##AGT.AGT_RECORDS 
        SET TITLE = :title,
            FIRST_NAME = :first_name,
            LAST_NAME = :last_name,
            AGE = :age,
            GENDER = :gender,
            DATE_OF_BIRTH = :date_of_birth,
            ADDRESS = :address,
            EMAIL = :email,
            MOBILE_NUMBER =:mobile_number,
            STATUS = :status,
            DEPARTMENT =:department,
            RELATIONSHIP_STATUS = :relationship_status,
            EMPLOYEMENT_status = :employement_status,
            CONSENT = :consent 
        WHERE ID = :id""",
        {'title': title, 'first_name': First_name, 'last_name': Last_name,
         'age': age, 'gender': gender, 'date_of_birth': date_of_birth, 'address': address, 'email': email, 'mobile_number': mobile_number, 'status':status, 'department': department, 'relationship_status': relationship_status, 'employement_status': employement_status, 'consent': consent, 'id': id})
    
    connection.commit()
    cursor.close()

    return redirect(url_for('index'))

@app.route('/insert', methods=['POST'])
def insert():
    title = request.form['title']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    age = request.form['age']
    gender = request.form['gender']
    date_of_birth = request.form['date_of_birth']
    address = request.form['address']
    email = request.form['email']
    mobile_number = request.form['mobile_number']
    status = request.form['status']
    department = request.form['department']
    relationship_status = request.form['relationship_status']
    employement_status = request.form['employement_status']
    consent = request.form.get('consent')

    cursor = connection.cursor()
    
    # SQL INSERT statement
    sql_insert_query = """
        INSERT INTO C##AGT.AGT_RECORDS (TITLE, FIRST_NAME, LAST_NAME, AGE, GENDER,
        DATE_OF_BIRTH, ADDRESS, EMAIL, MOBILE_NUMBER, STATUS,
        DEPARTMENT, RELATIONSHIP_STATUS, EMPLOYEMENT_STATUS, CONSENT)
        VALUES (:title, :first_name, :last_name, :age, :gender,
        TO_DATE(:date_of_birth, 'YYYY-MM-DD'), :address,
        :email, :mobile_number, :status,
        :department, :relationship_status,
        :employement_status, :consent)
    """
    
    cursor.execute(sql_insert_query, {
        'title': title,
        'first_name': first_name,
        'last_name': last_name,
        'age': age,
        'gender': gender,
        'date_of_birth': date_of_birth,
        'address': address,
        'email': email,
        'mobile_number': mobile_number,
        'status': status,
        'department': department,
        'relationship_status': relationship_status,
        'employement_status': employement_status,
        'consent': consent
    })
    
    connection.commit()
    
    cursor.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
