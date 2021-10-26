from app import create_app, db
from app.Model.models import Post, Field

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

if __name__ == "__main__":
    app.run(debug=True)