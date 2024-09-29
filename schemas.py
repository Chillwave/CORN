from app import ma
from models import User, Issue

# User schema
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

# Issue schema
class IssueSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Issue
