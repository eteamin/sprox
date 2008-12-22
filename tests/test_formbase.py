from sprox.formbase import FormBase
from base import setup_database
from model import User
from sprox.widgetselector import SAWidgetSelector
from sprox.metadata import FieldsMetadata
from nose.tools import raises, eq_


session = None
engine  = None
connection = None
trans = None
def setup():
    global session, engine, connection, trans
    session, engine, connection = setup_database()

class UserForm(FormBase):
    __entity__ = User

class TestFormBase:
    def setup(self):
        self.base = UserForm(session)

    def test_create(self):
        pass

    def test__fields__(self):
        eq_(['created', 'display_name', 'email_address', 'groups', 'password', 'sprox_id', 'town', 'town_id', 'user_id', 'user_name', 'visit_identity'],
             sorted(self.base.__fields__))

    def test__widget__(self):
        rendered = self.base.__widget__()
        assert """<td class="fieldcol">
                <input type="submit" class="submitbutton" value="Submit" />
            </td>""" in rendered, rendered

    def test_require_field(self):
        class RegistrationForm(FormBase):
            __entity__ = User
            __require_fields__ = ['user_name']

        form = RegistrationForm(session)
        eq_(form.__widget__.children['user_name'].validator.not_empty, True)
