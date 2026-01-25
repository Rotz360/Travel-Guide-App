'use client';

import { useState } from 'react';
import { Plane, Navigation, ArrowDown } from 'lucide-react';
import DestinationInput from '@/components/DestinationInput';
import LocationCard from '@/components/LocationCard';
import ItineraryDisplay from '@/components/ItineraryDisplay';
import RecommendationSection from '@/components/RecommendationSection';
import { generateTravelGuide, TravelGuide } from '@/lib/api';

export default function Home() {
    const [guide, setGuide] = useState<TravelGuide | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleGenerate = async (destinations: string[], days?: number, preferences?: string) => {
        setIsLoading(true);
        setError(null);
        setGuide(null);

        try {
            const result = await generateTravelGuide({
                destinations,
                days,
                preferences,
            });
            setGuide(result);

            // Scroll to results after a brief delay
            setTimeout(() => {
                document.getElementById('results')?.scrollIntoView({ behavior: 'smooth' });
            }, 300);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to generate travel guide');
            console.error('Error generating guide:', err);
        } finally {
            setIsLoading(false);
        }
    };

    const handleNewSearch = () => {
        setGuide(null);
        setError(null);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    return (
        <main className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50">
            {/* Hero Section */}
            <div className="relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-r from-purple-600/10 to-pink-600/10" />

                <div className="relative container mx-auto px-4 py-16 md:py-24">
                    <div className="text-center mb-12">
                        <div className="flex justify-center mb-6">
                            <div className="p-6 bg-white rounded-3xl shadow-2xl">
                                <Plane className="w-16 h-16 text-purple-600" />
                            </div>
                        </div>
                        <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-purple-600 via-pink-600 to-purple-600 bg-clip-text text-transparent">
                            AI Travel Guide Generator
                        </h1>
                        <p className="text-xl md:text-2xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
                            Create personalized travel itineraries with AI-powered recommendations,
                            stunning images, and optimized routes
                        </p>
                    </div>

                    {/* Input Section */}
                    <DestinationInput onGenerate={handleGenerate} isLoading={isLoading} />

                    {/* Scroll Indicator */}
                    {!guide && !isLoading && (
                        <div className="text-center mt-12 animate-bounce">
                            <ArrowDown className="w-8 h-8 mx-auto text-purple-400" />
                        </div>
                    )}
                </div>
            </div>

            {/* Error Message */}
            {error && (
                <div className="container mx-auto px-4 py-8">
                    <div className="bg-red-50 border-2 border-red-200 rounded-2xl p-6 text-center">
                        <p className="text-red-700 text-lg font-medium">
                            ⚠️ {error}
                        </p>
                        <button
                            onClick={handleNewSearch}
                            className="mt-4 px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
                        >
                            Try Again
                        </button>
                    </div>
                </div>
            )}

            {/* Results Section */}
            {guide && (
                <div id="results" className="container mx-auto px-4 py-16 space-y-16">
                    {/* Route Info */}
                    {guide.route_info && guide.route_info.segments.length > 0 && (
                        <div className="bg-white rounded-3xl shadow-xl p-8 md:p-12">
                            <div className="flex items-center gap-3 mb-6">
                                <Navigation className="w-8 h-8 text-purple-600" />
                                <h2 className="text-3xl font-bold text-gray-800">Your Route</h2>
                            </div>

                            <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-2xl p-6 mb-6">
                                <p className="text-lg font-semibold text-gray-700">
                                    <span className="text-purple-600">Total Distance:</span>{' '}
                                    {guide.route_info.total_distance_km} km
                                </p>
                                <p className="text-gray-600 mt-2">
                                    Traveling across {guide.destinations.length} destination{guide.destinations.length > 1 ? 's' : ''} over {guide.total_days} day{guide.total_days > 1 ? 's' : ''}
                                </p>
                            </div>

                            <div className="space-y-4">
                                {guide.route_info.segments.map((segment, index) => (
                                    <div key={index} className="flex items-center gap-4 bg-gray-50 rounded-xl p-4">
                                        <span className="flex-shrink-0 bg-purple-600 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold">
                                            {index + 1}
                                        </span>
                                        <div className="flex-1">
                                            <p className="font-semibold text-gray-800">
                                                {segment.from} → {segment.to}
                                            </p>
                                            <p className="text-sm text-gray-600">
                                                {segment.distance_km} km • ~{segment.estimated_hours} hours
                                            </p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Destinations */}
                    <div className="space-y-8">
                        <h2 className="text-4xl font-bold text-center bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                            Your Destinations
                        </h2>
                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                            {guide.destinations.map((location, index) => (
                                <LocationCard key={index} location={location} />
                            ))}
                        </div>
                    </div>

                    {/* Itinerary */}
                    {guide.itinerary.length > 0 && (
                        <ItineraryDisplay itinerary={guide.itinerary} />
                    )}

                    {/* Recommendations */}
                    <RecommendationSection recommendations={guide.recommendations} />

                    {/* New Search Button */}
                    <div className="text-center pt-8">
                        <button
                            onClick={handleNewSearch}
                            className="px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-bold text-lg rounded-xl shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200"
                        >
                            ✨ Plan Another Trip
                        </button>
                    </div>
                </div>
            )}

            {/* Footer */}
            <footer className="text-center py-12 text-gray-600">
                <p className="text-sm">
                    Powered by AI • Made with ❤️ for travelers
                </p>
            </footer>
        </main>
    );
}
