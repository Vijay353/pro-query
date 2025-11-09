import React from 'react';

const SECTIONS = [
  'ABOUT', 'EXPERIENCE', 'PROJECTS', 'CASE STUDIES', 'SKILLS', 'CERTIFICATIONS', 'EDUCATION'
];

export default function SectionPicker({ onPick }) {
  return (
    <div style={{
      position: 'absolute',
      bottom: 70,
      left: 16,
      background: '#0f1628',
      border: '1px solid #252a36',
      borderRadius: 12,
      padding: 8,
      zIndex: 10
    }}>
      {SECTIONS.map(s => (
        <button key={s} className="btn" onClick={() => onPick(s)}>{s}</button>
      ))}
    </div>
  );
}
