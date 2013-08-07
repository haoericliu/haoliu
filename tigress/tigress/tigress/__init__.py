from pyramid.config import Configurator
from mongoengine import *
from mongoengine.errors import DoesNotExist
from pyramid.view import notfound_view_config, view_config
from tigress.libs.errors import *
from pyramid_beaker import session_factory_from_settings
from .models import User

@notfound_view_config(append_slash=True, renderer='json')
def notfound(request):
    return {"error_code": "404", "error_msg" : "The URL is not recognized."}

"""http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/views.html#using-special-exceptions-in-view-callables

This is the catch up exception handler so as to not leak any info


@view_config(context=Exception, renderer='json')
def catchall_view(exc, request):
    #log or do other stuff to exc...
 """
 
''' Base Exception Handler for all of tigress '''
@view_config(context=BaseException, renderer='json')
def error_view(exc, request):
    return exc

def get_user(request):
    try:
        username = request.session['username']
        user = User.objects.get(username=username)
        return user
    except DoesNotExist:
        user = None
    except Exception:
        user = None

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    
    config = Configurator(settings=settings)

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('register', '/register')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('upload', '/upload')
    config.scan()

    ''' set session factory '''
    session_factory = session_factory_from_settings(settings)
    config.set_session_factory(session_factory)

    ''' make user variable available in request '''
    config.add_request_method(get_user, 'user', reify=True)

    ''' Connect to mongodb '''
    connect('tigress') 

    return config.make_wsgi_app()
