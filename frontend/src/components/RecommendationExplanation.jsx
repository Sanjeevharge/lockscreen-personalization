import React from 'react';

const RecommendationExplanation = ({ explanation }) => {
  return (
    <div className="text-center text-xs text-gray-400 mt-4">
      <p>{explanation}</p>
    </div>
  );
};

export default RecommendationExplanation;
