from models import User, db, Feedback
from app import app

# Create all tables
# db.drop_all()
# db.create_all()

# If table isn't empty, empty it
# User.query.delete()
Feedback.query.delete()

#Add Feedback

comment1 = Feedback(title="You shouldn't eat asphalt", content="Do what you want.  Whoa be it for me to tell you what you can and cannot do.  But asphalt has no nutritional value.  Just sayin'", username="docvolz3")

db.session.add(comment1)

db.session.commit()