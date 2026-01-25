'use client';

import { Clock, MapPin } from 'lucide-react';
import { DayItinerary } from '@/lib/api';

interface ItineraryDisplayProps {
    itinerary: DayItinerary[];
}

export default function ItineraryDisplay({ itinerary }: ItineraryDisplayProps) {
    return (
        <div className="space-y-8">
            <h2 className="text-4xl font-bold text-center bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-8">
                Your Personalized Itinerary
            </h2>

            {itinerary.map((day) => (
                <div key={day.day_number} className="bg-white rounded-2xl shadow-xl p-6 md:p-8 animate-fade-in">
                    {/* Day Header */}
                    <div className="border-b border-gray-200 pb-4 mb-6">
                        <div className="flex items-center justify-between flex-wrap gap-4">
                            <div>
                                <div className="flex items-center gap-3">
                                    <span className="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-4 py-2 rounded-full font-bold text-lg">
                                        Day {day.day_number}
                                    </span>
                                    <h3 className="text-2xl font-bold text-gray-800">{day.title}</h3>
                                </div>
                                {day.date && (
                                    <p className="text-gray-500 mt-2 ml-1">{day.date}</p>
                                )}
                            </div>
                            <div className="flex items-center gap-2 text-purple-600 font-medium">
                                <MapPin className="w-5 h-5" />
                                {day.location}
                            </div>
                        </div>
                    </div>

                    {/* Activities */}
                    <div className="space-y-6">
                        {day.activities.map((activity, index) => (
                            <div key={index} className="flex gap-4">
                                {/* Time Indicator */}
                                <div className="flex-shrink-0 w-24 text-center">
                                    <div className="bg-purple-50 rounded-lg px-3 py-2">
                                        <Clock className="w-5 h-5 mx-auto mb-1 text-purple-600" />
                                        <span className="text-sm font-semibold text-purple-700">
                                            {activity.time}
                                        </span>
                                    </div>
                                </div>

                                {/* Activity Content */}
                                <div className="flex-1 bg-gray-50 rounded-xl p-5 hover:bg-gray-100 transition-colors duration-200">
                                    <div className="flex items-start justify-between gap-4 mb-2">
                                        <h4 className="font-bold text-lg text-gray-800">{activity.activity}</h4>
                                        {activity.duration && (
                                            <span className="text-sm text-gray-500 bg-white px-3 py-1 rounded-full whitespace-nowrap">
                                                {activity.duration}
                                            </span>
                                        )}
                                    </div>
                                    <p className="text-gray-600 leading-relaxed">{activity.description}</p>
                                    {activity.location && (
                                        <p className="text-sm text-purple-600 mt-2 flex items-center gap-1">
                                            <MapPin className="w-4 h-4" />
                                            {activity.location}
                                        </p>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            ))}
        </div>
    );
}
