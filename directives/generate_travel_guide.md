# Directive: Generate Travel Guide

## Objective
Generate a comprehensive AI-powered travel guide for one or multiple destinations, including route optimization, detailed itineraries, images, and local recommendations.

## Inputs
- **Destinations** (required): Array of destination names (e.g., ["Paris, France", "Amsterdam, Netherlands"])
- **Days** (optional): Total trip duration in days. If not provided, defaults to 3 days per destination
- **Preferences** (optional): User preferences like "budget travel", "luxury", "adventure", etc.

## Tools & Scripts
- **AI Service** (`backend/services/ai_service.py`): Google Gemini API for content generation
- **Image Service** (`backend/services/image_service.py`): Unsplash API for location images
- **Itinerary Service** (`backend/services/itinerary_service.py`): Route optimization and distance calculations
- **Recommendations Service** (`backend/services/recommendations_service.py`): Orchestrates AI and image services

## Process Flow

### 1. Route Optimization (if multiple destinations)
- Uses nearest-neighbor algorithm to minimize travel distance
- Geocodes destinations using Nominatim (OpenStreetMap)
- Calculates distances between locations using geodesic measurements
- Returns optimized order of destinations

### 2. Location Details Generation
For each destination:
- Query Google Gemini for:
  - Compelling description (2-3 sentences)
  - 5 must-see highlights
  - Best time to visit
  - Local insider tip
- Fetch 4 high-quality images from Unsplash
- Geocode to get coordinates (lat/lng)

### 3. Itinerary Creation
- Distribute total days across destinations
- Generate day-by-day activities using AI:
  - Morning, afternoon, and evening activities
  - Activity descriptions
  - Estimated duration for each activity
  - Specific locations within each destination

### 4. Recommendations Generation
For each destination, generate 5 recommendations in each category:
- **Sleep**: Hotels, hostels, unique stays with price levels
- **Eat**: Restaurants, cafes, food experiences
- **Curiosities**: Hidden gems, local attractions, unique experiences

Each recommendation includes:
- Name and description
- Why it's recommended
- Price level ($, $$, $$$)
- Relevant image

### 5. Route Information
Calculate and return:
- Total distance in kilometers
- Segment-by-segment breakdown (from → to, distance, estimated travel time)
- Travel time estimates (assumes 60 km/h average speed)

## Output Format
Returns a `TravelGuide` object with:
```json
{
  "destinations": [{LocationDetail}],
  "itinerary": [{DayItinerary}],
  "recommendations": {
    "sleep": [{Recommendation}],
    "eat": [{Recommendation}],
    "curiosities": [{Recommendation}]
  },
  "route_info": {
    "total_distance_km": number,
    "segments": [{from, to, distance_km, estimated_hours}]
  },
  "total_days": number
}
```

## Edge Cases & Error Handling

### Geocoding Failures
- If a location cannot be geocoded, route optimization continues without that location
- Coordinates field will be `null` for that destination

### API Rate Limits
- **Unsplash**: Free tier allows 50 requests/hour
  - Fallback to `source.unsplash.com` placeholder images if rate limited
- **Google Gemini**: Has generous free tier
  - If API fails, return graceful fallback content

### Invalid JSON from AI
- AI responses should be valid JSON
- If parsing fails, use fallback content (predefined templates)
- Log errors for debugging

### Network Timeouts
- Image fetching has 10-second timeout
- If timeout occurs, use placeholder image

### Empty Destinations
- Validate that at least one destination is provided
- Return 400 error if no valid destinations

## Timing Expectations
- Single destination: 15-25 seconds
- Multiple destinations (3): 30-45 seconds
- Most time spent on:
  - AI content generation (parallel requests help)
  - Image fetching from Unsplash
  - Geocoding locations

## Best Practices
1. **Parallel Processing**: Where possible, make API calls concurrently
2. **Caching**: Consider caching location details and images for popular destinations
3. **Error Recovery**: Always provide fallback content rather than failing completely
4. **User Feedback**: Frontend shows loading state during generation
5. **Rate Limiting**: Implement exponential backoff for API retries

## Configuration
Environment variables (in `.env`):
- `GOOGLE_API_KEY`: Google Gemini API key (required)
- `UNSPLASH_ACCESS_KEY`: Unsplash API key (optional, uses placeholders if missing)
- `FRONTEND_URL`: Frontend URL for CORS (default: http://localhost:3000)

## Testing Commands
```bash
# Start backend
cd backend
python main.py

# Start frontend
cd frontend
npm run dev

# Health check
curl http://localhost:8000/api/health

# Test guide generation
curl -X POST http://localhost:8000/api/generate-guide \
  -H "Content-Type: application/json" \
  -d '{"destinations": ["Rome, Italy"], "days": 3}'
```

## Known Limitations
- Route optimization uses simple nearest-neighbor (not TSP solver)
- Geocoding relies on OpenStreetMap (may not find very specific locations)
- AI-generated content quality depends on Gemini's knowledge
- Images are generic location photos, not specific to recommendations
- No real-time pricing or availability data

## Future Improvements
- Implement proper TSP solver for better route optimization
- Add caching layer (Redis) for popular destinations
- Integrate Google Places API for more accurate location data
- Add user accounts to save generated guides
- Support for date-specific recommendations (events, weather)
- Multi-language support for international travelers
