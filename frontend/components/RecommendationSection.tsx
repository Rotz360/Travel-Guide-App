'use client';

import { Hotel, Utensils, Sparkles } from 'lucide-react';
import { Recommendation } from '@/lib/api';

interface RecommendationSectionProps {
    recommendations: {
        sleep: Recommendation[];
        eat: Recommendation[];
        curiosities: Recommendation[];
    };
}

export default function RecommendationSection({ recommendations }: RecommendationSectionProps) {
    const categories = [
        {
            key: 'sleep' as const,
            title: 'Where to Stay',
            icon: Hotel,
            items: recommendations.sleep,
            gradient: 'from-blue-500 to-cyan-500',
        },
        {
            key: 'eat' as const,
            title: 'Where to Eat',
            icon: Utensils,
            items: recommendations.eat,
            gradient: 'from-orange-500 to-red-500',
        },
        {
            key: 'curiosities' as const,
            title: 'Local Curiosities',
            icon: Sparkles,
            items: recommendations.curiosities,
            gradient: 'from-purple-500 to-pink-500',
        },
    ];

    return (
        <div className="space-y-12">
            <h2 className="text-4xl font-bold text-center bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                Recommendations & Tips
            </h2>

            {categories.map((category) => (
                <div key={category.key} className="animate-fade-in">
                    {/* Category Header */}
                    <div className="flex items-center gap-3 mb-6">
                        <div className={`p-3 rounded-xl bg-gradient-to-r ${category.gradient} text-white shadow-lg`}>
                            <category.icon className="w-7 h-7" />
                        </div>
                        <h3 className="text-3xl font-bold text-gray-800">{category.title}</h3>
                    </div>

                    {/* Recommendations Grid */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {category.items.map((item, index) => (
                            <div
                                key={index}
                                className="bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1"
                            >
                                {/* Image */}
                                {item.image && (
                                    <div className="relative h-48 overflow-hidden">
                                        <img
                                            src={item.image.url}
                                            alt={item.image.alt_text}
                                            className="w-full h-full object-cover transition-transform duration-500 hover:scale-110"
                                        />
                                        {item.price_level && (
                                            <div className="absolute top-3 right-3 bg-white/90 backdrop-blur-sm px-3 py-1 rounded-full text-sm font-bold">
                                                {item.price_level}
                                            </div>
                                        )}
                                    </div>
                                )}

                                {/* Content */}
                                <div className="p-5">
                                    <h4 className="font-bold text-xl mb-2 text-gray-800">{item.name}</h4>
                                    <p className="text-gray-600 text-sm mb-3 leading-relaxed">
                                        {item.description}
                                    </p>

                                    {/* Why Recommended */}
                                    <div className={`bg-gradient-to-r ${category.gradient} bg-opacity-10 rounded-lg p-3 border-l-4 border-gradient-to-r ${category.gradient}`}>
                                        <p className="text-sm font-medium text-gray-700">
                                            <span className="font-bold">Why: </span>
                                            {item.why_recommended}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            ))}
        </div>
    );
}
