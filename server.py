import os
import binascii
import md5
import urlparse
from flask import Flask, request, abort, render_template

app = Flask(__name__)

def sign_req(values, secret):
    s = secret
    for k, v in sorted(values.items()):
        s += k
        s += v
    return md5.MD5(s).hexdigest()

USER_ID = 42
USER_NAME = "Jack"
API_KEY = binascii.hexlify(os.urandom(16))
API_SECRET = binascii.hexlify(os.urandom(16))

@app.route('/')
def show_info():
    req = {
        "method": "vimeo.test.login",
        "api_key": API_KEY
    }

    return render_template('info.html',
        user_id=USER_ID, api_key=API_KEY, user_name=USER_NAME,
        api_sig=sign_req(req, API_SECRET))

@app.route('/api', methods=['POST'])
def handle_api():
    values = dict(urlparse.parse_qsl(request.get_data()))

    if not 'api_sig' in values: abort(400)
    if not 'api_key' in values: abort(400)
    if not 'method' in values: abort(400)

    if values['api_key'] != API_KEY: abort(403)
    api_sig = values['api_sig']
    del values['api_sig']
    if sign_req(values, API_SECRET) != api_sig: abort(403)

    if values["method"] == "vimeo.test.login":
        return render_template("user.xml", user_id=USER_ID, user_name=USER_NAME)

    elif values["method"] == "vimeo.videos.setFavorite":
        if not 'video_id' in values: abort(400)
        if not 'favorite' in values: abort(400)

        if values["video_id"] != '1337': abort(404)

        return render_template("ok.xml")

    else:
        abort(404)


if __name__ == '__main__':
    app.debug = True
    app.run(port=4242)
