from flask import Flask, jsonify, request

# initialize our Flask application

app= Flask(__name__)
@app.route("/name", methods=["POST"])
def setName():
    if request.method=='POST':
        posted_data = request.get_json()
        if 'data' in posted_data:
            with open("")
            data = posted_data['data']
            return jsonify(str("Successfully stored  " + str(data)))
        else:
            return jsonify('error')

#  main thread of execution to start the server
if __name__=='__main__':
    app.run(debug=True)