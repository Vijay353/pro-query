import React, { useState, useEffect } from 'react';
import './Welcome.css';

const sampleCategories = [
  {
    icon: '💼',
    title: 'Professional Background',
    color: '#0165E1',
    prompts: [
      { label: 'Tech Stack', question: 'What is your core tech stack and recent usage?' },
      { label: 'Experience Summary', question: 'Summarize your professional experience in 2 minutes.' },
    ]
  },
  {
    icon: '🚀',
    title: 'Projects & Achievements',
    color: '#17A9FD',
    prompts: [
      { label: 'Flagship Project', question: 'Tell me about your flagship project with API, model and frontend.' },
      { label: 'Impact Metrics', question: 'What are your recent achievements and measurable impact?' },
    ]
  },
  {
    icon: '☁️',
    title: 'Technical Skills',
    color: '#0165E1',
    prompts: [
      { label: 'Cloud & DevOps', question: 'Describe your experience with cloud platforms and DevOps practices.' },
      { label: 'Latest Technologies', question: 'What are the most recent technologies you\'ve worked with?' },
    ]
  },
  {
    icon: '📊',
    title: 'Quick Insights',
    color: '#17A9FD',
    prompts: [
      { label: 'Unique Strengths', question: 'What makes this candidate stand out from others?' },
      { label: 'Team Collaboration', question: 'How does this candidate work in team environments?' },
    ]
  }
];

const quickStats = [
  { icon: '⚡', label: 'Years Experience', value: '5+' },
  { icon: '🎯', label: 'Projects Completed', value: '20+' },
  { icon: '🛠️', label: 'Technologies', value: '15+' },
  { icon: '🏆', label: 'Certifications', value: '8' },
];

// Default profile images for different genders
const DEFAULT_AVATARS = {
  male: 'https://api.dicebear.com/7.x/avataaars/svg?seed=male-professional&backgroundColor=0165E1',
  female: 'https://api.dicebear.com/7.x/avataaars/svg?seed=female-professional&backgroundColor=17A9FD',
  neutral: 'https://api.dicebear.com/7.x/bottts/svg?seed=ai-professional&backgroundColor=0165E1'
};

export default function Welcome({ onAsk, profileImage, gender = 'neutral' }) {
  const [activeCategory, setActiveCategory] = useState(0);
  const [isVisible, setIsVisible] = useState(false);
  const [imageError, setImageError] = useState(false);

  useEffect(() => {
    setIsVisible(true);
  }, []);

  // Determine which image to use
  const getProfileImage = () => {
    if (profileImage && !imageError) {
      return profileImage;
    }
    return DEFAULT_AVATARS[gender] || DEFAULT_AVATARS.neutral;
  };

  const handleImageError = () => {
    setImageError(true);
  };

  return (
    <div className={`welcome-container ${isVisible ? 'visible' : ''}`}>
      {/* Animated Background Elements */}
      <div className="welcome-bg-orbs">
        <div className="orb orb-1"></div>
        <div className="orb orb-2"></div>
        <div className="orb orb-3"></div>
      </div>

      {/* Main Welcome Content */}
      <div className="welcome-content">
        {/* Hero Section */}
        <div className="welcome-hero">
          <div className="welcome-avatar">
            <div className="avatar-ring"></div>
            <div className="avatar-inner">
              <img 
                src={getProfileImage()} 
                alt="Profile"
                className="avatar-image"
                onError={handleImageError}
              />
            </div>
          </div>
          
          <h1 className="welcome-title">
            Welcome to Portfolio AI
          </h1>
          
          <p className="welcome-subtitle">
            Ask me anything about the candidate's background, skills, projects, and experience.
            <br />
            I'll provide detailed insights backed by real data.
          </p>
        </div>

        {/* Quick Stats */}
        <div className="quick-stats">
          {quickStats.map((stat, index) => (
            <div 
              key={stat.label} 
              className="stat-card"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className="stat-icon">{stat.icon}</div>
              <div className="stat-content">
                <div className="stat-value">{stat.value}</div>
                <div className="stat-label">{stat.label}</div>
              </div>
            </div>
          ))}
        </div>

        {/* Category Tabs */}
        <div className="category-tabs">
          {sampleCategories.map((category, index) => (
            <button
              key={category.title}
              className={`category-tab ${activeCategory === index ? 'active' : ''}`}
              onClick={() => setActiveCategory(index)}
              style={{
                '--tab-color': category.color
              }}
            >
              <span className="category-icon">{category.icon}</span>
              <span className="category-name">{category.title}</span>
            </button>
          ))}
        </div>

        {/* Sample Prompts */}
        <div className="prompts-container">
          {sampleCategories[activeCategory].prompts.map((prompt, index) => (
            <div
              key={prompt.label}
              className="prompt-card"
              onClick={() => onAsk(prompt.question)}
              style={{ 
                animationDelay: `${index * 0.1}s`,
                '--card-color': sampleCategories[activeCategory].color
              }}
            >
              <div className="prompt-header">
                <span className="prompt-label">{prompt.label}</span>
                <span className="prompt-arrow">→</span>
              </div>
              <p className="prompt-question">{prompt.question}</p>
            </div>
          ))}
        </div>

        {/* Quick Start Section */}
        <div className="quick-start">
          <div className="quick-start-icon">💡</div>
          <div className="quick-start-text">
            <strong>Pro Tip:</strong> Be specific in your questions to get detailed, actionable insights.
          </div>
        </div>
      </div>
    </div>
  );
}