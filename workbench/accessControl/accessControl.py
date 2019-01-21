from flask import Flask, Response, request, jsonify
import time
import random
import string


##
## Configuration
## 
permitted= {
        'client1',
        'client2'
        }


##
## Global variables
##
status = 'READY'
token_current = None


##
## The code
## 
app = Flask(__name__)
random.seed()


#
# Get status. Generate aess token
#
@app.route('/status')
def get_status():
    global status
    global token_current

    args = request.args

    client_id = None
    try:
        client_id = args['AUTH']
    except KeyError:
        pass

    if client_id in permitted:
        if status == 'READY':
            token_current = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))
        return jsonify(dict(
            AUTH=client_id,
            STATUS=status,
            TOKEN=token_current
        ))
    else:
        return jsonify(dict(
            STATUS="FORBIDDEN",
        ))


#
# START TEST PROTECTED ACCESS
#
@app.route('/testprotectedservice')
def work():
    global status
    global token_current
    
    args = request.args
    
    client_id = None
    try:
        client_id = args['AUTH']
    except KeyError:
        pass
    
    if client_id not in permitted:
        return jsonify(dict(
            STATUS="FORBIDDEN",
        ))

    access_token = None
    try:
        access_token = args['TOKEN']
    except:
        pass

    if ((access_token == None) or (access_token != token_current)):
        time.sleep(random.uniform(0,3))

        return jsonify(dict(
            AUTH=client_id,
            STATUS=status,
            ERROR="Wrong access token. Use /status to get the token."
        ))
    token_current = None
    
    return Response(get_data(client_id), mimetype='multipart; boundary=frame')

def get_data(client_id):
    global status
    
    status='BUSY'
    cnt = 0
    while True:
        cnt = cnt + 1
        if cnt < 60:
            time.sleep(1)
            yield (b'--frame\r\n' b'Content-Type: text/html\r\n\r\n' + str.encode(client_id, ) + b'X</br>' + b'\r\n')
        else:
            status = 'READY'
            return
#
# STOP TEST PROTECTED ACCESS
#

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5001, threaded=False)

