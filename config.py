from pyrogram import Client
from asBASE import asJSON

db = asJSON("as.json")
###


SUDORS = [916165019] # ايديات المطورين
API_ID = 14911221
API_HASH = "a5e14021456afd496e7377331e2e5bcf"
TOKEN = "5559264795:AAExX1y71oNAqgqYsiF0bRg5k9TX6b_CoCc" # التوكن
bot = Client("control",API_ID,API_HASH,bot_token=TOKEN,in_memory=True)
bot_id = TOKEN.split(":")[0]