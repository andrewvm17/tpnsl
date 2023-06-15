from flask import Flask
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import render_template
from forms import RegistrationForm
from flask import request, redirect, url_for



cred = credentials.Certificate("tpnsl-c0752-firebase-adminsdk-gstnb-2caeeab7f4.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'bç5\xdc\xe3*\x1eZ\x10\xd0\x96\x85\xa9\x15\xce<\x84\xfa'




@app.route("/registration", methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        ##date_of_birth = datetime.strptime(form.date_of_birth.data, "%d/%m/%Y")
        doc_ref = db.collection('registrations').document()
        doc_ref.set({
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'school': form.school.data,
            ##'date_of_birth': date_of_birth,
            'email': form.email.data
        })
        return redirect(url_for('home'))
    return render_template('registration.html', title='Register', form=form)



@app.route('/')
def home():
    return render_template('home.html', title='Home')


if __name__ == '__main__':
    app.run(debug=True)