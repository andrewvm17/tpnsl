from flask import Flask
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import render_template
from forms import RegistrationForm, MatchReportForm
from flask import request, redirect, url_for



cred = credentials.Certificate("tpnsl-c0752-firebase-adminsdk-gstnb-2caeeab7f4.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'bç5\xdc\xe3*\x1eZ\x10\xd0\x96\x85\xa9\x15\xce<\x84\xfa'


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    form = MatchReportForm()
    if form.validate_on_submit():
        # Save the data to Firebase
        doc_ref = db.collection('match_reports').document()
        doc_ref.set({
            'home_team': form.home_team.data,
            'home_team_score': form.home_team_score.data,
            'away_team': form.away_team.data,
            'away_team_score': form.away_team_score.data
        })
        flash('Match report for {} vs. {} submitted'.format(form.home_team.data, form.away_team.data))
        return redirect(url_for('index'))
    return render_template('admin.html', title='Report Match', form=form)

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