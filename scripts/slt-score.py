import re
import sys

def score_lit_review(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    sections = re.split(r'\n## ', content)
    full_text = content.lower()
    score = 0
    max_score = 100
    details = []

    # ── 1. SLT introduced before other sections (20pts) ──────────────────
    slt_pos = full_text.find('social learning')
    growth_pos = full_text.find('## firm growth')
    survival_pos = full_text.find('## firm survival')
    mentoring_pos = full_text.find('## mentoring')

    if slt_pos != -1 and slt_pos < growth_pos:
        score += 20
        details.append("[PASS +20] SLT introduced before Firm Growth section")
    elif slt_pos != -1 and slt_pos < mentoring_pos:
        score += 10
        details.append("[PARTIAL +10] SLT introduced before Mentoring but after Firm Growth/Survival")
    else:
        details.append("[FAIL +0] SLT not introduced early — appears only in its own section")

    # ── 2. SLT referenced in intro paragraph (15pts) ─────────────────────
    intro = sections[0].lower() if sections else ''
    if 'social learning' in intro or 'bandura' in intro:
        score += 15
        details.append("[PASS +15] SLT referenced in opening/intro paragraph")
    else:
        details.append("[FAIL +0] SLT not mentioned in intro paragraph")

    # ── 3. SLT linked in Firm Growth section (15pts) ─────────────────────
    growth_section = ''
    for s in sections:
        if s.lower().startswith('firm growth'):
            growth_section = s.lower()
    if 'social learning' in growth_section or 'bandura' in growth_section or 'observational' in growth_section:
        score += 15
        details.append("[PASS +15] SLT explicitly linked in Firm Growth section")
    else:
        details.append("[FAIL +0] SLT not linked in Firm Growth section")

    # ── 4. SLT linked in Firm Survival section (15pts) ───────────────────
    survival_section = ''
    for s in sections:
        if s.lower().startswith('firm survival'):
            survival_section = s.lower()
    if 'social learning' in survival_section or 'bandura' in survival_section or 'observational' in survival_section:
        score += 15
        details.append("[PASS +15] SLT explicitly linked in Firm Survival section")
    else:
        details.append("[FAIL +0] SLT not linked in Firm Survival section")

    # ── 5. SLT linked in Mentoring section (15pts) ───────────────────────
    mentoring_section = ''
    for s in sections:
        if s.lower().startswith('mentoring'):
            mentoring_section = s.lower()
    if 'social learning' in mentoring_section or 'bandura' in mentoring_section:
        score += 15
        details.append("[PASS +15] SLT explicitly linked in Mentoring section")
    else:
        details.append("[FAIL +0] SLT not linked in Mentoring section")

    # ── 6. Transition sentences linking back to SLT (10pts) ──────────────
    slt_transitions = len(re.findall(
        r'(social learning|bandura|observational learning|self.efficacy|role model)',
        full_text
    ))
    if slt_transitions >= 10:
        score += 10
        details.append(f"[PASS +10] Strong SLT threading — {slt_transitions} SLT references across document")
    elif slt_transitions >= 5:
        score += 5
        details.append(f"[PARTIAL +5] Moderate SLT threading — {slt_transitions} SLT references across document")
    else:
        details.append(f"[FAIL +0] Weak SLT threading — only {slt_transitions} SLT references found")

    # ── 7. SLT closing synthesis (10pts) ─────────────────────────────────
    last_500 = full_text[-500:]
    if 'social learning' in last_500 or 'bandura' in last_500:
        score += 10
        details.append("[PASS +10] SLT referenced in closing/synthesis section")
    else:
        details.append("[FAIL +0] SLT not present in closing synthesis")

    # ── Output ────────────────────────────────────────────────────────────
    print(f"\n{'='*55}")
    print(f"  SLT Framework Compliance Score: {score}/{max_score}")
    print(f"  compliance: {score}%")
    print(f"{'='*55}")
    for d in details:
        print(f"  {d}")
    print(f"{'='*55}\n")
    return score

if __name__ == '__main__':
    filepath = sys.argv[1] if len(sys.argv) > 1 else 'papers/lit-review/literature_review.md'
    score_lit_review(filepath)
