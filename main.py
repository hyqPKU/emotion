#coding=utf-8
from flask import Flask, request, make_response, jsonify
import traceback
import json

from config import VERSION, HOST, PORT
from emotion import emotion_classifier

app = Flask(__name__)
@app.route('/v%s/emotion/query' % VERSION, methods=['POST'])
def emotion():
    try:
        data = json.loads(request.get_data())
        query = data['query']
        debug = data['debug'] if 'debug' in data else 0
    except:
        traceback.print_exc()
        return make_response(jsonify({'status': 500, 'info': 'format error'}))

    try:
        polar, confidence, debug_info = emotion_classifier(query)
        result = {'status': 200, 'polar': polar, 'confidence': confidence}
        if debug == 1:
            result['_debug_info'] = debug_info
        return make_response(jsonify(result))
    except BaseException, e:
        traceback.print_exc()
        return make_response(jsonify({'status': 500, 'info': 'system error'}))


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, threaded=True)
