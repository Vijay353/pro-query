import { SAMPLE_PROMPTS } from '../data/samplePrompts'
export default function Library(){
return (
<div>
<h4>Example questions</h4>
<ul>
{SAMPLE_PROMPTS.map(p => <li key={p}>{p}</li>)}
</ul>
</div>
)
}