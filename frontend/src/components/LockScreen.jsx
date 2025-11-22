"use client";

import React, { useState, useEffect } from "react";
import ContentCard from "./ContentCard";
import RecommendationExplanation from "./RecommendationExplanation";

const API_URL = "http://localhost:8001";

const LockScreen = () => {
  const [card, setCard] = useState(null);

  const fetchNextCard = async () => {
    try {
      const response = await fetch(
        `${API_URL}/recommendation/next?user_id=U123`,
      );
      const data = await response.json();
      setCard(data);
    } catch (error) {
      console.error("Error fetching next card:", error);
    }
  };

  const sendInteraction = async (eventType) => {
    try {
      await fetch(`${API_URL}/events/interaction`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_id: "U123",
          content_id: card.content_id,
          event_type: eventType,
        }),
      });
    } catch (error) {
      console.error("Error sending interaction:", error);
    }
  };

  useEffect(() => {
    fetchNextCard();
  }, []);

  const handleSwipe = (direction) => {
    let eventType;
    if (direction === "left") {
      eventType = "dislike";
    } else if (direction === "right") {
      eventType = "like";
    } else {
      eventType = "skip";
    }
    sendInteraction(eventType);
    fetchNextCard();
  };

  if (!card) {
    return <div>Loading...</div>;
  }

  return (
    <div className="h-screen w-screen flex items-center justify-center bg-gray-800">
      <div className="w-[390px] h-[844px] bg-black rounded-[40px] border-8 border-gray-900 overflow-hidden">
        <div className="relative h-full w-full">
          <img
            src="https://images.unsplash.com/photo-1718889791712-4c4c4a7a7f2a?q=80&w=1974&auto=format&fit=crop"
            alt="Wallpaper"
            className="absolute inset-0 h-full w-full object-cover"
          />
          <div className="absolute inset-0 bg-black bg-opacity-20" />
          <div className="relative z-10 flex flex-col h-full p-6 text-white">
            <div className="flex justify-between items-center">
              <span className="text-2xl font-semibold">
                {new Date().toLocaleTimeString([], {
                  hour: "2-digit",
                  minute: "2-digit",
                })}
              </span>
              <span className="text-lg">
                {new Date().toLocaleDateString([], {
                  weekday: "long",
                  month: "long",
                  day: "numeric",
                })}
              </span>
            </div>
            <div className="flex-1 flex flex-col items-center justify-center">
              <ContentCard card={card} onSwipe={handleSwipe} />
              <RecommendationExplanation explanation={card.explanation} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LockScreen;
