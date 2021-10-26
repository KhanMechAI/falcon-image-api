from datetime import datetime
from typing import List

import falcon
import jwt

from db.models import User


class AuthMiddleware:

    def __init__(self, key: str, algorithm: str, timedelta: [int, float], exempt_routes: List[str]):
        self.key = key
        self.algorithm = algorithm
        self.timedelta = timedelta
        self.exempt_routes = set(exempt_routes)

    def create_token(self, user_email) -> str:
        return jwt.encode(
            {
                "exp": datetime.utcnow().timestamp() + self.timedelta,
                "email": user_email
            },
            self.key,
            algorithm=self.algorithm
        )

    def check_token(self, token) -> str:
        try:
            data = jwt.decode(token, self.key, algorithms=self.algorithm, options={"require": ["exp", "email"]})
        except jwt.ExpiredSignatureError as e:
            raise falcon.HTTPUnauthorized(
                title="Authentication required",
                description="Token expired, please re-authenticate"
            )
        return data["email"]

    def valid_token(self, token: str, req) -> bool:
        user_email = self.check_token(token)

        with req.context.session as session:
            if session.query(User).filter_by(email=user_email).first():
                req.context.user_email = user_email
                return True
            return False

    def process_request(self, req, resp):

        req.context.auth = self
        for route in self.exempt_routes:
            if route in req.path:
                return

        token = req.get_cookie_values("auth_token")

        if token is None:
            description = ("Please provide an auth token "
                           "as part of the request.")

            raise falcon.HTTPUnauthorized(
                title="Auth token required",
                description=description,
            )

        token = token[0]
        if not self.valid_token(token, req):
            description = ("The provided auth token is not valid. "
                           "Please request a new token and try again.")

            raise falcon.HTTPUnauthorized(
                title="Authentication required",
                description=description,

            )
