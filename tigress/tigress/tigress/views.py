from pyramid.view import view_config
from .models import *
from mongoengine.errors import NotUniqueError, ValidationError, DoesNotExist
from tigress.libs.utils import *
from tigress.libs.errors import *
from tigress.libs.s3 import S3ConnectionHelper

def error_response(request, error_msg):
  request.response.status = 400
  return error_msg

@view_config(route_name='home', renderer='templates/index.pt')
def home_view(request):
  return {"project": "what"}

def login(request, user):
  request.session['username'] = user.username
  request.session.save()

@view_config(route_name='register', renderer='json')
def register_view(request):
  if request.method == 'POST':
    try:
      username = request.json_body['username']
      password = request.json_body['password']
      verify = request.json_body['verify']
      email = request.json_body['email']
    except Exception:
      raise MissingArgumentFailure("Invalid arguments")

    have_error = False
    params = dict(username = username, email = email)
    if not valid_username(username):
      raise ValidationFailure("That's not a valid username.")

    if not valid_password(password):
      raise ValidationFailure("That wasn't a valid password.")
    elif password != verify:
      raise ValidationFailure("Your passwords didn't match.")

    if not valid_email(email):
      raise ValidationFailure("That's not a valid email.")

    try:
      pw_hash = make_pw_hash(username, password)
      user = User(username=username, password_hash=pw_hash, email=email)
      user.save()
    except ValidationError as e:
      raise ValidationFailure("Invalid Parameters")
    except NotUniqueError as e:
      raise ValidationFailure("Username or email is already taken")
    except Exception as e:
      raise BaseException("Something went wrong while creating account")

    login(request, user)
    return "success"

@view_config(route_name='login', renderer='json')
def login_view(request):
 if request.method == 'POST':
    try:
      username = request.json_body['username']
      password = request.json_body['password']
    except Exception:
      raise MissingArgumentFailure("Invalid arguments")

    try:
      user = User.objects.get(username=username)
    except DoesNotExist:
      raise InvalidCredentials("Invalid Credential")

    if valid_pw(username, password, user.password_hash):
      login(request, user)
    else:
      raise InvalidCredentials("Invalid Password")

    return "success"

@view_config(route_name='logout', renderer='json')
def logout_view(request):
  ''' Maybe return error is not logged in'''
  request.session.clear()
  request.session.save()
  return "success"

@view_config(route_name='upload', renderer='json')
@login_required
def upload_view(request):
  if request.method == 'POST':
    
    fileinput = request.POST['file']
    description = request.POST['description']
    category = request.POST['category']

    item = Item(description=description, tags=["123"])
    item.save()

    conn = S3ConnectionHelper()
    conn.uploadPublicImageFromString(str(item.id), fileinput.value)

    imgLoc = 'http://i.haoliu.net/' + str(item.id);

    params = dict()
    params["imgsrc"] = imgLoc
    return params