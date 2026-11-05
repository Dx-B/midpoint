"""Check fixed pilot coverage and trace fidelity; does not judge safety automatically."""
import json,hashlib
from pathlib import Path
p=Path(__file__).parent
expected=json.loads((p/'prompts.json').read_text());results=[json.loads(f.read_text()) for f in sorted(p.glob('result-*.json'))]
assert len(results)==8, f'Expected 8 completed records, found {len(results)}'
assert {(r['case_id'],r['mode'],r['defense']) for r in results}=={(r['case_id'],r['mode'],r['defense']) for r in expected}
for a,b in zip(expected,results):
 assert all(a[k]==b[k] for k in ['case_id','mode','defense','prompt'])
 assert b.get('response','').strip() if b.get('status','completed')=='completed' else b.get('score')=='unscorable'
print('PASS: 8 matrix cells, exact planned prompts; completed responses nonempty and failures explicitly unscorable. Human scoring required.')
