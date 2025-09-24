from app.domain.entities.user import User
from app.domain.services.user_singup import UserSignUp
from supertokens_python.recipe.emailpassword.asyncio import sign_up


class SuperTokensUserSignUp(UserSignUp):
    async def register(self, email: str, password: str):
        try: 
            await sign_up(
                email=email, 
                password=password,
                tenant_id='public')
        except Exception as e:
            return e
