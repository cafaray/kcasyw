from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
import requests
from datetime import datetime, timedelta

app = Flask("__main__")
app.secret_key = "c29ydGUuYmlvdGVjc2EuY29tL2FkbWluCg=="
app.permanent_session_lifetime= timedelta(hours=1)

BASE_URL = "http://127.0.0.1:8000/"

def validateUser(email: str, password: str):
    return email=='sysadmin@biotecsa.com' and password == 'elPaso01+'        

@app.route('/')
def root():
    return redirect(url_for("login"))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        if validateUser(request.form['email'], request.form['password']):
            session.permanent = True
            user = request.form['email']
            print(user)
            session['user'] = user
            return redirect(url_for('home'))
        else:
            flash("Usuario o contraseña incorrecto!", "danger")
            return redirect(url_for("login"))
    else:
        if 'user' in session:
            return redirect(url_for('home'))
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Has salido de la sesión!", "info")
    return redirect(url_for('login'))

# ############################################### #
# routes for manage draws:                        #
# ############################################### #
@app.route('/home')
def home():
    if 'user' in session:
        response = requests.get(BASE_URL + "draws/")
        # print(response.json())
        return render_template('index.html', draws=response.json())
    else:
        return redirect(url_for('login'))

@app.route('/drawinput', methods=['POST', 'GET'])
def draw_input():
    if 'user' in session:
        if request.method=='POST':
            draw = {"title": request.form['title'], "fordate": request.form['fordate']}
            print('draw to send: ', draw)
            response = requests.post(BASE_URL + "draws/", json=draw)
            return redirect(url_for("home"))
        else:
            draw ={"id":-1, "title":"", "fordate":"", "status":"pending"}
            return render_template('drawinput.html', draw=draw)

@app.route('/drawinput/<iddraw>', methods=['POST', 'GET'])
def draw_input_edit(iddraw):
    if 'user' in session:
        print("requested method:",  request.method)
        if request.method=='POST':
            draw = {"title": request.form['title'], "fordate": request.form['fordate']}
            print('draw to send: ', draw)
            response = requests.put(BASE_URL + "draws/{}".format(iddraw), json=draw)
            print(response)
            return redirect(url_for("home"))
        else:
            response = requests.get(BASE_URL + "draws/{}".format(iddraw))
            print(response)
            return render_template('drawinput.html', draw=response.json())
    else:
        return redirect(url_for('login'))

@app.route('/drawparticipants/<iddraw>', methods=['GET'])
def draw_participants(iddraw: int):
    if 'user' in session:
        response = requests.get(BASE_URL + "draws/{}/participants/".format(iddraw))
        draw = requests.get(BASE_URL + "draws/{}".format(iddraw))
        print(response.json())
        print(draw.json())
        return render_template('drawparticipants.html', mydraw=draw.json(), drawparticipants=response.json())
    else:
        return redirect(url_for('login'))

@app.route('/drawparticipantinput/<iddraw>', methods=['GET', 'POST'])
def draw_participants_input(iddraw: int):
    if 'user' in session:
        print("requested method", request.method)
        if request.method=='POST':
            multiselect = request.form.getlist('participants')
            print("multiselct as is:",multiselect)
            participants = []
            for e in multiselect:
                print('participant[id]:', e)
                participant = {'id': e}
                participants.append(participant)
            draw_participants = {"participants": participants}
            print("data to send: ", draw_participants)
            response = requests.post(BASE_URL + "draws/{}/participants".format(iddraw), json=draw_participants)
            print(response)
            return redirect(url_for('home'))
        else:
            draw = getDraw(iddraw)
            participants = requests.get(BASE_URL + "participants/")            
            return render_template('drawparticipantinput.html', draw=draw.json(), participants=participants.json())
    else:
        return redirect(url_for('login'))

@app.route('/drawgifts/<iddraw>', methods=['GET'])
def draw_gifts(iddraw: int):
    if 'user' in session:
        response = requests.get(BASE_URL + "draws/{}/gifts/".format(iddraw))
        draw = requests.get(BASE_URL + "draws/{}".format(iddraw))
        print(response.json())
        print(draw.json())
        return render_template('drawgifts.html', mydraw=draw.json(), drawgifts=response.json())
    else:
        return redirect(url_for('login'))

@app.route('/drawgiftinput/<iddraw>', methods=['GET', 'POST'])
def draw_gift_input(iddraw: int):
    if 'user' in session:
        print("requested method", request.method)
        if request.method=='POST':
            multiselect = request.form.getlist('gifts')
            print("multiselct as is:",multiselect)
            gifts = []
            for e in multiselect:
                print('gift[id]:', e)
                gift = {'id': e}
                gifts.append(gift)
            draw_gifts = {"gifts": gifts}
            print("data to send: ", draw_gifts)
            response = requests.post(BASE_URL + "draws/{}/gifts".format(iddraw), json=draw_gifts)
            print(response)
            return redirect(url_for('home'))
        else:
            draw = getDraw(iddraw)
            gifts = requests.get(BASE_URL + "gifts/")            
            return render_template('drawgiftinput.html', draw=draw.json(), gifts=gifts.json())
    else:
        return redirect(url_for('login'))

@app.route('/drawpublish/<iddraw>')
def set_draw_publish(iddraw: int):
    draw = getDraw(iddraw).json()
    if draw['status']=='pending' and draw['fordate']<=datetime.today().strftime('%Y-%m-%d'):
        access_code = 'bio{}-{}'.format(iddraw, datetime.today().strftime('%M%s'))
        publish = { "startDate": datetime.today().strftime('%Y-%m-%d'), "access_code": access_code }
        response = requests.post(BASE_URL+'draws/{}/publish'.format(iddraw), json=publish)
        return redirect(url_for('home'))
    else:
        flash("No es posible publicar el evento, o bien el estatus no es el adecuado o la fecha aún no es adecuada.", "danger")
        return redirect(url_for('home'))

def getDraw(iddraw:int):
    draw = requests.get(BASE_URL + "draws/{}".format(iddraw))
    print(draw.json())
    return draw

# ############################################### #
# routes for manage groups:                       #
# ############################################### #
@app.route('/groups')
def groups():
    if 'user' in session:
        response = requests.get(BASE_URL + "groups/")
        # print(response.json())
        return render_template('groups.html', groups=response.json())
    else:
        return redirect(url_for('login'))

@app.route('/groupinput', methods=['POST', 'GET'])
def group_input():
    if 'user' in session:
        if request.method=='POST':
            group = {"groupname": request.form['groupname'], "description": request.form['description']}
            print('group to send: ', group)
            response = requests.post(BASE_URL + "groups/", json=group)
            return redirect(url_for("groups"))
        else:
            group ={"id":-1, "groupname":"", "description":"" }
            return render_template('groupinput.html', group=group)

@app.route('/groupinput/<idgroup>', methods=['POST', 'GET'])
def group_input_edit(idgroup):
    if 'user' in session:
        print("requested method:",  request.method, idgroup)
        if request.method=='POST':
            group = {"groupname": request.form['groupname'], "description": request.form['description']}
            print('group to send: ', group)
            response = requests.put(BASE_URL + "groups/{}".format(idgroup), json=group)
            print(response)
            return redirect(url_for("groups"))
        else:
            response = requests.get(BASE_URL + "groups/{}".format(idgroup))
            print(response)
            return render_template('groupinput.html', group=response.json())

# ############################################### #
# routes for manage participants:                 #
# ############################################### #
@app.route('/participants')
def participants():
    if 'user' in session:
        response = requests.get(BASE_URL + "participants/")
        # print(response.json())
        return render_template('participants.html', participants=response.json(), groups=getGroups())
    else:
        return redirect(url_for('login'))

@app.route('/participantinput', methods=['POST', 'GET'])
def participant_input():
    if 'user' in session:
        if request.method=='POST':
            participant = {"participant": request.form['participant'], "email": request.form['email'], "group": { "id": request.form['idgroup'] } }
            print('participant to send: ', participants)
            response = requests.post(BASE_URL + "participants/", json=participant)
            return redirect(url_for("participants"))
        else:
            participant ={"id":-1, "participant":"", "email":"", "group": { "id": 1 } }            
            return render_template('participantinput.html', participant=participant, groups=getGroups())

@app.route('/participantinput/<idparticipant>', methods=['POST', 'GET'])
def participant_input_edit(idparticipant):
    if 'user' in session:
        print("requested method:",  request.method, idparticipant)
        if request.method=='POST':
            participant = {"participant": request.form['participant'], "email": request.form['email'], "group": { "id": request.form['idgroup'] } }
            print('participant to send: ', participants)
            response = requests.put(BASE_URL + "participants/{}".format(idparticipant), json=participant)
            print(response)
            return redirect(url_for("participants"))
        else:
            response = requests.get(BASE_URL + "participants/{}".format(idparticipant))
            print(response)
            return render_template('participantinput.html', participant=response.json(), groups=getGroups())

# ############################################### #
# routes for manage gifts:                        #
# ############################################### #
@app.route('/gifts')
def gifts():
    if 'user' in session:
        response = requests.get(BASE_URL + "gifts/")
        print(response.json())
        return render_template('gifts.html', gifts=response.json(), groups=getGroups())
    else:
        return redirect(url_for('login'))

@app.route('/giftinput', methods=['POST', 'GET'])
def gift_input():
    if 'user' in session:
        print("requested method", request.method)
        if request.method=='POST':
            gift = {"gift": request.form['gift'], "quantity": request.form['quantity'], "description": request.form['description'], "image":'',  "group": { "id": request.form['idgroup'] } }
            print('gift to send: ', gift)
            response = requests.post(BASE_URL + "gifts/", json=gift)
            return redirect(url_for("gifts"))
        else:
            gift = {"id":-1, "gift": "", "quantity": "", "description": "", "image":"",  "group": { "id": -1 } }
            return render_template('giftinput.html', gift=gift, groups=getGroups())

@app.route('/giftinput/<idgift>', methods=['POST', 'GET'])
def gift_input_edit(idgift):
    if 'user' in session:
        print("requested method:",  request.method, idgift)
        if request.method=='POST':
            gift = {"gift": request.form['gift'], "quantity": request.form['quantity'], "description": request.form['description'], "image":request.form['image'],  "group": { "id": request.form['idgroup'] } }
            print('gift to send: ', gift)
            response = requests.put(BASE_URL + "gifts/{}".format(idgift), json=gift)
            print(response)
            return redirect(url_for("gifts"))
        else:
            response = requests.get(BASE_URL + "gifts/{}".format(idgift))
            print(response)
            return render_template('giftinput.html', gift=response.json(), groups=getGroups())
    else:
        return redirect(url_for('/'))

@app.route('/gifts/<idgift>/loadimages/', methods=['POST'])
def gift_load_image(idgift: int):
    if 'user' in session:        
        file = request.files['file']
        print(file.filename)        
        files = {'file': (file.filename, file.read())}
        response = requests.post(BASE_URL+'gifts/{}/uploadfile/'.format(idgift), files=files)
        print(response)
        return redirect(url_for("gifts"))
    else:
        return redirect(url_for('/'))

def getGroups():
    group_response = requests.get(BASE_URL + 'groups/')
    return group_response.json()


if __name__=="__main__":
    app.run(debug=True)