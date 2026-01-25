'use client';

import { useState } from 'react';
import { Plus, X, MapPin } from 'lucide-react';

interface DestinationInputProps {
    onGenerate: (destinations: string[], days?: number, preferences?: string) => void;
    isLoading: boolean;
}

export default function DestinationInput({ onGenerate, isLoading }: DestinationInputProps) {
    const [destinations, setDestinations] = useState<string[]>(['']);
    const [days, setDays] = useState<string>('');
    const [preferences, setPreferences] = useState<string>('');

    const addDestination = () => {
        setDestinations([...destinations, '']);
    };

    const removeDestination = (index: number) => {
        if (destinations.length > 1) {
            setDestinations(destinations.filter((_, i) => i !== index));
        }
    };

    const updateDestination = (index: number, value: string) => {
        const updated = [...destinations];
        updated[index] = value;
        setDestinations(updated);
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        const validDestinations = destinations.filter(d => d.trim() !== '');

        if (validDestinations.length === 0) {
            alert('Please enter at least one destination');
            return;
        }

        onGenerate(
            validDestinations,
            days ? parseInt(days) : undefined,
            preferences || undefined
        );
    };

    return (
        <div className="w-full max-w-4xl mx-auto">
            <div className="bg-white rounded-3xl shadow-2xl p-8 md:p-12 border border-gray-100">
                <div className="text-center mb-8">
                    <h2 className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-3">
                        Plan Your Journey
                    </h2>
                    <p className="text-gray-600 text-lg">
                        Enter your dream destinations and let AI create your perfect itinerary
                    </p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-6">
                    {/* Destinations */}
                    <div className="space-y-4">
                        <label className="block text-sm font-semibold text-gray-700 mb-3">
                            <MapPin className="inline w-5 h-5 mr-2 text-purple-600" />
                            Destinations
                        </label>

                        {destinations.map((dest, index) => (
                            <div key={index} className="flex gap-3 animate-fade-in">
                                <input
                                    type="text"
                                    value={dest}
                                    onChange={(e) => updateDestination(index, e.target.value)}
                                    placeholder={`Destination ${index + 1} (e.g., Paris, France)`}
                                    className="flex-1 px-5 py-4 rounded-xl border-2 border-gray-200 focus:border-purple-500 focus:outline-none transition-all duration-200 text-lg text-gray-900"
                                    disabled={isLoading}
                                />
                                {destinations.length > 1 && (
                                    <button
                                        type="button"
                                        onClick={() => removeDestination(index)}
                                        className="p-4 rounded-xl bg-red-50 text-red-600 hover:bg-red-100 transition-colors duration-200"
                                        disabled={isLoading}
                                    >
                                        <X className="w-5 h-5" />
                                    </button>
                                )}
                            </div>
                        ))}

                        <button
                            type="button"
                            onClick={addDestination}
                            className="w-full py-3 px-5 rounded-xl border-2 border-dashed border-purple-300 text-purple-600 hover:bg-purple-50 transition-all duration-200 flex items-center justify-center gap-2 font-medium"
                            disabled={isLoading}
                        >
                            <Plus className="w-5 h-5" />
                            Add Another Destination
                        </button>
                    </div>

                    {/* Days */}
                    <div>
                        <label className="block text-sm font-semibold text-gray-700 mb-3">
                            Trip Duration (optional)
                        </label>
                        <input
                            type="number"
                            value={days}
                            onChange={(e) => setDays(e.target.value)}
                            placeholder="Number of days"
                            min="1"
                            max="30"
                            className="w-full px-5 py-4 rounded-xl border-2 border-gray-200 focus:border-purple-500 focus:outline-none transition-all duration-200 text-lg text-gray-900"
                            disabled={isLoading}
                        />
                    </div>

                    {/* Preferences */}
                    <div>
                        <label className="block text-sm font-semibold text-gray-700 mb-3">
                            Travel Preferences (optional)
                        </label>
                        <textarea
                            value={preferences}
                            onChange={(e) => setPreferences(e.target.value)}
                            placeholder="e.g., budget travel, luxury, adventure, cultural experiences..."
                            rows={3}
                            className="w-full px-5 py-4 rounded-xl border-2 border-gray-200 focus:border-purple-500 focus:outline-none transition-all duration-200 text-lg resize-none text-gray-900"
                            disabled={isLoading}
                        />
                    </div>

                    {/* Submit Button */}
                    <button
                        type="submit"
                        disabled={isLoading}
                        className="w-full py-5 px-8 rounded-xl bg-gradient-to-r from-purple-600 to-pink-600 text-white font-bold text-lg shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
                    >
                        {isLoading ? (
                            <span className="flex items-center justify-center gap-3">
                                <svg className="animate-spin h-6 w-6" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                                </svg>
                                Generating Your Travel Guide...
                            </span>
                        ) : (
                            '✨ Generate Travel Guide'
                        )}
                    </button>
                </form>
            </div>
        </div>
    );
}
