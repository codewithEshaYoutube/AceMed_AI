import requests
api_key = "0axiXOqt.mVdfIOlB26Lp2PzAa5xo1s6Xwh6jXvdJ"
channel_token = "codewitheshayoutube"
prompt = "What is support and movement in biology?"

def query_llm(prompt, api_key, channel_token):
    url = f"https://payload.vextapp.com/hook/ICYAJ67MIS/catch/{channel_token}"
    headers = {
        "Content-Type": "application/json",
        "Apikey": f"Api-Key {api_key}"
    }
    payload = {
        "payload": prompt,
        "env": "dev"
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.text.strip()
        else:
            return f"❌ Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"⚠️ Exception occurred: {str(e)}"
