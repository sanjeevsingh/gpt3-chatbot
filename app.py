import os
from dotenv import load_dotenv
from flask import Flask, request, session, render_template, jsonify, make_response, json
from flask_cors import CORS
from twilio.twiml.messaging_response import MessagingResponse
from jabebot import ask, append_interaction_to_chat_log
from pusher import pusher
load_dotenv()
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
# configure pusher object
pusher = pusher.Pusher(
app_id=os.getenv('PUSHER_APP_ID'),
key=os.getenv('PUSHER_APP_KEY'),
secret=os.getenv('PUSHER_SECRET'),
cluster=os.getenv('PUSHER_CLUSTER'),
ssl=True)
# if for some reason your conversation with Jabe gets weird, change the secret key
app.config['SECRET_KEY'] = 'any-random-string'
@app.route('/kobot', methods=['POST'])
def kobot():
 incoming_msg = request.values['Body']
 print(incoming_msg)
 chat_log = session.get('chat_log')
 answer = ask(incoming_msg, chat_log)
 session['chat_log'] = append_interaction_to_chat_log(incoming_msg, answer,
 chat_log)
 msg = MessagingResponse()
 msg.message(answer)
 return str(msg)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/new/guest', methods=['POST'])
def guestUser():
    data = request.json
    print(data)
    pusher.trigger(u'general-channel', u'new-guest-details', { 
        'name' : data['name'], 
        'email' : data['email']
        })    
    return json.dumps(data)

@app.route("/pusher/auth", methods=['POST'])
def pusher_authentication():
    print(request.form['channel_name'],request.form['socket_id'])
    auth = pusher.authenticate(channel=request.form['channel_name'],socket_id=request.form['socket_id'])
    return json.dumps(auth)

@app.route("/webhook", methods=['POST'])
def pusher_webhook():
  # pusher_client is obtained through pusher_client = pusher.Pusher( ... )
  webhook = pusher.validate_webhook(
    key=request.headers.get('X-Pusher-Key'),
    signature=request.headers.get('X-Pusher-Signature'),
    body=request.data
  )

  for event in webhook['events']:
      print("Channel :" + event["channel"] + " Event : " + event["name"])

  return "ok"
if __name__ == '__main__':
 app.run(debug=True)