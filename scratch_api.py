import requests
import config

headers = {
    "Authorization": f"Bot {config.TOKEN}"
}
url = "https://discord.com/api/v10/applications/@me"
r = requests.get(url, headers=headers)
app_id = r.json()["id"]

url_cmds = f"https://discord.com/api/v10/applications/{app_id}/commands"
r_cmds = requests.get(url_cmds, headers=headers)
cmds = r_cmds.json()
print([c["name"] for c in cmds])
