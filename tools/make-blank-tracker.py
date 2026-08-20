#!/usr/bin/env python3
"""Regenerate blank-roadmap.md from roadmap.md.

blank-roadmap.md is the same page with every checkbox cleared — for anyone
who didn't solve these already. Run this after editing roadmap.md:

    python3 tools/make-blank-tracker.py
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(ROOT, 'roadmap.md'), encoding='utf-8').read()

OLD_STATS = re.search(r'^\*\*153 problems.*$', src, re.M)
NEW_STATS = (
    '**0 / 131 core · 0 / 22 stretch · ≈183 h to go** — about 5–6 months at an hour '
    'a day, or 3 at two hours. Slower than the "Blind 75 in 30 days" posts promise; '
    'unlike them, it sticks.\n\n'
    'This is [the roadmap](roadmap.md) with every box cleared — for anyone who isn\'t '
    'the author of this repo. Fork it, work down this page, tick as you go. Every '
    'lesson, walkthrough and solution linked below is the same.'
)

out = src
out = out.replace('# DSA Roadmap\n', '# DSA Roadmap — Blank Tracker\n', 1)
out = out.replace(OLD_STATS.group(0), NEW_STATS, 1)
out = out.replace('[📋 Blank tracker](blank-roadmap.md)', '[🗺 Solved version](roadmap.md)', 1)
out = out.replace(
    '| [📋 Blank tracker](blank-roadmap.md) | This page with every box unticked — start here if the repo isn\'t yours |',
    '| [🗺 Solved version](roadmap.md) | The same page as worked by the repo author, every box ticked |', 1)
out = out.replace('- [x] ', '- [ ] ')
out = out.replace(' · ✅</summary>', '</summary>').replace(' · 7/8 core done</summary>', '</summary>')
out = ('<!-- GENERATED FILE — do not edit by hand.\n'
       '     Regenerate after changing roadmap.md:  python3 tools/make-blank-tracker.py -->\n\n') + out

open(os.path.join(ROOT, 'blank-roadmap.md'), 'w', encoding='utf-8').write(out)
print('blank-roadmap.md regenerated ({} problems, {} ticked)'.format(
    len(re.findall(r"^- \[ \] \*\*[0-9]", out, re.M)), out.count('- [x]')))
