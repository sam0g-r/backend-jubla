from supertokens_python import init, InputAppInfo, SupertokensConfig
from supertokens_python.recipe import session, emailpassword
from app.shared.config.settings import settings


def init_supertokens():
    init(
        app_info=InputAppInfo(
            app_name=settings.PROJECT_NAME,
            api_domain='http://localhost:8000',
            website_domain='http://localhost:3000',
            api_base_path='/api/v1/auth',
            website_base_path='/auth'
        ),
        supertokens_config=SupertokensConfig(
            connection_uri='https://try.supertokens.com/'
        ),
        framework='fastapi',
        recipe_list=[
            session.init(),
            emailpassword.init()
        ],
        mode='asgi'
    )
