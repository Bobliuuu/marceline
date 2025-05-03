import requests

def get_valorant_rank(riot_id, riot_tag):
    # URL-encode the Riot ID and tag
    riot_id_encoded = riot_id.replace(" ", "%20")
    riot_tag_encoded = riot_tag
    profile_url = f"https://api.tracker.gg/api/v2/valorant/standard/profile/riot/{riot_id_encoded}%23{riot_tag_encoded}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(profile_url, headers=headers)
    if response.status_code != 200:
        print(f"Error: {response.status_code} — could not fetch profile.")
        return None

    data = response.json()

    try:
        segments = data["data"]["segments"]
        for seg in segments:
            if seg["type"] == "competitive":
                stats = seg["stats"]
                tier = stats["tier"]["metadata"]["tierName"]
                elo = stats.get("ranking_in_tier", {}).get("value", None)
                return f"{tier} ({elo} RR)" if elo is not None else tier
        print("Competitive stats not found.")
        return None
    except KeyError:
        print("Unexpected API format.")
        return None

riot_user = "Elizaboo#0000"
riot_id = riot_user.split("#")[0]
riot_tag = riot_user.split("#")[1]
rank = get_valorant_rank(riot_id, riot_tag)
print(f"Your rank: {rank}")
