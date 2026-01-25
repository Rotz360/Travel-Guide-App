# Travel Guide App

An AI-powered travel guide generator that creates personalized itineraries with route optimization, beautiful images, and local recommendations.

## Features

- 🗺️ **Smart Route Optimization**: Automatically calculates the best route for multiple destinations
- 🤖 **AI-Powered Content**: Generates detailed location descriptions and itineraries using Google Gemini
- 📍 **Real Google Maps Data**: Fetches actual attractions, restaurants, and hotels via Apify scraper (optional)
- 📸 **Beautiful Images**: Fetches stunning photos from Unsplash or Google Maps
- 🏨 **Complete Recommendations**: Real ratings, reviews, and pricing from Google Maps
- ⭐ **Quality Filtering**: Only shows highly-rated places (4+ stars)
- ✨ **Modern UI**: Beautiful, responsive interface with smooth animations

## Architecture

This application follows a 3-tier architecture:

### Backend (FastAPI)
- **Services**: AI content generation, real Google Maps data (Apify), image retrieval, route optimization
- **API**: RESTful endpoints for generating travel guides
- **Technologies**: Python, FastAPI, Google Gemini API, Apify, Unsplash API

### Frontend (Next.js)
- **Components**: Reusable React components with TypeScript
- **Styling**: Tailwind CSS with custom gradients and animations
- **Technologies**: Next.js 14, React, TypeScript

## Setup Instructions

### Prerequisites
- Python 3.8+ (for backend)
- Node.js 18+ (for frontend)
- OpenRouter API key (recommended) OR Google Gemini API key
- Apify API token (optional but recommended for real data)
- Unsplash API key (optional, falls back to placeholders)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file from the example:
```bash
copy .env.example .env
```

5. Edit `.env` and add your API keys:
   - `OPENROUTER_API_KEY`: Your OpenRouter API key
   - `APIFY_API_TOKEN`: Your Apify API token (optional but recommended)
   - `GOOGLE_API_KEY`: Your Google Gemini API key (fallback)
   - `UNSPLASH_ACCESS_KEY`: Your Unsplash API key (optional)

6. Run the backend server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## Usage

1. Open `http://localhost:3000` in your browser
2. Enter one or more destinations (e.g., "Paris, France", "Amsterdam, Netherlands")
3. Optionally specify trip duration and preferences
4. Click "Generate Travel Guide"
5. Explore your personalized itinerary with images and recommendations!

## Project Structure

```
Travel Guide App/
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── routes/              # API routes
│   ├── services/            # Business logic (AI, images, itinerary)
│   ├── models/              # Pydantic schemas
│   └── requirements.txt
├── frontend/
│   ├── app/                 # Next.js app directory
│   ├── components/          # React components
│   ├── lib/                 # API client
│   └── package.json
├── directives/              # SOPs for the system
└── .tmp/                    # Temporary files
```

## API Endpoints

- `POST /api/generate-guide`: Generate a complete travel guide
- `GET /api/health`: Health check endpoint
- `GET /`: API information

## Technologies Used

- **Backend**: FastAPI, Google Gemini AI, Apify (Google Maps Scraper), Unsplash API, geopy
- **Frontend**: Next.js 14, React, TypeScript, Tailwind CSS
- **UI Icons**: Lucide React

## Notes

- **Real Data**: When Apify is configured, the app fetches real places from Google Maps with actual ratings and reviews
- **Fallback**: Without Apify, the app uses AI-generated recommendations (still useful but not verified)
- The route optimization uses a nearest-neighbor algorithm for simplicity
- Geocoding relies on OpenStreetMap (may not find very specific locations)
- **Free Tier**: Apify offers $5/month free credit (~400 results, enough for testing)
- Images are fetched from Unsplash API (free tier has rate limits)
- AI content generation may take 10-30 seconds depending on the number of destinations
- All temporary files are stored in `.tmp/` and can be safely deleted

## Future Enhancements

- User accounts and saved itineraries
- Export to PDF functionality
- Integration with booking platforms
- Interactive maps
- Multi-language support
