
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/retrieve_person_table": {"origins": "http://localhost:3000"}})
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

#For insert, delete and update


#Person

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

        
@app.route('/deletePerson/<ssn>', methods=['DELETE'])
def delete_person(ssn):
    try:
        person_to_delete = Person.query.get(ssn)

        if person_to_delete:
            db.session.delete(person_to_delete)
            db.session.commit()
            return jsonify({'message': 'Person deleted successfully'}), 200
        else:
            return jsonify({'error': 'Person not found'}), 404

    except Exception as e:
        print('Error deleting person data:', e)
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        db.session.close()


@app.route('/updatePerson/<string:ssn>', methods=['PUT'])
def update_person(ssn):
    try:
        person_to_update = Person.query.get(ssn)

        if not person_to_update:
            return jsonify({'error': 'Person not found'}), 404

        # Update person attributes
        updated_data = request.json
        for key, value in updated_data.items():
            setattr(person_to_update, key, value)

        # Commit the changes to the existing transaction
        db.session.commit()

        return jsonify({'message': 'Person updated successfully'}), 200

    except Exception as e:
        print('Error updating person data:', e)
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error'}), 500

    finally:
        db.session.close()


#Item

class Item(db.Model):
    issn_isbn = db.Column(db.String, primary_key=True)
    version = db.Column(db.String)
    title = db.Column(db.String)
    price = db.Column(db.Numeric)  
    publication_date = db.Column(db.Date)  
    providerid = db.Column(db.String)
    itemtype = db.Column(db.String)

# Endpoint to handle adding person data
@app.route('/addItem', methods=['POST'])
def add_item():
    try:
        new_item = Item(**request.json)
        db.session.add(new_item)
        db.session.commit()
        return jsonify({'issn_isbn': new_item.issn_isbn}), 201
    except Exception as e:
        print('Error adding item data:', e)
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        db.session.close()

@app.route('/deleteItem/<issn_isbn>', methods=['DELETE'])
def delete_item(issn_isbn):
    try:
        item_to_delete = Item.query.get(issn_isbn)

        if item_to_delete:
            db.session.delete(item_to_delete)
            db.session.commit()
            return jsonify({'message': 'item deleted successfully'}), 200
        else:
            return jsonify({'error': 'item not found'}), 404

    except Exception as e:
        print('Error deleting item data:', e)
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        db.session.close()
        
        
@app.route('/updateItem/<string:issn_isbn>', methods=['PUT'])
def update_item(issn_isbn):
    try:
        item_to_update = Item.query.get(issn_isbn)

        if not item_to_update:
            return jsonify({'error': 'item not found'}), 404

        # Update person attributes
        updated_data = request.json
        for key, value in updated_data.items():
            setattr(item_to_update, key, value)

        # Commit the changes to the existing transaction
        db.session.commit()

        return jsonify({'message': 'item updated successfully'}), 200

    except Exception as e:
        print('Error updating item data:', e)
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error'}), 500

    finally:
        db.session.close()        
        
        
        
        
        
        

#For display all tables
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
    result = [{'issn_isbn': member[0], 'advisor': member[1],'institution': member[2]} for member in members]
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
    result = [{'payment_method': member[0], 'fine_type': member[1],'credit_score_update': member[2],'clientid': member[3],'managerid': member[4],'sessionid': member[5],"id": member[6]} for member in members]
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
    result = [{'issn_isbn': member[0], 'publisher': member[1], 'num_pages': member[2],'count': member[3]} for member in members]
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
    result = [{'issn_isbn': member[0],  'journal_conference': member[1]} for member in members]
    return jsonify({'result': result})

@app.route('/retrieve_session_table', methods=['GET'])
def retrieve_session_table():
    cur.execute("SELECT * FROM session")
    members = cur.fetchall()
    result = [{'sessionid': member[0], 'payment_method': member[1], 'cost': member[2],'clientid': member[3],'managerid': member[4],'wkey': member[5],'session_state': member[6],'borrow_date': member[7],'return_date': member[8],'physicalbookid': member[9],'level': member[10]} for member in members]
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



# 5 queries


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
    SELECT retrievel_title('{publication_year}', '{organization}');
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
    date = request.args.get('date')
    payment_method = request.args.get('payment_method')
    sql_query = f'''
    select retrieve_session('{payment_method}', '{date}');
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
    select retrieve_magazine_highest_price('{authorid}');
'''
    cur.execute(sql_query)
    conn.commit()
    outputs = cur.fetchall()
    outputs = [{'issn_isbn':output} for output in outputs]
    #cur.close()
    return jsonify({'result':outputs})


@app.route('/retrieve_client_name', methods=['POST', 'GET'])
def retrieve_client_name():
    '''
    Retrieve name of all client that make more than
    10 session in a specific year
    '''
    #cur = conn.cursor()
    year = request.args.get('year')
    sql_query = f'''
    select retrieve_total_cost('{year}');
'''
    cur.execute(sql_query)
    conn.commit()
    outputs = cur.fetchall()
    outputs = [{ 'fname':output[0], 'lname':output[1]} for output in outputs]
    #cur.close()
    return jsonify({'result':outputs})

#trigger, 
@app.route('/borrow_book', methods=['POST', 'GET'])
def borrow_book():
    attri = request.get_json()
    '''
	physical_bookid VARCHAR(255),
	borrow_date DATE,
	return_date DATE,
    payment_method VARCHAR(255),
	cost_borrow numeric,
	clientid int,
	managerid VARCHAR(255),
	wkey VARCHAR(255)


    call borrow_book('1', '2023-10-12', '2023-11-12', 'Cash', 10.00, 101, '112', 'key_5');
    '''
    physicalbookid = request.args.get('physicalbookid')
    borrow_date = request.args.get('borrow_date')
    return_date = request.args.get('return_date')
    payment_method = request.args.get('payment_method')
    cost_borrow = request.args.get('cost_borrow')
    clientid = request.args.get('clientid')
    managerid = request.args.get('managerid')
    wkey = request.args.get('wkey')
    sql_query = f'''
    call borrow_book({physicalbookid}, {borrow_date}, {return_date}, {payment_method}, {cost_borrow}, {clientid}, {managerid}, {wkey}) 
'''
    cur.execute(sql_query)
    conn.commit()
    #cur.close()
    return 'successfully add borrow book data'








# @app.route('/borrow_book', methods=['POST', 'GET'])
# def borrow_book():
#     borrow_date = request.args.get('borrow_date')

if __name__ == "__main__":
    app.run(host="127.0.0.1", port='6868', debug=True)