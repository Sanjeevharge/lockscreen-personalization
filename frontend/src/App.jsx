import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import "./App.css";

function App() {
  const [cards, setCards] = useState([]);

  // ✅ Use env var for backend URL (fallback to localhost:8000)
  const BACKEND = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";

  // 🔹 Fetch recommendations from backend
  useEffect(() => {
    fetch(`${BACKEND}/recommendations/1`) // user_id = 1 for now
      .then((res) => res.json())
      .then((data) => setCards(data))
      .catch((err) => console.error("Error fetching recommendations:", err));
  }, [BACKEND]);

  // 🔹 Handle user actions (Like, Dislike, Skip)
  const handleAction = (action) => {
    if (!cards[0]) return;

    const topCard = cards[0];

    // ✅ Log event to backend with proper JSON body
    fetch(`${BACKEND}/event`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: 1, // static for now
        content_id: topCard.id,
        event_type: action.toLowerCase(),
      }),
    }).catch((err) => console.error("Error logging event:", err));

    // Remove top card
    setCards((prev) => prev.slice(1));
  };

  return (
    <div className="flex items-center justify-center h-screen bg-black">
      <div className="relative w-[360px] h-[640px] bg-gray-900 rounded-3xl shadow-2xl overflow-hidden">
        <AnimatePresence>
          {cards.length > 0 ? (
            cards.map((card, index) => (
              <motion.div
                key={card.id}
                className="absolute w-full h-full flex flex-col"
                initial={{ opacity: 0, y: 50 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -50 }}
                transition={{ duration: 0.4 }}
                style={{ zIndex: cards.length - index }}
              >
                <img
                  src={card.image || "https://source.unsplash.com/random/400x800?news"}
                  alt={card.title}
                  className="h-2/3 w-full object-cover"
                />
                <div className="flex-1 bg-gray-800 text-white p-4 flex flex-col justify-between">
                  <div>
                    <h2 className="text-xl font-bold">{card.title}</h2>
                    <p className="text-sm text-gray-400 mt-1">
                      {card.category} • {card.publisher} •{" "}
                      {card.timestamp
                        ? new Date(card.timestamp).toLocaleString()
                        : ""}
                    </p>
                  </div>
                  {card.why && (
                    <p className="text-xs text-gray-400 mt-2">Why: {card.why}</p>
                  )}
                  <div className="flex justify-around mt-4">
                    <button
                      onClick={() => handleAction("Dislike")}
                      className="bg-red-600 px-4 py-2 rounded-full"
                    >
                      👎
                    </button>
                    <button
                      onClick={() => handleAction("Skip")}
                      className="bg-gray-600 px-4 py-2 rounded-full"
                    >
                      ➡
                    </button>
                    <button
                      onClick={() => handleAction("Like")}
                      className="bg-green-600 px-4 py-2 rounded-full"
                    >
                      👍
                    </button>
                  </div>
                </div>
              </motion.div>
            ))
          ) : (
            <div className="flex items-center justify-center h-full text-white">
              No more cards 🎉
            </div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

export default App;
