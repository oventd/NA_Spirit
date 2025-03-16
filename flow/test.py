from shotgun_api3 import Shotgun

SERVER_PATH = 'https://5thacademy.shotgrid.autodesk.com'
SCRIPT_NAME = 'nayeon_key'
API_KEY = 'h0mvmfnhuochunhzpgR~zlpur'

sg = Shotgun(SERVER_PATH, SCRIPT_NAME, API_KEY)

result = sg.find(
    "Task",
    [["id", "is", 6183]], 
    ["id", "content","upstream_tasks"]
)

print("DEBUG: ShotGrid Response >>>", result)