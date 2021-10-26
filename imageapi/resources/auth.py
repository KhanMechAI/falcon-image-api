import falcon
from spectree import Response

from ..db.models import User
from ..schemas.auth import AlreadyRegisteredSchema, LoginSchema, RegisterSchema
from ..schemas.base_api_spec import api


class RegisterResource:

    @api.validate(resp=Response(HTTP_201=None, HTTP_409=AlreadyRegisteredSchema), json=RegisterSchema)
    def on_post(self, req, resp):
        """
        Register new user

        Register new user for ImageAPI use
        """
        user_data = req.media
        with req.context.session as session:
            if session.query(User).filter_by(email=user_data["email"]).first():
                raise falcon.HTTPConflict(
                    title="User already exists",
                    description="This email is already associated with another account. Please try registering again"
                )
            new_user = User(email=user_data["email"], password=user_data["password"])
            session.add(new_user)
            session.commit()
        resp.status = falcon.HTTP_201


class LoginResource:

    @api.validate(resp=Response(HTTP_200=None, HTTP_403=None), json=LoginSchema)
    def on_post(self, req, resp):
        """
        User Login

        User login route
        """
        data = req.media

        if (user_id := self.is_valid_user(data["email"], data["password"], req)):
            token = req.context.auth.create_token(data["email"])
            # resp.append_header("Set-Cookie", dict(name="auth_token", value=token,))
            resp.set_cookie(
                name="auth_token",
                value=token,
                max_age=req.context.auth.timedelta,
                # domain=req.forwarded_host,
                path="/",
                secure=False,  # Excluding for the moment
                http_only=False,  # Excluding for the moment
                same_site="Lax"
            )
        else:
            raise falcon.HTTPUnauthorized(
                title="Login Failed",
                description="Bad email or password."
            )

        resp.status = falcon.HTTP_200

    def is_valid_user(self, user_email: str, password: str, req) -> [bool, int]:
        with req.context.session as session:
            if user := session.query(User).filter_by(email=user_email).first():
                if user.check_password(password=password):
                    return user.id
                return False
            return False
