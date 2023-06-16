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
        
        home_team = form.home_team.data
        print(home_team)
        away_team = form.away_team.data
        home_team_score = int(form.home_team_score.data)
        away_team_score = int(form.away_team_score.data)
        division = form.division.data
        season = 'Spring2023'  # Manually set season

        # Assume that db is your initialized Firestore client
        collection_ref = db.collection('seasons').document(season).collection('divisions').document(division).collection('standings')

        # Get all documents in the collection
        docs = collection_ref.stream()

        # Iterate through each document
        for doc in docs:
            doc_data = doc.to_dict()
            
            # If 'wins' field does not exist, add it
            if 'wins' not in doc_data:
                doc_data['wins'] = 0
            
            # Do the same for 'losses' and 'draws' fields
            if 'losses' not in doc_data:
                doc_data['losses'] = 0
            if 'draws' not in doc_data:
                doc_data['draws'] = 0

            if 'points' not in doc_data:
                doc_data['points'] = 0

            # Update the document with the new fields
            collection_ref.document(doc.id).set(doc_data)

        # Determine result
        if home_team_score > away_team_score:
            home_result = 'win'
            away_result = 'loss'
        elif home_team_score < away_team_score:
            home_result = 'loss'
            away_result = 'win'
        else:
            home_result = away_result = 'draw'

        match_report_data = {
            'home_team': home_team,
            'home_team_score': home_team_score,
            'home_result': home_result,
            'away_team': away_team,
            'away_team_score': away_team_score,
            'away_result': away_result,
            'division': division,
        }
        
        # Save match report to match_reports sub-collection of the correct division
        match_report_ref = db.collection('seasons').document(season).collection('divisions').document(division).collection('match_reports').document()
        match_report_ref.set(match_report_data)

        # Update standings
        # Assumes that each team has a document in the standings collection with the same name as the team
        standings_ref = db.collection('seasons').document(season).collection('divisions').document(division).collection('standings')
        home_team_standings = standings_ref.document(home_team).get().to_dict()
        away_team_standings = standings_ref.document(away_team).get().to_dict()

        # Update standings based on result
        if home_result == 'win':
            home_team_standings['wins'] += 1
            home_team_standings['points'] += 3
            away_team_standings['losses'] += 1
        elif home_result == 'loss':
            home_team_standings['losses'] += 1
            away_team_standings['wins'] += 1
            away_team_standings['points'] += 3
        else:
            home_team_standings['draws'] += 1
            home_team_standings['points'] += 1
            away_team_standings['draws'] += 1
            away_team_standings['points'] += 1

        # Save updated standings back to database
        standings_ref.document(home_team).set(home_team_standings)
        standings_ref.document(away_team).set(away_team_standings)

        return redirect(url_for('admin'))
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

@app.route('/standings', methods=['GET'])
def standings():
    season = 'Spring2023'  # Manually set season
    division = 'coed10'  # Replace with your division name
    standings_ref = db.collection('seasons').document(season).collection('divisions').document(division).collection('standings')
    standings = [{'name': doc.id, **doc.to_dict()} for doc in standings_ref.stream()]
    standings.sort(key=lambda x: x['points'], reverse=True)
    return render_template('standings.html', title='Standings', standings=standings)


@app.route('/')
def home():
    return render_template('home.html', title='Home')


if __name__ == '__main__':
    app.run(debug=True)