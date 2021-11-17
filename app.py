from app import create_app, db
from app.Model.models import Post, Field, Language

app = create_app()

@app.before_first_request
def initDB(*args, **kwargs):
    db.create_all()
    if Field.query.count() == 0:
        fields =    ['Machine Learning','High Performance Computing', 'Object Oriented Programming', 
                    'Cyber Security', 'Data Analytics', 'Human Computer Interaction', 'Data Mining']
        for f in fields:
            db.session.add(Field(name=f))
        db.session.commit()
    if Language.query.count() == 0:
        languages = ['Javascript','Python', 'C', 'C++', 'C#', 'HTML', 'CSS', 'Ruby', 'Java', 'R', 'Swift', 'PHP', 'Pascal', 'Pearl', 'SQL', 'Go', 'Bash', 'TypeScript']
        for l in languages:
            db.session.add(Language(name=l))
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)