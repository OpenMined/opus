from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flasgger import Swagger, APISpec, fields
from flask_marshmallow import Marshmallow

from .models import Users

ma = Marshmallow()


class ErrorSchema(ma.Schema):
    message = fields.Str(required=True)


class UserSchema(ma.ModelSchema):
    class Meta:
        model = Users


definitions = [ErrorSchema, UserSchema]


def configure_spec(app):
    ma.init_app(app)
    app.config['SWAGGER'] = {'uiversion': 3}
    spec = APISpec(
        title='Private Identity Server',
        version='0.0.0',
        openapi_version='2.0',
        plugins=[
            FlaskPlugin(),
            MarshmallowPlugin(),
        ],
    )
    template = spec.to_flasgger(
        app,
        definitions=definitions
    )
    Swagger(app, template=template)
