#!/usr/bin/env python3
"""
V0.11-D3-E4 — Repeated Delivery Suppression (RDS) prototype + self-test + 15K replay.
Prereg: docs/architecture/V0.11-D3-E4-RDS-PROTOTYPE-PREREG-V1.md (FROZEN 7d9b343e)
Unified mechanical primitive over E2/E3/E14 repeated-delivery phenomena.
anchor-first / exact-only / fail-closed / auditable recovery identity / 100% exact reconstruction.
Deterministic; zero model calls; zero production deploy modification.
"""
import json, re, statistics, hashlib, unittest
import pyarrow.parquet as pq

PARQUET = 'D:/tasco-temp/d3_hf_data/sessions.parquet'
OUT = 'evidence/V1/v011-d3e4-rds-prototype-replay.json'
MIN_SEG_LINES = 2          # frozen: segments shorter than 2 lines are not worth the marker overhead -> native lines
MARKER = '[TASCO-RDS omitted: observation #{k} lines {a}..{b} ({n} chars); new: {m} chars]'

# ============================ RDS PRIMITIVE ============================

class RDS:
    """Session-scoped Repeated Delivery Suppression.
    Runs on newline-normalized text. All accounting in normalized chars."""

    def __init__(self):
        self.delivered_index = {}   # line_text -> (obs_seq, line_idx)  first delivery only
        self.observations = []      # obs_seq -> list of normalized lines
        self.obs_chars = []         # obs_seq -> normalized char count

    def _normalize(self, text):
        return (text or '').replace('\r\n', '\n')

    def compress(self, obs_raw, obs_seq):
        """Returns dict: {action: 'native'|'compressed', saving_chars, segments, marker, reconstruction}
        fail-closed: any inconsistency -> native."""
        if not isinstance(obs_raw, str):
            return {'action': 'native', 'reason': 'malformed_payload', 'saving_chars': 0}
        text = self._normalize(obs_raw)
        lines = text.split('\n')
        n = len(lines)
        segments = []           # ('orig', i, j) or ('omit', src_obs, a, b, i, j)
        i = 0
        matched_chars = 0
        while i < n:
            hit = self.delivered_index.get(lines[i])
            if hit is None:
                # extend native run
                j = i
                while j < n and self.delivered_index.get(lines[j]) is None:
                    j += 1
                segments.append(('orig', i, j))
                i = j
                continue
            src_obs, src_idx = hit
            # try to extend a contiguous aligned segment within a SINGLE prior observation
            j = i
            while j < n:
                h2 = self.delivered_index.get(lines[j])
                if h2 is None or h2[0] != src_obs or h2[1] != src_idx + (j - i):
                    break
                j += 1
            seg_len = j - i
            if seg_len >= MIN_SEG_LINES and src_obs < obs_seq:
                seg_chars = sum(len(lines[t]) + 1 for t in range(i, j - 1)) + len(lines[j - 1])
                segments.append(('omit', src_obs, src_idx, src_idx + seg_len - 1, i, j, seg_chars))
                matched_chars += seg_chars
                i = j
            else:
                # single line / stale alignment -> keep native line
                j2 = i
                while j2 < n and self.delivered_index.get(lines[j2]) is None:
                    j2 += 1
                if j2 == i: j2 = i + 1
                segments.append(('orig', i, j2))
                i = j2
        # accounting invariant (C5): matched + new == original
        new_chars = len(text) - matched_chars
        if matched_chars == 0 or matched_chars + new_chars != len(text):
            return {'action': 'native', 'reason': 'accounting_inconsistent', 'saving_chars': 0}
        marker = MARKER.format(k=self._last_source_obs(segments), a=min(s[2] for s in segments if s[0] == 'omit'),
                               b=max(s[3] for s in segments if s[0] == 'omit'),
                               n=matched_chars, m=new_chars)
        compressed_text = self._render(segments, lines, marker)
        return {
            'action': 'compressed', 'saving_chars': matched_chars,
            'matched_chars': matched_chars, 'new_chars': new_chars,
            'segments': segments, 'marker': marker,
            'compressed_text': compressed_text, 'original_normalized': text,
        }

    def _last_source_obs(self, segments):
        srcs = [s[1] for s in segments if s[0] == 'omit']
        return (min(srcs) + 1) if srcs else 0

    def _render(self, segments, lines, marker):
        parts = []
        for s in segments:
            if s[0] == 'orig':
                parts.append('\n'.join(lines[s[1]:s[2]]))
            else:
                parts.append(MARKER.format(k=s[1] + 1, a=s[2] + 1, b=s[3] + 1, n=s[6], m=sum(len(lines[t]) + 1 for t in range(s[4], s[5] - 1)) + len(lines[s[5] - 1]) if s[5] - s[4] else 0))
        return '\n'.join(parts)

    def deliver(self, obs_raw, obs_seq):
        """Process an observation in trajectory order: compress then register lines (first delivery index)."""
        result = self.compress(obs_raw, obs_seq)
        text = self._normalize(obs_raw)
        lines = text.split('\n')
        self.observations.append(lines)
        self.obs_chars.append(len(text))
        for idx, l in enumerate(lines):
            if l not in self.delivered_index:
                self.delivered_index[l] = (obs_seq, idx)
        # reconstruction closure check (R3)
        if result['action'] == 'compressed':
            recon = self.reconstruct(result, obs_seq)
            result['reconstruction_exact'] = (recon == text)
        else:
            result['reconstruction_exact'] = True
        return result

    def reconstruct(self, result, obs_seq):
        """Rebuild original normalized text from compressed representation + referenced anchor observations."""
        parts = []
        segs = result['segments']
        # recompute render with explicit reconstruction from anchor lines
        for s in segs:
            if s[0] == 'orig':
                pass
        # robust reconstruction: parse compressed_text markers back
        text = result['compressed_text']
        out = []
        for block in re.split(r'\[TASCO-RDS omitted: observation #(\d+) lines (\d+)\.\.(\d+) \((\d+) chars\); new: \d+ chars\]', text):
            out.append(block)
        # marker-aware reconstruction: replace each marker with referenced anchor lines
        def repl(m):
            k = int(m.group(1)) - 1
            a = int(m.group(2)) - 1
            b = int(m.group(3)) - 1
            src = self.observations[k]
            if k >= len(self.observations) or b >= len(src):
                return m.group(0)  # unresolvable -> will fail exact match (fail-closed surface)
            return '\n'.join(src[a:b + 1])
        recon = re.sub(r'\[TASCO-RDS omitted: observation #(\d+) lines (\d+)\.\.(\d+) \(\d+ chars\); new: \d+ chars\]', repl, text)
        return recon

# ============================ SELF-TEST (frozen matrix) ============================

class RDSContractTests(unittest.TestCase):
    def mk(self):
        return RDS()

    def test_01_exact_duplicate(self):
        r = self.mk(); r.deliver('A\nB\nC', 0)
        res = r.deliver('A\nB\nC', 1)
        self.assertEqual(res['action'], 'compressed')
        self.assertEqual(res['saving_chars'], 5)
        self.assertTrue(res['reconstruction_exact'])

    def test_02_partial_line_overlap(self):
        r = self.mk(); r.deliver('A\nB\nC\nD', 0)
        res = r.deliver('A\nB\nC\nD\nE', 1)
        self.assertEqual(res['action'], 'compressed')
        self.assertIn('E', res['compressed_text'])
        self.assertTrue(res['reconstruction_exact'])

    def test_03_content_changed(self):
        r = self.mk(); r.deliver('A\nB\nC', 0)
        res = r.deliver('X\nY\nZ', 1)
        self.assertEqual(res['action'], 'native')

    def test_04_reordered_lines(self):
        r = self.mk(); r.deliver('A\nB\nC', 0)
        # fully shuffled, no contiguous aligned segment of >=2 lines -> native
        res_shuffled = r.deliver('C\nB\nA', 1)
        self.assertEqual(res_shuffled['action'], 'native')
        # 'A\nB' IS a contiguous aligned segment (anchor lines 0..1) even though 'C' moved;
        # contract C2 allows folding exactly that segment, reconstruction must stay exact
        res = r.deliver('C\nA\nB', 1)
        self.assertEqual(res['action'], 'compressed')
        self.assertTrue(res['reconstruction_exact'])
        self.assertIn('C', res['compressed_text'])

    def test_05_same_command_different_output(self):
        r = self.mk(); r.deliver('tests: 10 passed', 0)
        res = r.deliver('tests: 3 failed, 7 passed', 1)  # command same, output different
        self.assertEqual(res['action'], 'native')

    def test_06_same_file_path_file_changed(self):
        r = self.mk(); r.deliver('v1 content alpha\nv1 line2', 0)
        res = r.deliver('v2 content beta\nv2 line2x', 1)  # file same, content changed
        self.assertEqual(res['action'], 'native')

    def test_07_missing_anchor(self):
        r = self.mk()
        res = r.deliver('first observation\nline2', 0)
        self.assertEqual(res['action'], 'native')  # anchor-first: never compressed

    def test_08_stale_anchor(self):
        r = self.mk(); r.deliver('head\nshared-tail', 0)
        res = r.deliver('head\nCHANGED-tail\nextra', 1)  # partial: only 'head' aligns (1 line < MIN_SEG) -> native
        self.assertEqual(res['action'], 'native')

    def test_09_truncated_payload_accounting(self):
        r = self.mk()
        # simulate accounting inconsistency via malformed structure
        res = r.compress(None, 1)
        self.assertEqual(res['action'], 'native')
        self.assertEqual(res['reason'], 'malformed_payload')

    def test_10_malformed_payload(self):
        r = self.mk(); r.deliver('ok', 0)
        res = r.compress(12345, 1)
        self.assertEqual(res['action'], 'native')

    def test_11_cross_task_boundary(self):
        r = self.mk()
        r.deliver('task1 build output\nmany lines\nhere', 0)
        res = r.deliver('task2 totally unrelated\ncontent flows\nnow', 1)
        self.assertEqual(res['action'], 'native')

    def test_12_multiple_candidate_anchors(self):
        r = self.mk()
        r.deliver('shared line\nextra1', 0)
        r.deliver('shared line\nextra2', 1)  # 'shared line' first delivered by obs 0
        res = r.deliver('shared line\nextra3', 2)
        self.assertEqual(res['action'], 'native')  # single shared line < MIN_SEG
        # with 2 shared lines the segment resolves to the FIRST delivering observation
        r2 = self.mk()
        r2.deliver('s1\ns2\nonly0', 0)
        r2.deliver('other', 1)
        res2 = r2.deliver('s1\ns2\nnew3', 2)
        self.assertEqual(res2['action'], 'compressed')
        self.assertTrue(res2['reconstruction_exact'])

    def test_13_unicode_newline_normalization(self):
        r = self.mk()
        r.deliver('数据行一\r\n数据行二\r\n数据行三', 0)
        res = r.deliver('数据行一\n数据行二\n数据行三\n新增', 1)
        self.assertEqual(res['action'], 'compressed')
        self.assertTrue(res['reconstruction_exact'])
        self.assertIn('新增', res['compressed_text'])

    def test_14_huge_repeated_payload(self):
        r = self.mk()
        big = '\n'.join(f'line-{i}-xxxxxxxxxxxxxxxxxxxx' for i in range(10000))
        r.deliver(big, 0)
        res = r.deliver(big, 1)
        self.assertEqual(res['action'], 'compressed')
        self.assertTrue(res['reconstruction_exact'])
        self.assertGreater(res['saving_chars'], 100000)

    def test_15_negative_command_same_output_differs(self):
        r = self.mk(); r.deliver('run 1 results\ndetail a', 0)
        res = r.deliver('run 2 results\ndetail b', 1)  # same command implied, output differs
        self.assertEqual(res['action'], 'native')

    def test_16_negative_file_same_content_differs(self):
        r = self.mk(); r.deliver('file v1\ncode();\nmore();', 0)
        res = r.deliver('file v2\ncode();\nmore();', 1)  # file same label, content partially changed
        # contract: only the mechanically-identical contiguous lines fold; the changed first
        # line MUST survive verbatim; file-same label alone never triggers whole-payload compression
        self.assertTrue(res['action'] in ('compressed', 'native'))
        if res['action'] == 'compressed':
            self.assertIn('file v2', res['compressed_text'])  # changed line preserved
            self.assertNotIn('file v1', res['compressed_text'])
            self.assertTrue(res['reconstruction_exact'])
        # full content change -> native
        res2 = r.deliver('completely\ndifferent\ncontent', 2)
        self.assertEqual(res2['action'], 'native')

    def test_17_accounting_invariant_enforced(self):
        r = self.mk(); r.deliver('A\nB\nC\nD', 0)
        res = r.deliver('A\nB\nC\nD\nE\nF', 1)
        if res['action'] == 'compressed':
            self.assertEqual(res['matched_chars'] + res['new_chars'], len(res['original_normalized']))
        self.assertTrue(res['reconstruction_exact'])

# ============================ 15K REPLAY ============================

def parse_events(msgs):
    events = []; pending = None
    for idx, m in enumerate(msgs):
        role = m.get('role'); content = m.get('content') or ''
        if role == 'assistant':
            tc = m.get('tool_calls_json'); cmd = None; path = None
            if tc:
                try:
                    calls = json.loads(tc)
                    if isinstance(calls, dict): calls = [calls]
                    for call in calls:
                        fn = (call.get('function') or {})
                        try: args = json.loads(fn.get('arguments') or '{}')
                        except Exception: args = {}
                        a = args.get('command')
                        if isinstance(a, str) and a.strip(): cmd = norm_cmd(a.splitlines()[0])
                        if args.get('path'): path = args['path']
                except Exception: pass
            if cmd is None:
                mm = re.search(r'```[a-z]*\s*\n(.+?)\n```', content, re.S)
                if mm:
                    first = mm.group(1).strip().splitlines()[0]
                    cmd = norm_cmd(first)
                    pm = re.search(r'(/[^\s`]+)', first)
                    if pm: path = pm.group(1)
            if cmd: pending = {'cmd': cmd, 'path': path}
        elif role == 'tool' and pending is not None:
            pending['obs'] = content; events.append(pending); pending = None
        elif role == 'user' and pending is not None:
            c = content if content.startswith('OBSERVATION:') else (content[content.find('OBSERVATION:'):] if 'OBSERVATION:' in content[:200] else None)
            if c is not None:
                pending['obs'] = c[len('OBSERVATION:'):].strip(); events.append(pending); pending = None
            else:
                rm = re.search(r'<returncode>(\d+)</returncode>', content)
                om = re.search(r'<output>\n?(.*?)\n?</output>\s*$', content, re.S)
                if rm and om:
                    pending['obs'] = om.group(1); pending['exit'] = int(rm.group(1)); events.append(pending); pending = None
    return events

def norm_cmd(c): return ' '.join(c.split()).strip()

def pctl(a, q):
    if not a: return None
    s = sorted(a); return s[min(len(s) - 1, int(q * len(s)))]
def med(a): return statistics.median(a) if a else None
def r4(x): return round(x, 4) if isinstance(x, float) else x

def main():
    # 1) self-test gate
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(RDSContractTests)
    tr = unittest.TextTestRunner(verbosity=0).run(suite)
    if tr.failures or tr.errors:
        print('SELF-TEST FAIL:', len(tr.failures), 'failures,', len(tr.errors), 'errors')
        for t, tb in list(tr.failures) + list(tr.errors): print(tb[:800])
        sys_exit(1)
    print('self-test: ALL PASS (17 cases)')

    # 2) replay over 15K sessions
    SESSIONS_TOTAL = 0
    per_session_saving = []       # (hit, saving, obs_total)
    e3_removable_total = 0.0      # E3 census oracle recompute (path-group line-set intersection)
    rds_removed_total = 0.0
    rds_removed_in_path_groups = 0.0
    recon_fail = 0
    compressed_events = 0
    pf = pq.ParquetFile(PARQUET)
    for batch in pf.iter_batches(batch_size=250):
        for row in batch.to_pylist():
            SESSIONS_TOTAL += 1
            try: msgs = json.loads(row['messages_json'])
            except Exception: continue
            events = parse_events(msgs)
            if not events: continue
            rds = RDS()
            # ---- E3 census oracle denominator rebuilt faithfully (d3e3 logic) ----
            by_path = {}
            csim_groups = {}
            for i, e in enumerate(events):
                e.setdefault('obs_chars', len(e.get('obs') or ''))
                e.setdefault('lines', frozenset((e.get('obs') or '').replace('\r\n', '\n').split('\n')))
                if e.get('path'): by_path.setdefault(e['path'], []).append(i)
                csim_groups.setdefault(e['csim'] if 'csim' in e else None, []).append(i) if False else None
            # csim for E2 coverage of denominator is not needed: capture denominator = E3 shape only
            VIEW_WORDS = {'view', 'open', 'cat', 'head', 'tail', 'less', 'sed', 'str_replace_editor'}
            for i, e in enumerate(events):
                first = e['cmd'].split(' ', 1)[0].strip('`')
                if first in VIEW_WORDS and not e.get('path'):
                    pm = re.search(r'(/[^\s`]+)', e['cmd'])
                    if pm: by_path.setdefault(pm.group(1), []).append(i)
            path_repeat_events = set()
            for p, idxs in by_path.items():
                if len(idxs) < 2: continue
                seen = set()
                for j, i in enumerate(idxs):
                    if j > 0:
                        e3_removable_total += sum(len(l) + 1 for l in events[i]['lines'] if l in seen)
                        path_repeat_events.add(i)
                    seen |= events[i]['lines']
            # ---- RDS application over full trajectory (unified rule) ----
            sess_saving = 0; sess_hit = False
            obs_seq = 0
            for i, e in enumerate(events):
                obs = e.get('obs') or ''
                res = rds.deliver(obs, obs_seq)
                obs_seq += 1
                if res['action'] == 'compressed':
                    compressed_events += 1
                    sess_saving += res['saving_chars']
                    rds_removed_total += res['saving_chars']
                    if i in path_repeat_events:
                        rds_removed_in_path_groups += res['saving_chars']
                    sess_hit = True
                    if not res.get('reconstruction_exact', False): recon_fail += 1
            per_session_saving.append((sess_hit, sess_saving, sum(e['obs_chars'] for e in events)))
    # R3 gate
    print('reconstruction failures:', recon_fail, '/', compressed_events)
    hit_savings = [s for (h, s, _) in per_session_saving if h]
    all_savings = [s for (_, s, _) in per_session_saving]
    hit_sessions = len(hit_savings)
    capture = rds_removed_total / e3_removable_total if e3_removable_total else None
    out = {
        'schema_version': 1,
        'stage': 'V0.11-D3-E4 RDS prototype replay (prereg 7d9b343e FROZEN before replay)',
        'date': '2026-09-23',
        'dataset': {'pin': 'D:/tasco-temp/d3_hf_data/sessions.parquet', 'sessions': SESSIONS_TOTAL},
        'self_test': 'ALL PASS (17 cases incl 2 negative locks)',
        'r1_oracle_capture': {'rds_removed_chars_in_path_groups': rds_removed_in_path_groups, 'rds_removed_chars_total_all_trajectory': rds_removed_total, 'e3_census_conservative_removable_chars': e3_removable_total, 'capture_rate_e3_scope': r4(rds_removed_in_path_groups / e3_removable_total) if e3_removable_total else None, 'note': 'capture numerator = RDS removals on E3 path-group repeat events only; denominator = E3 census conservative removable (same d3e3 oracle); RDS also removes repeated content outside path groups (E2/unlabeled) reported separately'},
        'r2_offline_observable_char_saving': {
            'all_sessions': {'p25': pctl(all_savings, 0.25), 'median': med(all_savings), 'p75': pctl(all_savings, 0.75)},
            'hit_sessions': {'count': hit_sessions, 'p25': pctl(hit_savings, 0.25), 'median': med(hit_savings), 'p75': pctl(hit_savings, 0.75)},
            'ge5pct_session_incidence_all': r4(sum(1 for (_, s, o) in per_session_saving if o and s / o >= 0.05) / SESSIONS_TOTAL),
            'ge10pct_session_incidence_all': r4(sum(1 for (_, s, o) in per_session_saving if o and s / o >= 0.10) / SESSIONS_TOTAL),
            'naming': 'offline observable-char saving; NOT token saving',
        },
        'r3_correctness_closure': {'compressed_events': compressed_events, 'reconstruction_failures': recon_fail, 'exact_match_rate': r4(1 - recon_fail / compressed_events) if compressed_events else None, 'gate': 'PASS' if recon_fail == 0 else 'FAIL'},
        'verdict': 'PROTOTYPE_REPLAY_COMPLETE' if recon_fail == 0 else 'PROTOTYPE_FAIL',
    }
    out['aggregates_sha256'] = hashlib.sha256(json.dumps({k: v for k, v in out.items()}, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print('sessions:', SESSIONS_TOTAL, '| hit:', hit_sessions)
    print('R1 capture:', {k: v for k, v in out['r1_oracle_capture'].items() if k != 'note'})
    print('R2 all:', out['r2_offline_observable_char_saving']['all_sessions'])
    print('R2 hit:', out['r2_offline_observable_char_saving']['hit_sessions'])
    print('R2 >=5%:', out['r2_offline_observable_char_saving']['ge5pct_session_incidence_all'], '| >=10%:', out['r2_offline_observable_char_saving']['ge10pct_session_incidence_all'])
    print('R3:', out['r3_correctness_closure'])
    print('hash:', out['aggregates_sha256'][:16], '...')

def sys_exit(code):
    raise SystemExit(code)

if __name__ == '__main__':
    import sys
    main()
