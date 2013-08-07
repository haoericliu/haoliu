def error_msg(code, msg):
  return {'error' : [{"message": msg, "code": code}]}

class BaseException(Exception):
  msg = "Something is broken"
  code = 1
  
  def __init__(self, msg):
    self.msg = msg

  def __json__(self, request):
    request.response.status = 500
    return error_msg(self.code, self.msg)

class MissingArgumentFailure(BaseException):
  msg = "Missing argument"
  code = 3

  def __init__(self, msg):
    self.msg = msg

  def __json__(self, request):
    request.response.status = 400
    return error_msg(self.code, self.msg)

class ValidationFailure(BaseException):
    msg = "The arguments are invalid"
    code = 2

    def __init__(self, msg):
      self.msg = msg

    def __json__(self, request):
      request.response.status = 400
      return error_msg(self.code, self.msg)

class InvalidCredentials(BaseException):
    msg = "Invalid Credentials"
    code = 4

    def __json__(self, request):
      request.response.status = 400
      return error_msg(self.code, self.msg)

class UnauthorizedError(BaseException):
    msg = "Not logged in"
    code = 5

    def __json__(self, request):
      request.response.status = 400
      return error_msg(self.code, self.msg) 