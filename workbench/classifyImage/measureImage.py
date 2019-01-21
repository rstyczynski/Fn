from flask import Flask, Response, request, jsonify
import time, random, string, sys, linecache, io
import numpy as np
import cv2

import accessControl


##
## The code
## 
app = Flask(__name__)
random.seed()

def getActiveLine():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    return 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)


#
# Get accessControl.status. Generate aess token
#
@app.route('/status')
def get_status():


    args = request.args

    client_id = None
    try:
        client_id = args['AUTH']
    except KeyError:
        pass

    if client_id in accessControl.permitted:
        if accessControl.status == 'READY':
            accessControl.token_current = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))
        return jsonify(dict(
            AUTH=client_id,
            STATUS=accessControl.status,
            TOKEN=accessControl.token_current
        ))
    else:
        return jsonify(dict(
            STATUS="FORBIDDEN",
        ))


@app.route("/dimensions", methods=['POST'])
def dimensions():
    #
    # access control
    #
        
    args = request.args
    
    client_id = None
    try:
        client_id = args['AUTH']
    except KeyError:
        pass
    
    if client_id not in accessControl.permitted:
        return jsonify(dict(
            STATUS="FORBIDDEN",
        ))

    access_token = None
    try:
        access_token = args['TOKEN']
    except:
        pass

    if ((access_token == None) or (access_token != accessControl.token_current)):
        time.sleep(random.uniform(0,3))

        return jsonify(dict(
            AUTH=client_id,
            STATUS=accessControl.status,
            ERROR="Wrong access token. Use /accessControl.status to get the token."
        ))
    accessControl.token_current = None
    #
    # acess control stop
    #
    try:
        fileBytes = request.files['filedata']
        fileName = request.form['name']
        #
        in_memory_file = io.BytesIO()
        fileBytes.save(in_memory_file)
        fileData = np.frombuffer(in_memory_file.getvalue(), dtype=np.uint8)
        nparr = np.frombuffer(fileData, np.uint8)
        # decode image
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        #
        response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])}
        # encode response using jsonpickle
        response_json = jsonify(response)
        #
        return response_json
    except Exception as ex:
        response = "Exception:" + str(ex) + ' at ' + getActiveLine()
        return response




#
# START TEST PROTECTED ACCESS
#
@app.route('/testprotectedservice')
def work():
    
    args = request.args
    
    client_id = None
    try:
        client_id = args['AUTH']
    except KeyError:
        pass
    
    if client_id not in accessControl.permitted:
        return jsonify(dict(
            STATUS="FORBIDDEN",
        ))

    access_token = None
    try:
        access_token = args['TOKEN']
    except:
        pass

    if ((access_token == None) or (access_token != accessControl.token_current)):
        time.sleep(random.uniform(0,3))

        return jsonify(dict(
            AUTH=client_id,
            STATUS=accessControl.status,
            ERROR="Wrong access token. Use /accessControl.status to get the token."
        ))
    accessControl.token_current = None
    
    return Response(get_data(client_id), mimetype='multipart; boundary=frame')

def get_data(client_id):
    
    accessControl.status='BUSY'
    cnt = 0
    while True:
        cnt = cnt + 1
        if cnt < 60:
            time.sleep(1)
            yield (b'--frame\r\n' b'Content-Type: text/html\r\n\r\n' + str.encode(client_id, ) + b'X</br>' + b'\r\n')
        else:
            accessControl.status = 'READY'
            return
#
# STOP TEST PROTECTED ACCESS
#

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5002, threaded=False)

