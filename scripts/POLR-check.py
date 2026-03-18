#!/usr/bin/env python3
"""
POLR-check.py  —  Provisional Outline Literature Review compliance checker.

POLR principles (from papers/lit-review/POLR.md):
  • Structured skeleton: clear, conceptual headings for each topic
  • Question-focused structure: each section explicitly frames what question it addresses
  • Key findings synthesised (not merely listed author-by-author)
  • Organised for easy restructuring: closing summaries + inter-section transitions
  • Framework-centred: theoretical framework woven through all sections

Scoring (100 pts total):
  Check 1 — Intro roadmap accurately previews all sections            (15 pts)
  Check 2 — Section headings are conceptual and present              (10 pts)
  Check 3 — Each section opens with a purpose/question sentence      (15 pts)
  Check 4 — Each section closes with an "In summary" synthesis       (20 pts)
  Check 5 — Inter-section transitions link consecutive sections      (20 pts)
  Check 6 — Multi-source synthesis (paragraphs cite >=2 sources)      (10 pts)
  Check 7 — Research relevance stated in intro                       (10 pts)

Usage:
  python scripts/POLR-check.py [filepath]
  python scripts/POLR-check.py | grep "compliance"
"""

import re
import sys
import os
import glob

# -- Resolve file(s) ------------------------------------------------------------
if len(sys.argv) > 1:
    files = [sys.argv[1]]
else:
    pattern = os.path.join(os.path.dirname(__file__), '..', 'papers', 'lit-review', '**', '*.md')
    files = [f for f in glob.glob(pattern, recursive=True)
             if not os.path.basename(f).startswith('POLR')]

if not files:
    print("compliance: 0%")
    sys.exit(0)

total_score = 0
total_max   = 0
all_details = []

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    filename = os.path.basename(filepath)
    lines    = content.splitlines()
    lower    = content.lower()

    score   = 0
    details = [f"\n-- {filename} ------------------------------------------"]

    # Split into sections on ## headings
    raw_sections = re.split(r'\n(?=## )', content)
    intro = raw_sections[0] if raw_sections else ''
    sections = {}
    for s in raw_sections[1:]:
        heading_match = re.match(r'## (.+)', s)
        if heading_match:
            key = heading_match.group(1).strip().lower()
            sections[key] = s

    # -- CHECK 1: Intro roadmap accurately previews section topics (15 pts) ------
    # POLR needs the intro to signal what each section covers AND why.
    # We look for: mentions of the actual section heading keywords + a signposting phrase.
    section_keywords = {
        'firm growth':    ['firm growth', 'venture growth', 'growth'],
        'firm survival':  ['firm survival', 'venture survival', 'survival'],
        'mentoring':      ['mentor', 'mentoring', 'mentorship'],
        'social learning':['social learning', 'bandura', 'learning theory'],
    }
    intro_lower = intro.lower()
    intro_hits  = sum(1 for kws in section_keywords.values()
                      if any(kw in intro_lower for kw in kws))
    has_signpost = bool(re.search(
        r'(this chapter|what follows|this review|is organized|is structured|'
        r'first.*then|begins with|followed by|outline)',
        intro_lower))
    c1 = 0
    if intro_hits >= 4 and has_signpost:
        c1 = 15;  details.append("[PASS +15] Intro roadmap: all topics previewed + signposting phrase")
    elif intro_hits >= 3 and has_signpost:
        c1 = 10;  details.append(f"[PARTIAL +10] Intro roadmap: {intro_hits}/4 topics + signposting phrase")
    elif intro_hits >= 3:
        c1 = 7;   details.append(f"[PARTIAL +7] Intro roadmap: {intro_hits}/4 topics mentioned but no signposting")
    elif intro_hits >= 2:
        c1 = 4;   details.append(f"[PARTIAL +4] Intro roadmap: only {intro_hits}/4 topics mentioned")
    else:
        c1 = 0;   details.append(f"[FAIL +0] Intro roadmap: only {intro_hits}/4 topics, no clear signposting")
    score += c1

    # -- CHECK 2: Section headings are conceptual (10 pts) ------------------------
    h2_headings = re.findall(r'^## (.+)', content, re.MULTILINE)
    # Conceptual = not purely generic ("section 1", "introduction", "conclusion")
    generic = re.compile(r'^(section \d+|chapter \d+|introduction|conclusion|references|appendix)$', re.I)
    conceptual = [h for h in h2_headings if not generic.match(h.strip())]
    c2 = 0
    if len(conceptual) >= 4:
        c2 = 10;  details.append(f"[PASS +10] Section headings: {len(conceptual)} conceptual ## headings found")
    elif len(conceptual) >= 2:
        c2 = 5;   details.append(f"[PARTIAL +5] Section headings: only {len(conceptual)} conceptual headings")
    else:
        c2 = 0;   details.append("[FAIL +0] Section headings: fewer than 2 conceptual ## headings")
    score += c2

    # -- CHECK 3: Each section opens with a purpose/question sentence (15 pts) --─
    # POLR: "question-focused subheadings" — first sentence should frame
    # what question/purpose the section addresses, not just state a fact.
    purpose_patterns = re.compile(
        r'(this section|in this section|this paper|this study|this review|'
        r'examines|explores|addresses|investigates|focuses on|'
        r'is central to|is relevant to|is important (for|to)|'
        r'pertains to|the purpose|the aim|in the context of this|'
        r'why do|how do|what (factors|determines|explains|drives)|'
        r'one of the main questions)', re.IGNORECASE)
    section_texts = list(sections.values())
    purpose_passes = 0
    for s in section_texts:
        # Get first 2 sentences of the section body (after heading line)
        body = re.sub(r'^## .+\n', '', s).strip()
        first_two = ' '.join(re.split(r'(?<=[.!?])\s+', body)[:3])
        if purpose_patterns.search(first_two):
            purpose_passes += 1
    pts_per = 15 / max(len(section_texts), 1)
    c3 = round(pts_per * purpose_passes)
    c3 = min(c3, 15)
    if purpose_passes == len(section_texts):
        details.append(f"[PASS +{c3}] Purpose sentences: all {purpose_passes} sections open with purpose/question framing")
    elif purpose_passes > 0:
        details.append(f"[PARTIAL +{c3}] Purpose sentences: {purpose_passes}/{len(section_texts)} sections have purpose framing")
    else:
        details.append("[FAIL +0] Purpose sentences: no sections open with purpose/question framing")
    score += c3

    # -- CHECK 4: Each section closes with an "In summary" synthesis (20 pts) ----
    # POLR: the outline must identify key findings per theme — prose version =
    # each section has an explicit synthesis/summary closing paragraph.
    summary_patterns = re.compile(
        r'(in summary|in conclusion|to summarise|to summarize|'
        r'overall,|taken together|collectively|in short,|'
        r'thus,.*section|this section has|the foregoing)', re.IGNORECASE)
    summary_passes = 0
    for s in section_texts:
        # Check second half of section (summary could be a long paragraph)
        half = len(s) // 2
        tail = s[half:].lower()
        if summary_patterns.search(tail):
            summary_passes += 1
    pts_per = 20 / max(len(section_texts), 1)
    c4 = round(pts_per * summary_passes)
    c4 = min(c4, 20)
    if summary_passes == len(section_texts):
        details.append(f"[PASS +{c4}] Closing synthesis: all {summary_passes} sections have 'In summary' paragraph")
    elif summary_passes > 0:
        details.append(f"[PARTIAL +{c4}] Closing synthesis: {summary_passes}/{len(section_texts)} sections have closing synthesis")
    else:
        details.append("[FAIL +0] Closing synthesis: no sections have a closing synthesis paragraph")
    score += c4

    # -- CHECK 5: Inter-section transitions (20 pts) --------------------------─
    # POLR: easy restructuring requires explicit bridges between sections.
    # We look for transition language at the END of each section OR at the
    # START of the next that explicitly names the previous/next topic.
    transition_patterns = re.compile(
        r'(having (established|examined|reviewed|discussed|outlined|considered)|'
        r'building on (this|these|the above|the foregoing)|'
        r'the (preceding|following|next) section|'
        r'as (established|discussed|noted|shown|demonstrated) (above|earlier|previously)|'
        r'this (relationship|connection|link) (between|with)|'
        r'(turn(ing|s) to|now turn|we now|the focus now|attention now)|'
        r'(the following section|the next section|section \d))', re.IGNORECASE)

    # Also: a paragraph that names TWO section topics (bridging paragraph)
    bridge_pattern = re.compile(
        r'(mentor\w*).{0,150}(surviv\w*|growth\w*)|(surviv\w*|growth\w*).{0,150}(mentor\w*)|'
        r'(social learning|bandura).{0,150}(mentor\w*)|(mentor\w*).{0,150}(social learning|bandura)',
        re.IGNORECASE | re.DOTALL)

    transition_count = 0
    # Check tail of each section and head of next for transition language
    section_list = list(sections.values())
    for i, s in enumerate(section_list):
        tail = s[-600:]
        head = section_list[i+1][:300] if i + 1 < len(section_list) else ''
        combined = tail + ' ' + head
        if transition_patterns.search(combined) or bridge_pattern.search(combined):
            transition_count += 1
    # Also check between intro and first section
    if section_list:
        intro_tail = intro[-400:]
        first_head = section_list[0][:200]
        if transition_patterns.search(intro_tail + first_head):
            transition_count += 1

    max_transitions = len(section_list)  # one per section gap
    pts_per_t = 20 / max(max_transitions, 1)
    c5 = round(pts_per_t * transition_count)
    c5 = min(c5, 20)
    if transition_count >= max_transitions:
        details.append(f"[PASS +{c5}] Transitions: all {transition_count} section-gaps have bridging sentences")
    elif transition_count > 0:
        details.append(f"[PARTIAL +{c5}] Transitions: {transition_count}/{max_transitions} section-gaps bridged")
    else:
        details.append("[FAIL +0] Transitions: no inter-section transition sentences found")
    score += c5

    # -- CHECK 6: Multi-source synthesis paragraphs (10 pts) ------------------
    # POLR: "key findings from critical analysis" — good synthesis cites
    # multiple authors. We measure what % of body paragraphs have >=2 citations.
    citation_pattern = re.compile(r'[A-Z][a-z]+\s+et al\.|[A-Z][a-z]+\s+\(\d{4}\)|\(\w[\w\s,;&]+\d{4}\)')
    body_paragraphs = [p.strip() for p in re.split(r'\n{2,}', content)
                       if len(p.strip()) > 100 and not p.strip().startswith('#')]
    multi_cite = sum(1 for p in body_paragraphs
                     if len(citation_pattern.findall(p)) >= 2)
    ratio = multi_cite / max(len(body_paragraphs), 1)
    if ratio >= 0.6:
        c6 = 10;  details.append(f"[PASS +10] Multi-source synthesis: {multi_cite}/{len(body_paragraphs)} paragraphs cite >=2 sources ({ratio:.0%})")
    elif ratio >= 0.35:
        c6 = 6;   details.append(f"[PARTIAL +6] Multi-source synthesis: {multi_cite}/{len(body_paragraphs)} paragraphs cite >=2 sources ({ratio:.0%})")
    else:
        c6 = 2;   details.append(f"[FAIL +2] Multi-source synthesis: only {multi_cite}/{len(body_paragraphs)} paragraphs cite >=2 sources ({ratio:.0%})")
    score += c6

    # -- CHECK 7: Research relevance stated in intro (10 pts) ----------------─
    # POLR: the outline should make clear WHY these topics matter to the study.
    relevance_patterns = re.compile(
        r'(this study|the present study|the current study|this research|'
        r'the purpose of this (review|study|chapter)|'
        r'in the context of (this|the) (study|research)|'
        r'this (literature review|chapter) (aims|seeks|is intended|serves to)|'
        r'(to address|to investigate|to examine|to explore) (the|this|how|why|what)|'
        r'research (question|gap|problem|objective))', re.IGNORECASE)
    c7 = 0
    if relevance_patterns.search(intro):
        c7 = 10;  details.append("[PASS +10] Research relevance: intro states study purpose/research question")
    else:
        c7 = 0;   details.append("[FAIL +0] Research relevance: intro does not link review to the study's purpose")
    score += c7

    # -- Totals ----------------------------------------------------------------─
    score = min(score, 100)
    all_details.extend(details)
    total_score += score
    total_max   += 100

avg_score = round(total_score / max(len(files), 1))

print(f"\n{'='*55}")
print(f"  POLR Compliance Score: {avg_score}/100")
print(f"  compliance: {avg_score}%")
print(f"{'='*55}")
for d in all_details:
    print(f"  {d}")
print(f"{'='*55}\n")
