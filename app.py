from flask import Flask, jsonify,request,redirect,render_template
import pymongo
from flask.helpers import url_for
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)
cors = CORS(app)
val = os.environ['mongouri']
myclient = pymongo.MongoClient(val)
mydb = myclient["ServiceInfo"]
currentCollection = mydb["ServiceInfo"]



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/services', methods = ['GET'])
def retrieveAll():
    holder = list()
    for i in currentCollection.find():
        holder.append({'name':i['name'], 'category' : i['category'], 'description' : i['description']})
    return jsonify(holder)

@app.route('/services/<name>', methods = ['GET'])
@cross_origin()
def retrieveFromName(name):
    data = currentCollection.find_one({"name" : name})
    return jsonify({'name' : data['name'], 'category' : data['category'], 'description' : data['description']})

@app.route('/postData', methods = ['POST'])
def postData():
    name = request.json['name']
    category = request.json['category']
    description = request.json['description']
    currentCollection.insert_one({'name' : name, 'category' : category, 'description' : description})
    return jsonify({'name' : name, 'category' : category, 'description' : description})

@app.route('/deleteData/<name>', methods = ['DELETE'])
def deleteData(name):
    currentCollection.delete_one({'name' : name})
    return redirect(url_for('retrieveAll'))

@app.route('/update/<name>', methods = ['PUT'])
def updateData(name):
    updatedName = request.json['name']
    currentCollection.update_one({'name':name}, {"$set" : {'name' : updatedName}})
    return redirect(url_for('retrieveAll'))

if __name__ == '__main__':
    app.run(debug=True)
