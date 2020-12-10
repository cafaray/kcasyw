import os
# import logging.config
from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
import requests
from datetime import datetime, timedelta

app = Flask(__name__) # , template_folder='templates', static_folder='static')
# logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'logging.conf'))
# print('===> logging conf path: ', logging_conf_path)
# logging.config.fileConfig(logging_conf_path)
# log = logging.getLogger(__name__)

app.secret_key = "c29ydGUuYmlvdGVjc2EuY29tL2FkbWluCg=="
app.permanent_session_lifetime= timedelta(hours=1)
app.config['EXPLAIN_TEMPLATE_LOADING'] = True

BASE_URL = "http://biotecsa.com/draw/services/"
# BASE_URL = "http://localhost:8000/"

if __name__=="__main__":
    #log.info('>>>>> Starting server at http://{}/v1/stats/ <<<<<'.format('0.0.0.0:5000'))
    app.run( host='0.0.0.0', port=8080, debug=True )  # debug=True, host='0.0.0.0', port=8080

def validateUser(email: str, password: str):
    return email=='sysadmin@biotecsa.com' and password == 'elPaso01+'        

@app.route('/')
def root():
    return redirect(url_for("login"))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        if validateUser(request.form['email'], request.form['password']):
            session.permanent = False
            user = request.form['email']
            #log.info('===> user logged {}'.format(user))
            session['user'] = user
            return redirect(url_for('home'))
        else:
            flash("Usuario o contraseña incorrecto!", "danger")
            return redirect(url_for("login"))
    else:
        if 'user' in session:
            return redirect(url_for('home'))
        return render_template('/login.html')

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
        #log.info('Application started, getting first service ...')
        response = requests.get(BASE_URL + "draws/")
        #log.info('response: {}'.format(response))
        if response.status_code==200:
            return render_template('index.html', draws=response.json())
        else: 
            session.pop('user', None)
            flash("Vaya, al parecer no hemos logrado conectar con los servicios!", "danger")
            flash("Notifica sobre este error a ofarias@biotecsa.com {}".format(response), "danger")
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/drawinput', methods=['POST', 'GET'])
def draw_input():
    if 'user' in session:
        if request.method=='POST':
            draw = {"title": request.form['title'], "fordate": request.form['fordate']}
            #log.info('===> draw to send: {}'.format(draw))
            response = requests.post(BASE_URL + "draws/", json=draw)
            return redirect(url_for("home"))
        else:
            draw ={"id":-1, "title":"", "fordate":"", "status":"pending"}
            return render_template('drawinput.html', draw=draw)

@app.route('/drawinput/<iddraw>', methods=['POST', 'GET'])
def draw_input_edit(iddraw):
    if 'user' in session:
        # print("requested method:",  request.method)
        if request.method=='POST':
            draw = {"title": request.form['title'], "fordate": request.form['fordate']}
            #log.info('===> draw to send: '.format(draw))
            response = requests.put(BASE_URL + "draws/{}".format(iddraw), json=draw)
            #log.info('===> response: {}'.format(response))
            return redirect(url_for("home"))
        else:
            response = requests.get(BASE_URL + "draws/{}".format(iddraw))
            #log.info('===> response: {}'.format(response))
            return render_template('drawinput.html', draw=response.json())
    else:
        return redirect(url_for('login'))

@app.route('/drawparticipants/<iddraw>', methods=['GET'])
def draw_participants(iddraw: int):
    if 'user' in session:
        response = requests.get(BASE_URL + "draws/{}/participants".format(iddraw))
        draw = requests.get(BASE_URL + "draws/{}".format(iddraw))
        #log.info('===> response.json(): {}'.format(response.json()))
        #log.info('===> draw.json(): {}'.format(draw.json()))
        return render_template('drawparticipants.html', mydraw=draw.json(), drawparticipants=response.json())
    else:
        return redirect(url_for('login'))

@app.route('/drawparticipantinput/<iddraw>', methods=['GET', 'POST'])
def draw_participants_input(iddraw: int):
    if 'user' in session:
        # print("requested method", request.method)
        if request.method=='POST':
            multiselect = request.form.getlist('participants')
            # print("multiselct as is:",multiselect)
            participants = []
            for e in multiselect:
                # print('participant[id]:', e)
                participant = {'id': e}
                participants.append(participant)
            draw_participants = {"participants": participants}
            #log.info('===> drawparticipantinput to send: {}'.format(draw_participants))
            response = requests.post(BASE_URL + "draws/{}/participants".format(iddraw), json=draw_participants)
            #log.info('===> response: {}'.format(response))
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
        response = requests.get(BASE_URL + "draws/{}/gifts".format(iddraw))
        draw = requests.get(BASE_URL + "draws/{}".format(iddraw))
        #log.info('===> response.json(): {}'.format(response.json()))
        #log.info('===> draw.json(): {}'.format(draw.json()))
        return render_template('drawgifts.html', mydraw=draw.json(), drawgifts=response.json())
    else:
        return redirect(url_for('login'))

@app.route('/drawgiftinput/<iddraw>', methods=['GET', 'POST'])
def draw_gift_input(iddraw: int):
    if 'user' in session:
        # print("requested method", request.method)
        if request.method=='POST':
            multiselect = request.form.getlist('gifts')
            # print("multiselct as is:",multiselect)
            gifts = []
            for e in multiselect:
                # print('gift[id]:', e)
                gift = {'id': e}
                gifts.append(gift)
            draw_gifts = {"gifts": gifts}
            #log.info('===> draw_gifts to send: {}'.format(draw_gifts))
            response = requests.post(BASE_URL + "draws/{}/gifts".format(iddraw), json=draw_gifts)
            #log.info('===> response: {}'.format(response))
            return redirect(url_for('home'))
        else:
            draw = getDraw(iddraw)
            gifts = requests.get(BASE_URL + "gifts/")            
            return render_template('drawgiftinput.html', draw=draw.json(), gifts=gifts.json())
    else:
        return redirect(url_for('login'))

@app.route('/drawpublish/<iddraw>')
def set_draw_publish(iddraw: int):
    if 'user' in session:
        draw = getDraw(iddraw).json()
        if draw['status']=='pending' and draw['fordate']<=datetime.today().strftime('%Y-%m-%d'):
            access_code = 'bio{}-{}'.format(iddraw, datetime.today().strftime('%M%s'))
            publish = { "startDate": datetime.today().strftime('%Y-%m-%d'), "access_code": access_code }
            response = requests.post(BASE_URL+'draws/{}/publish'.format(iddraw), json=publish)
            flash("Se ha publicado el evento, el código de acceso que debes enviar para acceder es: {}".format(access_code), "info")
            return redirect(url_for('home'))
        else:
            flash("No es posible publicar el evento, o bien el estatus no es el adecuado o la fecha aún no es adecuada.", "danger")
            return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

@app.route('/drawruning/<iddraw>')
def get_access_code(iddraw: int):
    if 'user' in session:
        response = requests.get(BASE_URL+"draws/{}/publish".format(iddraw))
        if response.status_code==200:
            #log.info('===> get_access_code: {}'.format(response.json()))
            return render_template('drawruning.html', draw=response.json())
        else:
            flash("No es posible localizar el evento, probablemente aún no este publicado", "warning")
            return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

def getDraw(iddraw:int):
    draw = requests.get(BASE_URL + "draws/{}".format(iddraw))
    # print(draw.json())
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
            # print('group to send: ', group)
            response = requests.post(BASE_URL + "groups/", json=group)
            return redirect(url_for("groups"))
        else:
            group ={"id":-1, "groupname":"", "description":"" }
            return render_template('groupinput.html', group=group)

@app.route('/groupinput/<idgroup>', methods=['POST', 'GET'])
def group_input_edit(idgroup):
    if 'user' in session:
        # print("requested method:",  request.method, idgroup)
        if request.method=='POST':
            group = {"groupname": request.form['groupname'], "description": request.form['description']}
            # print('group to send: ', group)
            response = requests.put(BASE_URL + "groups/{}".format(idgroup), json=group)
            # print(response)
            return redirect(url_for("groups"))
        else:
            response = requests.get(BASE_URL + "groups/{}".format(idgroup))
            # print(response)
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
        # print("requested method:",  request.method, idparticipant)
        if request.method=='POST':
            participant = {"participant": request.form['participant'], "email": request.form['email'], "group": { "id": request.form['idgroup'] } }
            #log.info('===> participant to send: {}'.format(participants))
            response = requests.put(BASE_URL + "participants/{}".format(idparticipant), json=participant)
            #log.info('===> response POST: {}'.format(response))
            return redirect(url_for("participants"))
        else:
            response = requests.get(BASE_URL + "participants/{}".format(idparticipant))
            #log.info('===> response GET: {}'.format(response))
            return render_template('participantinput.html', participant=response.json(), groups=getGroups())

# ############################################### #
# routes for manage gifts:                        #
# ############################################### #
@app.route('/gifts')
def gifts():
    if 'user' in session:
        response = requests.get(BASE_URL + "gifts/")
        # print(response.json())
        return render_template('gifts.html', gifts=response.json(), groups=getGroups())
    else:
        return redirect(url_for('login'))

@app.route('/giftinput', methods=['POST', 'GET'])
def gift_input():
    if 'user' in session:
        # print("requested method", request.method)
        if request.method=='POST':
            gift = {"gift": request.form['gift'], "quantity": request.form['quantity'], "description": request.form['description'], "image":'',  "group": { "id": request.form['idgroup'] } }
            #log.info('===> gift to send: {}'.format(gift))
            response = requests.post(BASE_URL + "gifts/", json=gift)
            return redirect(url_for("gifts"))
        else:
            gift = {"id":-1, "gift": "", "quantity": "1", "description": "", "image":"",  "group": { "id": -1 } }
            return render_template('giftinput.html', gift=gift, groups=getGroups())

@app.route('/giftinput/<idgift>', methods=['POST', 'GET'])
def gift_input_edit(idgift):
    if 'user' in session:
        # print("requested method:",  request.method, idgift)
        if request.method=='POST':
            gift = {"gift": request.form['gift'], "quantity": request.form['quantity'], "description": request.form['description'], "image":'',  "group": { "id": request.form['idgroup'] } }
            #log.info('===> gift to send: {}'.format(gift))
            response = requests.put(BASE_URL + "gifts/{}".format(idgift), json=gift)
            #log.info('===> response: {}'.format(response))
            return redirect(url_for("gifts"))
        else:
            response = requests.get(BASE_URL + "gifts/{}".format(idgift))
            #log.info('===> response GET: {}'.format(response))
            return render_template('giftinput.html', gift=response.json(), groups=getGroups())
    else:
        return redirect(url_for('/'))

@app.route('/gifts/<idgift>/loadimages/', methods=['POST'])
def gift_load_image(idgift: int):
    if 'user' in session:        
        file = request.files['file']
        #log.info('===> uploading file: {}'.format(file.filename))
        files = {'file': (file.filename, file.read())}
        response = requests.post(BASE_URL+'gifts/{}/uploadfile/'.format(idgift), files=files)
        #log.info('===> response: {}'.format(response))
        return redirect(url_for("gifts"))
    else:
        return redirect(url_for('/'))

def getGroups():
    group_response = requests.get(BASE_URL + 'groups/')
    return group_response.json()


# ############################################### #
# routes for events:                              #
# ############################################### #

@app.route('/events/selection/<alias>')
def events_selection(alias: str):
    if 'participant' in session and 'draw' in session:
        #log.info('Selected gift by user{}: {}'.format(session['participant'], alias))
        response = requests.post(BASE_URL+'events/{}/selections?alias={}&participantid={}'.format(session['draw'], alias, session['participantid']))
        #log.info('response: {}'.format(response))
        if response.status_code==201:
            resgift = requests.get(BASE_URL+'events/{}/selections/participants/{}'.format(session['draw'], session['participantid']))
            if resgift.status_code==200:
                data = resgift.json()
                flash("Feliciades has seleccionado tu premio, mira los detalles e imprime esta pantalla como comprobante!", "success")
                return render_template('/event/selection.html', data= data)
        else:
            flash("Vaya al parecer no se ha logrado registrar el premio, selecciona otro!", "warning")                
            return redirect(url_for('events_home'))
    else:
        # need to login
        return redirect(url_for('events_login'))

@app.route('/events/home')
def events_home():
    if 'participant' in session and 'draw' in session:
        # here is the participant, look for available gifts:
        res = requests.get(BASE_URL+'events/{}/selections?participantid={}'.format(session['draw'], session['participantid']))
        #log.info('here is the participant, look for available gifts: {}'.format(res))
        if res.status_code==200:            
            data = res.json()
            #log.info('resposne: {}'.format(data))
            gifts = data['gifts']
            if len(gifts)<=0:
                flash("Vaya al parecer no se han localizado premios disponibles!", "warning")                
                return render_template('/event/index.html')
            else:
                flash("Selecciona un premio antes de que alguien más lo tome!", "success")                
                return render_template('/event/index.html', gifts=gifts)

        else:
            flash("Vaya hubo un fallo al recuperar los premios!", "warning")
            return render_template('event/index.html')
    else:
        # need to login
        return redirect(url_for('events_login'))

@app.route('/events/', methods=['GET', 'POST'])
def events_login():
    if request.method=='POST':
        # do login
        participant = request.form['email']
        access_code = request.form['password']
        req = { 'participant': participant, 'access_code': access_code }
        # print('req', req)
        response = requests.get(BASE_URL+'events/login?participant={}&access_code={}'.format(participant, access_code))
        if response.status_code==200:
            session.permanent = True
            res = response.json()
            # print('res', res)
            session['participant'] = res['participants'][0]['participant']
            session['participantid'] = res['participants'][0]['id']
            session['email'] = res['participants'][0]['email']
            session['draw'] = res['draw']['id']            
            session['data'] = res
            #log.info('VALUES at SESSION:\n\tparticipantid= {}\n\tparticipant={}\n\temail = {}\n\tdraw={}'.format(session['participantid'], session['participant'],session['email'],session['draw']))
            return redirect(url_for('events_home'))
        else:
            flash("Usuario o contraseña incorrecto!", "danger")
            return render_template('event/login.html')
    else:
        if 'participant' in session and 'draw' in session:
            return redirect(url_for('events_home'))
        
    return render_template('event/login.html')

@app.route('/events/logout')
def events_logout():
    session.pop('participant', None)
    session.pop('draw', None)
    session.pop('data', None)
    flash("Has salido de la sesión!", "info")
    return redirect(url_for('events_login'))
