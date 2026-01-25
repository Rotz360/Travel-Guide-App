# Directive: Apify Google Maps Integration

## Objective
Fetch real places data from Google Maps using Apify's `compass/crawler-google-places` scraper to provide accurate, verified recommendations.

## When to Use
- User has `APIFY_API_TOKEN` configured in `.env`
- Fetching recommendations for attractions, restaurants, or accommodations
- Prioritize quality over generated content

## Inputs
- **Destination**: City or location name (e.g., "Paris, France")
- **Category**: "attractions", "restaurants", or "hotels"
- **Max Results**: Number of results to fetch (default: 5)
- **Min Rating**: Minimum rating filter (default: 4.0)

## Apify Actor Details

**Actor ID**: `compass/crawler-google-places`

### Input Parameters
```json
{
  "searchStringsArray": ["restaurants in Paris"],
  "maxCrawledPlacesPerSearch": 10,
  "language": "en",
  "skipClosedPlaces": true,
  "reviews": false,
  "images": true,
  "additionalInfo": false
}
```

### Output Fields Used
- `title`: Place name
- `description`: Place description
- `totalScore`: Rating (0-5)
- `reviewsCount`: Number of reviews
- `address`: Full address
- `website`: Website URL
- `phone`: Phone number
- `imageUrl` or `images`: Photos
- `location`: {lat, lng} coordinates
- `priceLevel`: Price indicator
- `categoryName`: Type/category

## Implementation

### Service Location
`backend/services/apify_service.py`

### Functions

#### `search_google_places(query, max_results, min_rating)`
Generic search function that:
1. Runs the Apify actor with search query
2. Waits for completion
3. Fetches results from dataset
4. Filters by minimum rating
5. Returns list of places

#### `get_attractions(destination, max_results)`
Searches for "tourist attractions in {destination}"

#### `get_restaurants(destination, max_results)`
Searches for "best restaurants in {destination}"

#### `get_accommodations(destination, max_results)`
Searches for "hotels in {destination}"

## Integration Points

### Recommendations Service
`backend/services/recommendations_service.py`

**Logic**:
```python
if APIFY_ENABLED:
    # Use real Google Maps data
    places = await get_restaurants(destination)
else:
    # Fallback to AI-generated
    places = await ai_generate_recommendations(destination, "eat")
```

### Data Transformation
Convert Apify response to our `Recommendation` schema:
- Map `title` → `name`
- Map `totalScore` → include in `description` and `why_recommended`
- Map `reviewsCount` → include in `why_recommended`
- Map `imageUrl` → `ImageInfo` object
- Map `priceLevel` → `price_level` ($, $$, $$$)

## Rate Limiting & Costs

### Apify Pricing
- **Free Tier**: $5/month credit
- **Cost**: ~$0.25 per 1000 results
- **Our Usage**: ~6 queries per guide (2 destinations × 3 categories)
- **Results per query**: ~5 places
- **Total per guide**: ~30 results = ~$0.0075 per guide

### Free Tier Capacity
- $5 credit = ~20,000 results
- At 30 results/guide = ~660 guides per month
- More than sufficient for development and moderate use

## Error Handling

### No API Token
```python
if not APIFY_ENABLED:
    print("Apify not enabled - falling back to AI")
    return []
```

### API Errors
```python
try:
    run = client.actor("compass/crawler-google-places").call(...)
except Exception as e:
    print(f"Error fetching from Apify: {e}")
    return []
```

### Empty Results
- If no places meet rating filter, return empty list
- Recommendations service falls back to AI

## Quality Filters

### Minimum Rating
- Attractions: 4.2+ stars
- Restaurants: 4.0+ stars
- Accommodations: 4.0+ stars

### Skip Closed Places
- `skipClosedPlaces: true` in actor input
- Ensures only active businesses

## Performance Optimization

### What We DON'T Fetch
- **Reviews content**: Too expensive, not needed
- **Additional info**: Reduces API time
- **Popular times**: Not essential

### What We DO Fetch
- **Images**: Essential for UI
- **Basic details**: Name, rating, address, etc.
- **Coordinates**: For mapping

### Parallel Execution
The service runs asynchronously, allowing multiple Apify calls in parallel for different destinations.

## Testing

### Manual Test
```bash
# Set APIFY_API_TOKEN in .env
cd backend
python -c "
from services.apify_service import get_restaurants
import asyncio
results = asyncio.run(get_restaurants('Paris, France', 5))
print(results)
"
```

### Via API
```bash
curl -X POST http://localhost:8000/api/generate-guide \
  -H "Content-Type: application/json" \
  -d '{"destinations": ["Paris"], "days": 3}'
```

Check backend logs for "Fetching real data from Google Maps"

## Monitoring

### Success Indicators
- Log message: "Fetching real data from Google Maps for {destination}"
- Log message: "Found X places with rating >= Y"
- Frontend shows real ratings (e.g., "4.5/5 from 1,234 reviews")

### Failure Indicators
- Log message: "Apify not enabled - falling back to AI"
- Log message: "Error fetching from Apify: {error}"
- Generic descriptions without specific ratings

## Future Improvements

1. **Caching**: Cache popular destinations to save API credits
2. **Custom Queries**: Let users specify cuisine type, price range, etc.
3. **Booking Integration**: Link to reservation systems
4. **User Reviews**: Show recent reviews from Google Maps
5. **Real-time Availability**: Check if places are currently open

## References

- Apify Google Places Scraper: https://apify.com/compass/crawler-google-places
- Apify Python Client: https://docs.apify.com/api/client/python
- Actor Documentation: https://apify.com/compass/crawler-google-places/api
