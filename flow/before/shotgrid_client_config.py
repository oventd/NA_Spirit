from shotgun_api3 import Shotgun

SERVER_PATH = 'https://hi.shotgrid.autodesk.com'
SCRIPT_NAME = 'nayeon_key'
API_KEY = 'syeswcrleslhjbh4bd!poRvde'

def get_shotgrid_client():
    return Shotgun(SERVER_PATH, SCRIPT_NAME, API_KEY)

