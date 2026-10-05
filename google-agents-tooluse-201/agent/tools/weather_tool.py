"""Retourne une meteo simulee pour un agent Gemini."""

def get_weather(city: str) -> dict:
    return {"city": city, "summary": "sunny"}
