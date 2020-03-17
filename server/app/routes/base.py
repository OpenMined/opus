from flask import Response

def init_base_routes(app):
  @app.route('/')
  def index():
    return Response("Hello, world!")
