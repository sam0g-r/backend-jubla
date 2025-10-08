import os
from supertokens_python import init, InputAppInfo, SupertokensConfig
from supertokens_python.recipe import session, emailpassword
from app.shared.config.settings import settings


def init_supertokens():
    init(
        app_info=InputAppInfo(
            app_name=settings.PROJECT_NAME,
            api_domain='https://p01--backend-jubla--48898slpwtw6.code.run',
            website_domain='http://localhost:3000', #jubla.lat.co
            api_base_path='/api/v1/auth',
            website_base_path='/auth'
        ),
        supertokens_config=SupertokensConfig(
            connection_uri='https://auth--supertokensjubla--yfqk8y7vjnjc.code.run/',
            api_key=os.getenv('SUPERTOKENS_API_KEY')
        ),
        framework='fastapi',
        recipe_list=[
            session.init(),
            emailpassword.init()
        ],
        mode='asgi'
    )
