import React, { useState, useEffect } from 'react';

export default function HeaderBar() {
  const [shareOpen, setShareOpen] = useState(false);
  const [likeCount, setLikeCount] = useState(0);
  const [isLiked, setIsLiked] = useState(false);

  // Load likes from localStorage
  useEffect(() => {
    const savedLikes = localStorage.getItem('portfolioLikes');
    const savedLiked = localStorage.getItem('portfolioIsLiked');

    if (savedLikes) setLikeCount(parseInt(savedLikes, 10));
    if (savedLiked) setIsLiked(savedLiked === 'true');
  }, []);

  // Handle like toggle
  const handleLike = () => {
    const newLiked = !isLiked;
    const newCount = newLiked ? likeCount + 1 : Math.max(0, likeCount - 1);
    setIsLiked(newLiked);
    setLikeCount(newCount);
    localStorage.setItem('portfolioLikes', newCount);
    localStorage.setItem('portfolioIsLiked', newLiked);
  };

  // Handle share menu actions
  const handleShare = (platform) => {
    const url = window.location.href;
    if (platform === 'link') {
      navigator.clipboard.writeText(url)
        .then(() => alert('Link copied to clipboard!'))
        .catch(() => alert('Failed to copy link'));
    } else if (platform === 'linkedin') {
      window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${url}`, '_blank');
    } else if (platform === 'gmail') {
      window.open(`https://mail.google.com/mail/?view=cm&body=${url}`, '_blank');
    } else if (platform === 'twitter') {
      window.open(`https://twitter.com/intent/tweet?url=${url}`, '_blank');
    }
    setShareOpen(false);
  };

  return (
    <header className="header">
      <div className="header-title">Portfolio AI</div>

      <div className="header-actions" style={{ position: 'relative' }}>
        {/* Share Button */}
        <div style={{ position: 'relative' }}>
          <button className="btn" onClick={() => setShareOpen(!shareOpen)}>
            Share
          </button>
          {shareOpen && (
            <div className="share-dropdown show">
              <div className="share-item" onClick={() => handleShare('link')}>🔗 Copy Link</div>
              <div className="share-item" onClick={() => handleShare('linkedin')}>💼 LinkedIn</div>
              <div className="share-item" onClick={() => handleShare('gmail')}>📧 Gmail</div>
              <div className="share-item" onClick={() => handleShare('twitter')}>🐦 Twitter</div>
            </div>
          )}
        </div>

        {/* Like Button */}
        <button
          className={`btn like-btn ${isLiked ? 'liked' : ''}`}
          onClick={handleLike}
          title={isLiked ? 'Unlike' : 'Like'}
        >
          {isLiked ? '❤️' : '🤍'} {likeCount}
        </button>
      </div>
    </header>
  );
}
