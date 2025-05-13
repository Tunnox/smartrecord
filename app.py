from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import psycopg2

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key

# Configure your PostgreSQL database connection here
connection = psycopg2.connect(dbname='AGT', user='postgres', password='postk116chuk95', host='localhost', port='5432')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    cursor = connection.cursor()
    
    # SQL query to search for data in DATA_RECORDS table
    sql_query = f"""
        SELECT * FROM public."DATA_RECORDS" 
        WHERE "TITLE" ILIKE %s OR
           "FIRST_NAME" ILIKE %s 
           OR "LAST_NAME" ILIKE %s 
           OR "AGE"::TEXT ILIKE %s 
           OR "GENDER" ILIKE %s
           OR "DATE_OF_BIRTH"::TEXT ILIKE %s
           OR "ADDRESS" ILIKE %s
           OR "EMAIL" ILIKE %s
           OR "MOBILE_NUMBER"::TEXT ILIKE %s 
           OR "STATUS" ILIKE %s  
           OR "DEPARTMENT" ILIKE %s
           OR "RELATIONSHIP_STATUS" ILIKE %s
           OR "EMPLOYEMENT_STATUS" ILIKE %s
           OR "CONSENT" ILIKE %s
    """
    
    # Execute the query with wildcard search
    cursor.execute(sql_query, [f'%{keyword}%'] * 14)
    
    results = cursor.fetchall()
    
    # Close cursor after fetching results
    cursor.close()
    
    return render_template('index.html', results=results)

@app.route('/get_details', methods=['POST'])
def get_details():
    full_name = request.json['full_name']
    name_parts = full_name.split(' ')
    
    # Check if we have at least two parts for first and last name
    if len(name_parts) < 2:
        return jsonify({"error": "Please provide both first and last names."}), 400
    
    First_name = name_parts[0]
    Last_name = ' '.join(name_parts[1:])  # Join the rest as the last name
    cursor = connection.cursor()
    
    # SQL query to get full details based on first and last name
    sql_query = f"""
        SELECT "TITLE", "FIRST_NAME", "LAST_NAME", "AGE", "GENDER", "DATE_OF_BIRTH", "ADDRESS", "EMAIL", "MOBILE_NUMBER", "STATUS", "DEPARTMENT", "RELATIONSHIP_STATUS", "EMPLOYEMENT_STATUS", "CONSENT" 
        FROM public."DATA_RECORDS" 
        WHERE "FIRST_NAME" = %s AND "LAST_NAME" = %s
    """
    
    cursor.execute(sql_query, (First_name, Last_name))
    record = cursor.fetchone()
    cursor.close()
    
    return jsonify(record)

@app.route('/insert', methods=['GET','POST'])
def insert():
    if request.method == 'POST':
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
        employment_status = request.form['employment_status']
        consent = request.form['consent']

        cursor = connection.cursor()
        
        cursor.execute("""
            INSERT INTO public."DATA_RECORDS" ("TITLE", "FIRST_NAME", "LAST_NAME", "AGE", "GENDER", "DATE_OF_BIRTH", "ADDRESS", "EMAIL", "MOBILE_NUMBER", "STATUS", "DEPARTMENT", "RELATIONSHIP_STATUS", "EMPLOYEMENT_STATUS", "CONSENT")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (title, first_name, last_name, age, gender,date_of_birth, address, email, mobile_number, status,department, relationship_status, employment_status, consent))
        connection.commit()  # Don't forget to commit the transaction!
        cursor.close()
    
    flash('Record inserted successfully!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
    
    
