import React from 'react';
import { motion } from 'framer-motion';

const ContentCard = ({ card, onSwipe }) => {
  return (
    <motion.div
      className="w-full max-w-sm bg-white rounded-2xl shadow-lg overflow-hidden"
      drag="x"
      dragConstraints={{ left: -100, right: 100 }}
      onDragEnd={(event, info) => {
        if (info.offset.x > 50) {
          onSwipe('right');
        } else if (info.offset.x < -50) {
          onSwipe('left');
        }
      }}
    >
      <img className="w-full h-48 object-cover" src={card.image_url} alt={card.title} />
      <div className="p-4">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-semibold text-gray-500">{card.category}</span>
          <span className="text-xs text-gray-400">{card.publisher}</span>
        </div>
        <h3 className="text-lg font-bold text-gray-800 mb-2">{card.title}</h3>
        <p className="text-sm text-gray-600">{card.timestamp}</p>
        <div className="flex justify-around mt-4">
          <button onClick={() => onSwipe('left')} className="text-red-500 hover:text-red-700">👎 Dislike</button>
          <button onClick={() => onSwipe('down')} className="text-gray-500 hover:text-gray-700">➡ Skip</button>
          <button onClick={() => onSwipe('right')} className="text-green-500 hover:text-green-700">👍 Like</button>
        </div>
      </div>
    </motion.div>
  );
};

export default ContentCard;
