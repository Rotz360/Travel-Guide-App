"""
AI service using OpenRouter or Google Gemini for content generation
"""
import os
import json
from typing import List, Dict, Any
from dotenv import load_dotenv
import google.generativeai as genai
from openai import OpenAI

load_dotenv()

# Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet")

# Initialize Clients
openai_client = None
if OPENROUTER_API_KEY:
    openai_client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-pro')


def _clean_json_response(text: str) -> str:
    """Clean markdown code blocks from JSON response"""
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()


async def generate_content(prompt: str) -> str:
    """
    Generate content using available AI provider (OpenRouter preferred)
    """
    if openai_client:
        try:
            response = openai_client.chat.completions.create(
                model=OPENROUTER_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful travel assistant that outputs valid JSON only."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenRouter Error: {e}")
            # Fallback to Gemini if available
            if not GOOGLE_API_KEY:
                raise e
    
    if GOOGLE_API_KEY:
        try:
            response = gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Gemini Error: {e}")
            raise e
            
    return "{}" # No provider available


async def generate_location_details(destination: str) -> Dict[str, Any]:
    """
    Generate detailed information about a destination
    """
    prompt = f"""Generate detailed travel information about {destination} in JSON format.

Include:
- name: The destination name
- description: A compelling 2-3 sentence description
- highlights: Array of 5 must-see attractions or experiences
- best_time_to_visit: Brief note on best season
- local_tip: One insider tip for visitors

Format as valid JSON only, no additional text."""

    response_text = await generate_content(prompt)
    
    try:
        # Parse the JSON response
        result = json.loads(_clean_json_response(response_text))
        return result
    except Exception:
        # Fallback
        return {
            "name": destination,
            "description": f"A beautiful destination: {destination}",
            "highlights": ["Explore the local culture", "Visit historic sites", "Enjoy local cuisine"],
            "best_time_to_visit": "Spring and Fall",
            "local_tip": "Learn a few phrases in the local language"
        }


async def generate_itinerary(
    destinations: List[str], 
    days: int,
    preferences: str = ""
) -> List[Dict[str, Any]]:
    """
    Generate day-by-day itinerary for the trip
    """
    destinations_str = ", ".join(destinations)
    pref_str = f" with preferences: {preferences}" if preferences else ""
    
    prompt = f"""Create a {days}-day travel itinerary for {destinations_str}{pref_str}.

For each day, provide:
- day_number: Integer (1 to {days})
- title: Brief title for the day
- location: Main location for that day
- activities: Array of 3-4 activities with:
  - time: "Morning", "Afternoon", or "Evening"
  - activity: Name of the activity
  - description: Brief description (1 sentence)
  - duration: Approximate time needed (e.g., "2 hours")

Optimize the route to minimize travel time. Return as a JSON array of days, no additional text."""

    response_text = await generate_content(prompt)
    
    try:
        result = json.loads(_clean_json_response(response_text))
        return result if isinstance(result, list) else []
    except Exception:
        # Fallback itinerary
        return [{
            "day_number": i + 1,
            "title": f"Exploring {destinations[min(i, len(destinations)-1)]}",
            "location": destinations[min(i, len(destinations)-1)],
            "activities": [
                {
                    "time": "Morning",
                    "activity": "City exploration",
                    "description": "Discover the main attractions",
                    "duration": "3 hours"
                }
            ]
        } for i in range(days)]


async def generate_recommendations(
    destination: str,
    category: str
) -> List[Dict[str, Any]]:
    """
    Generate recommendations for sleep, eat, or curiosities
    """
    category_prompts = {
        "sleep": "accommodations (hotels, hostels, unique stays)",
        "eat": "restaurants, cafes, and food experiences",
        "curiosity": "hidden gems, local curiosities, and unique attractions"
    }
    
    category_text = category_prompts.get(category, "places of interest")
    
    prompt = f"""Recommend 5 great {category_text} in {destination}.

For each recommendation, provide:
- name: Name of the place
- description: 1-2 sentence description
- category: "{category}"
- price_level: "$" (budget), "$$" (mid-range), or "$$$" (luxury)
- why_recommended: One sentence explaining why it's recommended

Return as a JSON array, no additional text."""

    response_text = await generate_content(prompt)
    
    try:
        result = json.loads(_clean_json_response(response_text))
        return result if isinstance(result, list) else []
    except Exception:
        # Fallback recommendations
        return [{
            "name": f"Great {category} option in {destination}",
            "description": "A wonderful choice for travelers",
            "category": category,
            "price_level": "$$",
            "why_recommended": "Highly rated by locals and tourists alike"
        }]


async def generate_curiosities(destination: str) -> List[str]:
    """
    Generate interesting facts and curiosities about a destination
    """
    prompt = f"""List 5 interesting facts or curiosities about {destination}.

Return as a JSON array of strings, each being a complete sentence. No additional text."""

    response_text = await generate_content(prompt)
    
    try:
        result = json.loads(_clean_json_response(response_text))
        return result if isinstance(result, list) else []
    except Exception:
        return [
            f"{destination} has a rich cultural heritage.",
            "The local cuisine is renowned worldwide.",
            "There are many historic landmarks to explore."
        ]
