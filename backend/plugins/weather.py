"""Weather plugin - Get current weather"""

import logging
import requests
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class WeatherPlugin:
    """Get weather information"""
    
    NAME = "weather"
    DESCRIPTION = "Get current weather information"
    TRIGGERS = ["weather", "forecast", "temperature", "what's the weather"]
    
    @staticmethod
    async def execute(command: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute weather command"""
        try:
            city = args.get("city", "auto")  # Use IP-based location by default
            
            # Using open-meteo API (free, no key required)
            # For IP-based location
            if city.lower() == "auto":
                # Get location from IP
                try:
                    location_response = requests.get("https://ipapi.co/json/", timeout=5)
                    if location_response.status_code == 200:
                        location_data = location_response.json()
                        latitude = location_data.get("latitude")
                        longitude = location_data.get("longitude")
                        city_name = location_data.get("city", "Unknown")
                    else:
                        return {
                            "status": "error",
                            "message": "Could not determine location"
                        }
                except Exception as e:
                    logger.error(f"Location lookup error: {e}")
                    return {
                        "status": "error",
                        "message": "Could not determine location"
                    }
            else:
                # Geocode city name
                try:
                    geo_response = requests.get(
                        "https://geocoding-api.open-meteo.com/v1/search",
                        params={"name": city, "count": 1, "language": "en", "format": "json"},
                        timeout=5
                    )
                    if geo_response.status_code == 200:
                        geo_data = geo_response.json()
                        if geo_data["results"]:
                            latitude = geo_data["results"][0]["latitude"]
                            longitude = geo_data["results"][0]["longitude"]
                            city_name = geo_data["results"][0]["name"]
                        else:
                            return {
                                "status": "error",
                                "message": f"City '{city}' not found"
                            }
                    else:
                        return {
                            "status": "error",
                            "message": "Could not geocode city"
                        }
                except Exception as e:
                    logger.error(f"Geocoding error: {e}")
                    return {
                        "status": "error",
                        "message": "Could not geocode city"
                    }
            
            # Get weather data
            try:
                weather_response = requests.get(
                    "https://api.open-meteo.com/v1/forecast",
                    params={
                        "latitude": latitude,
                        "longitude": longitude,
                        "current": "temperature_2m,weather_code,wind_speed_10m,humidity",
                        "temperature_unit": "celsius"
                    },
                    timeout=5
                )
                
                if weather_response.status_code == 200:
                    weather_data = weather_response.json()["current"]
                    
                    return {
                        "status": "success",
                        "city": city_name,
                        "temperature": weather_data["temperature_2m"],
                        "humidity": weather_data["humidity"],
                        "wind_speed": weather_data["wind_speed_10m"],
                        "condition": WeatherPlugin._get_weather_description(weather_data["weather_code"]),
                        "message": f"Current weather in {city_name}: {weather_data['temperature_2m']}°C, {WeatherPlugin._get_weather_description(weather_data['weather_code'])}"
                    }
                else:
                    return {
                        "status": "error",
                        "message": "Could not fetch weather data"
                    }
            except Exception as e:
                logger.error(f"Weather fetch error: {e}")
                return {
                    "status": "error",
                    "message": str(e)
                }
        
        except Exception as e:
            logger.error(f"Weather command error: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    @staticmethod
    def _get_weather_description(code: int) -> str:
        """Get weather description from WMO code"""
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Foggy",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with hail",
            99: "Thunderstorm with hail"
        }
        return weather_codes.get(code, "Unknown")
