#!/usr/bin/env python3
"""Retain actual delegated-run artifacts. Never generates answers or grades."""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
from zoneinfo import ZoneInfo


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def artifact(path: Path, repo: Path) -> dict:
    return {'path': path.relative_to(repo).as_posix(), 'sha256': sha(path)}


def retain(path: Path, data: bytes) -> None:
    if path.exists():
        if path.read_bytes() != data:
            raise ValueError(f'Refusing to overwrite retained evidence: {path}')
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--run-id', required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--agent-task', required=True)
    parser.add_argument('--snapshot', default='round-1')
    parser.add_argument('--retest-of', action='append', default=[])
    args = parser.parse_args()
    if not re.fullmatch(r'P1-U\d{2}-V\d{2}-R\d+', args.run_id):
        raise ValueError('Unexpected run ID')
    repo = args.repo_root.resolve()
    run_dir = repo / 'tests/phase-3/runs' / args.run_id
    if (run_dir / 'run.json').exists():
        print(f'Already captured: {args.run_id}; no evidence overwritten')
        return 0
    output_dir = args.output_dir.resolve()
    if not output_dir.is_dir() or not output_dir.is_relative_to(Path('/private/tmp')):
        raise ValueError('Expected the isolated /private/tmp execution output directory')
    for filename in ['output.md', 'tool-trace.json']:
        if not (output_dir / filename).is_file():
            raise ValueError(f'Missing actual executor artifact: {filename}')
    retained = []
    for source in sorted(output_dir.rglob('*')):
        if source.is_symlink():
            raise ValueError('Symlink not permitted in retained output')
        if source.is_file():
            dest = run_dir / 'artifacts' / source.relative_to(output_dir)
            retain(dest, source.read_bytes())
            retained.append(artifact(dest, repo))
    trace = json.loads((run_dir / 'artifacts/tool-trace.json').read_text())
    variant = args.run_id.rsplit('-R', 1)[0]
    case = variant.rsplit('-V', 1)[0]
    matrix_path = repo / 'tests/phase-3/acceptance-matrix.json'
    matrix = json.loads(matrix_path.read_text())
    case_spec = next(c for c in matrix['matrix']['cases'] if c['id'] == case)
    now = datetime.now(ZoneInfo('Asia/Ho_Chi_Minh')).isoformat()
    execution = {
        'run_id': args.run_id, 'task_name': args.agent_task,
        'dispatch_mechanism': 'collaboration.spawn_agent', 'fork_turns': 'none',
        'recorded_at': now, 'execution_observed_by': 'root Codex task',
        'retention_method': 'Copy actual files written by the delegated executor after completion',
        'model_identifier': 'not_available',
        'limitations': ['No full exported host transcript is available; tool-trace.json is executor-maintained.',
                       'Fresh context is from fork_turns=none; inherited system/developer instructions still apply.']
    }
    execution_path = run_dir / 'execution-record.json'
    retain(execution_path, (json.dumps(execution, ensure_ascii=False, indent=2)+'\n').encode())
    fixture_dir = repo / 'tests/phase-3/fixtures' / variant
    inputs = [{'fixture_id': variant+':'+p.name, 'version':'1', 'artifact':artifact(p, repo)}
              for p in sorted(fixture_dir.iterdir()) if p.is_file()]
    inputs.append({'fixture_id':'execution-harness','version':'1',
                   'artifact':artifact(repo/'tests/phase-3/harness.md', repo)})
    simulated = case in ['P1-U07', 'P1-U08', 'P1-U17']
    record = {
        'run_id': args.run_id, 'case_id': case, 'variant_id': variant,
        'requirement_ids': case_spec['requirements'],
        'timestamp': trace.get('started_at', now), 'verification_mode':'model',
        'execution_status':'executed',
        'runtime': {
          'platform':'Codex', 'surface':'Codex desktop delegated local runtime',
          'runtime':'collaboration.spawn_agent', 'model':None,
          'model_identifier_status':'not_available', 'fresh_context':True,
          'capabilities': {'local_file_read':'available',
            'external_lookup': 'authorized_read_only' if case=='P1-U06' else 'prohibited_by_run_policy',
            'specialist': 'authorized_local_document_evidence' if variant=='P1-U16-V01' else 'not_invoked'},
          'capability_simulation':simulated
        },
        'authorized_source_scope':'Frozen skill; this fixture; harness; necessary local readers. Public official web only for U06; local Document-Evidence only for U16-V01.',
        'inputs':inputs,
        'skill_snapshot':artifact(repo/f'tests/phase-3/snapshots/{args.snapshot}/manifest.json',repo),
        'raw_prompt':artifact(run_dir/'prompt.txt',repo),
        'raw_output':artifact(run_dir/'artifacts/output.md',repo),
        'tool_trace':artifact(run_dir/'artifacts/tool-trace.json',repo),
        'execution_record':artifact(execution_path,repo),
        'review':None, 'retest_of':args.retest_of, 'additional_artifacts':retained,
        'limitations':['Synthetic business inputs, not real-organization assurance.',
                       'Executor-maintained trace, not a complete exported host transcript.',
                       'Exact model identifier is not exposed by this delegation interface.']
    }
    if simulated:
        record['limitations'].append('Capability/access conditions are simulated test conditions; not platform capability verification.')
    retain(run_dir/'run.json', (json.dumps(record, ensure_ascii=False, indent=2)+'\n').encode())
    print(json.dumps({'captured':args.run_id, 'retained_artifacts':len(retained), 'review_status':'executed_unreviewed'}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
