/**
 * TypeScript types for the Travel Guide API
 */

export interface ImageInfo {
    url: string;
    alt_text: string;
    photographer?: string;
}

export interface LocationDetail {
    name: string;
    description: string;
    highlights: string[];
    main_image?: ImageInfo;
    additional_images: ImageInfo[];
    coordinates?: {
        lat: number;
        lng: number;
    };
}

export interface DayActivity {
    time: string;
    activity: string;
    description: string;
    location: string;
    duration?: string;
}

export interface DayItinerary {
    day_number: number;
    date?: string;
    title: string;
    activities: DayActivity[];
    location: string;
}

export interface Recommendation {
    name: string;
    description: string;
    category: string;
    price_level?: string;
    why_recommended: string;
    image?: ImageInfo;
}

export interface TravelGuide {
    destinations: LocationDetail[];
    itinerary: DayItinerary[];
    recommendations: {
        sleep: Recommendation[];
        eat: Recommendation[];
        curiosities: Recommendation[];
    };
    route_info?: {
        total_distance_km: number;
        segments: Array<{
            from: string;
            to: string;
            distance_km: number;
            estimated_hours: number;
        }>;
    };
    total_days: number;
}

export interface GuideRequest {
    destinations: string[];
    days?: number;
    preferences?: string;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Generate a travel guide
 */
export async function generateTravelGuide(
    request: GuideRequest
): Promise<TravelGuide> {
    const response = await fetch(`${API_BASE_URL}/api/generate-guide`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to generate travel guide');
    }

    return response.json();
}

/**
 * Health check
 */
export async function checkHealth(): Promise<{ status: string }> {
    const response = await fetch(`${API_BASE_URL}/api/health`);
    return response.json();
}
