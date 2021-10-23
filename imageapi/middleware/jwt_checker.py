import falcon
from falcon_jwt_checker import JwtChecker

jwt_checker = JwtChecker(
    secret='secret_here',  # May be a public key
    algorithm='HS256',
    exempt_routes=['/auth'],  # Routes listed here will not require a jwt
    exempt_methods=['OPTIONS'],  # HTTP request methods listed here will not require a jwt
    audience='api.example.com',
    leeway=30
)