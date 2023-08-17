import os


class Config(object):
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "5559264795:AAExX1y71oNAqgqYsiF0bRg5k9TX6b_CoCc")

    APP_ID = int(os.environ.get("APP_ID", 10878311))

    API_HASH = os.environ.get("API_HASH", "151b5b67acb5676b267c610dfca246ba")
