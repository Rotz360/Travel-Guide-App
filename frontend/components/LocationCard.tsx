'use client';

import Image from 'next/image';
import { MapPin, Star } from 'lucide-react';
import { LocationDetail } from '@/lib/api';

interface LocationCardProps {
    location: LocationDetail;
}

export default function LocationCard({ location }: LocationCardProps) {
    return (
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden transform transition-all duration-300 hover:scale-[1.02] hover:shadow-2xl">
            {/* Hero Image */}
            {location.main_image && (
                <div className="relative h-64 md:h-80 overflow-hidden">
                    <img
                        src={location.main_image.url}
                        alt={location.main_image.alt_text}
                        className="w-full h-full object-cover transition-transform duration-500 hover:scale-110"
                    />
                    <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 to-transparent p-6">
                        <h3 className="text-3xl font-bold text-white flex items-center gap-2">
                            <MapPin className="w-7 h-7" />
                            {location.name}
                        </h3>
                    </div>
                </div>
            )}

            {/* Content */}
            <div className="p-6 md:p-8">
                <p className="text-gray-700 text-lg leading-relaxed mb-6">
                    {location.description}
                </p>

                {/* Highlights */}
                {location.highlights && location.highlights.length > 0 && (
                    <div>
                        <h4 className="font-bold text-xl mb-4 flex items-center gap-2 text-purple-600">
                            <Star className="w-5 h-5" />
                            Must-See Highlights
                        </h4>
                        <ul className="space-y-3">
                            {location.highlights.map((highlight, index) => (
                                <li key={index} className="flex items-start gap-3">
                                    <span className="flex-shrink-0 w-2 h-2 bg-gradient-to-r from-purple-600 to-pink-600 rounded-full mt-2" />
                                    <span className="text-gray-700">{highlight}</span>
                                </li>
                            ))}
                        </ul>
                    </div>
                )}

                {/* Additional Images */}
                {location.additional_images && location.additional_images.length > 0 && (
                    <div className="mt-6 grid grid-cols-3 gap-3">
                        {location.additional_images.map((image, index) => (
                            <div key={index} className="relative h-24 rounded-lg overflow-hidden">
                                <img
                                    src={image.url}
                                    alt={image.alt_text}
                                    className="w-full h-full object-cover transition-transform duration-300 hover:scale-110"
                                />
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}
