from fastapi import APIRouter, Request

from utils import get_guild, checkPermissions, getChannels

from sql.crud import get_welcome, upsert_welcome_message, update_welcome_message


router = APIRouter(prefix="/guilds", tags=["guilds"])


@router.get("/{guild}")
async def getGuild(guild: int):
    data = get_guild(guild)

    if data is None: return 'null'

    return {
        "id": data['id'],
        "name": data['name'],
        "icon": data['icon'],
        "enabledFeatures": ['welcome-message']
    }

@router.get('/{guild}/channels')
async def getChannel(guild: int):
    data = getChannels(guild)

    if data is None: return 'null'

    return data

@router.get('/{guild}/features/welcome-message')
async def getFeature(request: Request, guild: int):
    data = get_welcome(guild)
    if data is None:
        return 'null'
    return {
        "message": data.message,
        "channel": str(data.channel)
    }

@router.post('/{guild}/features/welcome-message')
async def enableFeature(request: Request, guild: int):
    if checkPermissions(request.session, guild):
        upsert_welcome_message(guild_id=guild)
    return 'Success'

@router.patch('/{guild}/features/welcome-message')
async def updateFeature(request: Request, guild: int):
    r_data = await request.json()
    if checkPermissions(request.session, guild):
        data = update_welcome_message(guild_id=guild, message=r_data['message'], channel=r_data['channel'])
        return data
