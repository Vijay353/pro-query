import React from 'react';

const samples = [
  {t:'Tech Stack', q:'What is your core tech stack and recent usage?'},
  {t:'Flagship Project', q:'Tell me about your flagship project with API, model and frontend.'},
  {t:'Achievements', q:'What are your recent achievements and impact metrics?'},
  {t:'Cloud & DevOps', q:'Describe your experience with cloud platforms and DevOps.'},
];

export default function Welcome({ onAsk }){
  return (
    <div className="welcome-message">
      <div className="welcome-title">Welcome to Portfolio AI</div>
      <p>Ask anything about the candidate's background, skills, and experience.</p>

      <div className="sample-prompts">
        {samples.map(s =>
          <div key={s.t} className="sample-prompt" onClick={()=>onAsk(s.q)}>
            <div className="sample-prompt-title">{s.t}</div>
            <div className="sample-prompt-text">{s.q}</div>
          </div>)}
      </div>
    </div>
  );
}