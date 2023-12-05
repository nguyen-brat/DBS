
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

# PostgreSQL database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456789@database-1.cxrip2pysplk.ap-southeast-2.rds.amazonaws.com:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
conn = psycopg2.connect(
    database="postgres",
    user = "postgres", 
    host= 'database-1.cxrip2pysplk.ap-southeast-2.rds.amazonaws.com',
    password = "123456789",
    port = 5432
)
cur = conn.cursor()

# Define the Member model
class Member(db.Model):
    memberid = db.Column(db.Integer, primary_key=True)
    ssn = db.Column(db.String)
    providerid = db.Column(db.Integer)

# Endpoint to handle adding member data
@app.route('/addMember', methods=['POST'])
def add_member():
    try:
        new_member = Member(**request.json)
        db.session.add(new_member)
        db.session.commit()
        return jsonify(new_member.memberid), 201
    except Exception as e:
        print('Error adding member data:', e)
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        db.session.close()

class Person(db.Model):
    ssn = db.Column(db.String, primary_key=True)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    email = db.Column(db.String)
    phone_number = db.Column(db.String)
    home_address = db.Column(db.String)

# Endpoint to handle adding person data
@app.route('/addPerson', methods=['POST'])
def add_person():
    try:
        new_person = Person(**request.json)
        db.session.add(new_person)
        db.session.commit()
        return jsonify({'ssn': new_person.ssn}), 201
    except Exception as e:
        print('Error adding person data:', e)
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        db.session.close()


@app.route('/retrieve_member_table', methods=['GET'])
def retrieve_member_table():
    cur.execute("SELECT * FROM member")
    members = cur.fetchall()
    result = [{'ssn': member[0], 'memberid': member[1], 'providerid': member[2]} for member in members]
    return jsonify({'result': result})

@app.route('/retrieve_item_table', methods=['GET'])
def retrieve_item_table():
    cur.execute("SELECT * FROM item")
    members = cur.fetchall()
    
    result = [{'issn_isbn': member[0], 'version': member[1], 'title': member[2],'price': member[3], 'publication_date': member[4], 'providerid': member[5], 'itemtype': member[6],} for member in members]
    return jsonify({'result': result})

@app.route('/retrieve_author_table', methods=['GET'])
def retrieve_author_table():
    cur.execute("SELECT * FROM author")
    members = cur.fetchall()
    result = [{'authorid': member[0], 'ssn': member[1]} for member in members]
    return jsonify({'result': result})

@app.route('/retrieve_write_table', methods=['GET'])
def retrieve_write_table():
    cur.execute("SELECT * FROM write")
    members = cur.fetchall()
    result = [{'issn_isbn': member[0], 'authorid': member[1]} for member in members]
    return jsonify({'result': result})



@app.route('/retrieve_person_table', methods=['GET'])
def retrieve_person_table():
    cur.execute("SELECT * FROM person")
    members = cur.fetchall()
    result = [{'ssn': member[0], 'fname': member[1], 'lname': member[2],'email': member[3],'phone_number': member[4],'home_address': member[5]} for member in members]
    return jsonify({'result': result})


@app.route('/retrieve_data_warehouse_table', methods=['GET'])
def retrieve_data_warehouse_table():
    cur.execute("SELECT * FROM data_warehouse")
    members = cur.fetchall()
    result = [{'public_key': member[0], 'managerid': member[1]} for member in members]
    return jsonify({'result': result})

@app.route('/retrieve_digital_copy_table', methods=['GET'])
def retrieve_digital_copy_table():
    cur.execute("SELECT * FROM digital_copy")
    members = cur.fetchall()
    result = [{'issn_isbn': member[0], 'filesize': member[1]} for member in members]
    return jsonify({'result': result})

@app.route('/retrieve_dissertation_table', methods=['GET'])
def retrieve_dissertation_table():
    cur.execute("SELECT * FROM dissertation")
    members = cur.fetchall()
    result = [{'issn_isbn': member[0], 'id': member[1], 'advisor': member[2],'institution': member[3]} for member in members]
    return jsonify({'result': result})


@app.route('/retrieve_file_info_table', methods=['GET'])
def retrieve_file_info_table():
    cur.execute("SELECT * FROM file_info")
    members = cur.fetchall()
    result = [{'issn_isbn': member[0], 'afile_format': member[1], 'afile_size': member[2]} for member in members]
    return jsonify({'result': result})

@app.route('/retrieve_client_table', methods=['GET'])
def retrieve_client_table():
    cur.execute("SELECT * FROM client")
    members = cur.fetchall()
    result = [{'memberid': member[0], 'registerdate': member[1], 'creditscore': member[2]} for member in members]
    return jsonify({'result': result})

@app.route('/retrieve_fine_transaction_table', methods=['GET'])
def retrieve_fine_transaction_table():
    cur.execute("SELECT * FROM fine_transaction")
    members = cur.fetchall()
    result = [{'bookid': member[0], 'payment_method': member[1], 'fine_type': member[2],'credit_score_update': member[3],'clientid': member[4],'managerid': member[5]} for member in members]
    return jsonify({'result': result})

@app.route('/retrieve_magazine_table', methods=['GET'])
def retrieve_magazine_table():
    cur.execute("SELECT * FROM magazine")
    members = cur.fetchall()
    result = [{'issn_isbn': member[0], 'issuenumber': member[1]} for member in members]
    return jsonify({'result': result})

@app.route('/retrieve_manager_table', methods=['GET'])
def retrieve_manager_table():
    cur.execute("SELECT * FROM manager")
    members = cur.fetchall()
    result = [{'memberid': member[0], 'startdate': member[1]} for member in members]
    return jsonify({'result': result})

@app.route('/retrieve_organization_table', methods=['GET'])
def retrieve_organization_table():
    cur.execute("SELECT * FROM organization")
    members = cur.fetchall()
    result = [{'name': member[0], 'address': member[1], 'website': member[2],'providerid': member[3]} for member in members]
    return jsonify({'result': result})

@app.route('/retrieve_physical_copy_table', methods=['GET'])
def retrieve_physical_copy_table():
    cur.execute("SELECT * FROM physical_copy")
    members = cur.fetchall()
    result = [{'issn_isbn': member[0], 'publisher': member[1], 'num_pages': member[2],'borrow_date': member[3],'return_date': member[4],'sid': member[5]} for member in members]
    return jsonify({'result': result})

@app.route('/retrieve_provider_table', methods=['GET'])
def retrieve_provider_table():
    cur.execute("SELECT * FROM provider")
    members = cur.fetchall()
    result = [{'providerid': member[0]} for member in members]
    return jsonify({'result': result})

@app.route('/retrieve_scientific_paper_table', methods=['GET'])
def retrieve_scientific_paper_table():
    cur.execute("SELECT * FROM scientific_paper")
    members = cur.fetchall()
    result = [{'issn_isbn': member[0], 'id': member[1], 'journal_conference': member[2]} for member in members]
    return jsonify({'result': result})

@app.route('/retrieve_session_table', methods=['GET'])
def retrieve_session_table():
    cur.execute("SELECT * FROM session")
    members = cur.fetchall()
    result = [{'sessionid': member[0], 'payment_method': member[1], 'cost': member[2],'day': member[3],'month': member[4],'year': member[5],'clientid': member[6],'managerid': member[7],'wkey': member[8]} for member in members]
    return jsonify({'result': result})


@app.route('/', methods=['POST', 'GET'])
def default():
    return "Hello world"

# @app.route('/borrow_book', methods=['POST', 'GET'])
# def borrow_book():
#     pass

# @app.route('/pay_book', method=['POST', 'GET'])
# def pay_book():
#     pass

@app.route('/retrieve_title', methods=['POST', 'GET'])
def retrieve_title():
    '''
    This function retrieve the titles of all materials that was provided by a
    specific organization name and published in a specific year
    '''
    #cur = conn.cursor()
    publication_year = request.args.get('publication_year')
    organization = request.args.get('organization')
    sql_query = f'''
    SELECT title FROM item
    INNER JOIN organization ON organization.providerid = item.providerid
    WHERE item.publication_date >= '%{publication_year}-1-1%'::date
    AND item.publication_date <= '%{publication_year}-12-31%'::date
    AND organization.name LIKE '%{organization}%'
'''
    cur.execute(sql_query)
    outputs = cur.fetchall()
    outputs = [{'title':output} for output in outputs]
    conn.commit()
    #cur.close()
    return jsonify({'result':outputs})

@app.route('/retrieve_session', methods=['POST', 'GET'])
def retrieve_session():
    '''
    find session_id of a session has data < given date
    and chossen payment method
    '''
    #cur = conn.cursor()
    day = request.args.get('day')
    month = request.args.get('month')
    year = request.args.get('year')
    payment_method = request.args.get('payment_method')
    sql_query = f'''
    SELECT sessionid FROM session
    WHERE payment_method LIKE '%{payment_method}%'
    AND day < {day}
    AND month <= {month}
    AND year <= {year}
'''
    cur.execute(sql_query)
    outputs = cur.fetchall()
    outputs = [{'sessionid':output} for output in outputs]
    conn.commit()
    #cur.close()
    return jsonify({'result':outputs})

@app.route('/retrieve_magazine_expensivest', methods=['POST', 'GET'])
def retrieve_magazine_highest_price():
    #cur = conn.cursor()
    authorid = request.args.get('authorid')
    sql_query = f'''
    SELECT
        item.issn_isbn
    FROM
        item
    INNER JOIN write ON item.issn_isbn = write.issn_isbn
    INNER JOIN author ON write.authorid = author.authorid
    WHERE
        item.itemtype LIKE '%Magazine%' AND author.authorid = {authorid}
    AND item.price = (
        SELECT
            MAX(price)
        FROM
            item
        WHERE
            itemtype LIKE '%Magazine%'
    );
'''
    cur.execute(sql_query)
    conn.commit()
    outputs = cur.fetchall()
    outputs = [{'issn_isbn':output} for output in outputs]
    #cur.close()
    return jsonify({'result':outputs})

@app.route('/retrieve_total_cost', methods=['POST', 'GET'])
def retrieve_total_cost():
    #cur = conn.cursor()
    clientid = request.args.get('clientid')
    month = request.args.get('month')
    sql_query = f'''
    SELECT SUM(cost)
    FROM session
    WHERE session.clientid LIKE '%{clientid}%'
    AND session.month = {month}
    AND session.year = 2022
'''
    cur.execute(sql_query)
    conn.commit()
    output = cur.fetchall()
    output = [{'result':output}]
    #cur.close()
    return jsonify({'result':output})

@app.route('/retrieve_client_name', methods=['POST', 'GET'])
def retrieve_client_name():
    '''
    Retrieve name of all client that make more than
    10 session in a specific year
    '''
    #cur = conn.cursor()
    year = request.args.get('year')
    sql_query = f'''
    SELECT
        session.clientid, fname, lname
    FROM
        session
    INNER JOIN member ON member.memberid = session.clientid
    INNER JOIN person ON person.ssn = member.ssn
    WHERE
        session.year = {year}
    GROUP BY
        session.clientid, fname, lname
    HAVING
        COUNT(session.clientid) >= 10
'''
    cur.execute(sql_query)
    conn.commit()
    outputs = cur.fetchall()
    outputs = [{'cliendid':output[0], 'fname':output[1], 'lname':output[2]} for output in outputs]
    #cur.close()
    return jsonify({'result':outputs})

@app.route('/add_client', methods=['POST', 'GET'])
def add_client():
    #cur = conn.cursor()
    ssn = request.args.get('ssn')
    fname = request.args.get('fname')
    mname = request.args.get('mname')
    lname = request.args.get('lname')
    email = request.args.get('email')
    phone_number = request.args.get('phone_number')
    home_address = request.args.get('home_address')
    sql_query = f'''INSERT INTO person (ssn, fname, mname, lname, email, phone_number, home_address) VALUES
    {ssn, fname, mname, lname, email, phone_number, home_address};
    '''
    cur.execute(sql_query)
    conn.commit()
    #cur.close()
    return f"sucess full add client to db"

@app.route('/remove_client', methods=['POST', 'GET'])
def remove_client():
    #cur = conn.cursor()
    ssn = request.args.get('ssn')
    sql_query = f'''DELETE FROM person
    WHERE ssn LIKE '%{ssn}%';
    '''
    cur.execute(sql_query)
    conn.commit()
    #cur.close()

    return f"success full remove client has ssn {ssn} out of db"

# @app.route('/borrow_book', methods=['POST', 'GET'])
# def borrow_book():
#     borrow_date = request.args.get('borrow_date')


@app.route('/api/insertData', methods=['POST'])
def insert_data():
    try:
        data = request.json
        table = data.get('table')
        column_data = data.get('columnData')

        # Connect to the PostgreSQL database
        cursor = conn.cursor()

        # Build the INSERT query dynamically based on user input
        insert_query = f"INSERT INTO {table} ({', '.join(column_data.keys())}) VALUES ({', '.join(['%s'] * len(column_data))}) RETURNING *"
        values = tuple(column_data.values())

        cursor.execute(insert_query, values)
        conn.commit()

        result = cursor.fetchone()
        conn.close()

        return jsonify(result), 200

    except Exception as e:
        print('Error inserting data:', e)
        return jsonify({'error': 'Internal Server Error'}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port='6868', debug=True)