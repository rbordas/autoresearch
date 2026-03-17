#!/usr/bin/env python3
"""
resume-score.py
Scores resume.md against Harvard style guide criteria.
Outputs a single integer 0-100 to stdout.
Set VERBOSE=1 for breakdown.
"""

import re
import os
import sys

resume_path = os.path.join(os.path.dirname(__file__), '..', 'resume.md')

if not os.path.exists(resume_path):
    print(0)
    sys.exit(0)

with open(resume_path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()
lower = content.lower()

score = 0
breakdown = []

# ─── 1. CONTACT INFORMATION (15 pts) ──────────────────────────────────────────
has_email    = bool(re.search(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}', content))
has_phone    = bool(re.search(r'\(?\d{3}\)?[\s.\-]?\d{3}[\s.\-]?\d{4}', content))
has_linkedin = bool(re.search(r'linkedin\.com/in/', content, re.IGNORECASE))
first_nonempty = next((l for l in lines if l.strip()), '')
has_name     = bool(re.match(r'^#{1,3}\s+\S', first_nonempty)) or bool(re.match(r'^\*\*\S', first_nonempty))

if has_name:     score += 3;  breakdown.append('+3  name at top')
if has_email:    score += 5;  breakdown.append('+5  email present')
if has_phone:    score += 4;  breakdown.append('+4  phone present')
if has_linkedin: score += 3;  breakdown.append('+3  LinkedIn present')

# ─── 2. REQUIRED SECTIONS (20 pts) ────────────────────────────────────────────
has_summary    = bool(re.search(r'summary|qualifications|objective|profile', content, re.IGNORECASE))
has_experience = bool(re.search(r'experience|work history|employment', content, re.IGNORECASE))
has_education  = bool(re.search(r'\beducation\b', content, re.IGNORECASE))
has_skills     = bool(re.search(r'\bskills?\b|competencies|technical', content, re.IGNORECASE))
has_volunteer  = bool(re.search(r'volunteer|community service|mentoring', content, re.IGNORECASE))
has_certif     = bool(re.search(r'certif|training|credential', content, re.IGNORECASE))

if has_summary:    score += 6;  breakdown.append('+6  summary/qualifications section')
if has_experience: score += 5;  breakdown.append('+5  experience section')
if has_education:  score += 4;  breakdown.append('+4  education section')
if has_skills:     score += 2;  breakdown.append('+2  skills section')
if has_volunteer:  score += 2;  breakdown.append('+2  volunteer section')
if has_certif:     score += 1;  breakdown.append('+1  certifications section')

# ─── 3. ACTION VERBS (15 pts) ─────────────────────────────────────────────────
ACTION_VERBS = {
    'accomplished','achieved','administered','analyzed','arranged','assembled','assessed',
    'assisted','attained','authored','built','chaired','clarified','coached','collaborated',
    'compiled','completed','conducted','consolidated','contributed','coordinated','created',
    'defined','delivered','demonstrated','designed','developed','directed','drove','earned',
    'eliminated','enabled','established','evaluated','executed','expanded','expedited',
    'facilitated','generated','guided','headed','implemented','improved','increased',
    'initiated','installed','instructed','integrated','introduced','launched','led',
    'liaised','managed','mentored','modeled','monitored','negotiated','orchestrated',
    'organized','oversaw','performed','planned','prepared','presented','produced',
    'programmed','provided','published','recruited','redesigned','reduced','reinforced',
    'reorganized','researched','reviewed','revised','scheduled','simplified','spearheaded',
    'standardized','streamlined','strengthened','structured','supervised','supported',
    'surpassed','systematized','taught','trained','transitioned','unified','upgraded',
    'utilized','validated','verified','wrote'
}

bullet_lines = [l for l in lines if re.match(r'^\s*[-•]\s+', l)]
verb_count = 0
for bl in bullet_lines:
    text = re.sub(r'^\s*[-•]\s*', '', bl).lower()
    first_word = re.sub(r'[^a-z]', '', text.split()[0]) if text.split() else ''
    if any(first_word == v or first_word.startswith(v) for v in ACTION_VERBS):
        verb_count += 1

if bullet_lines:
    ratio = verb_count / len(bullet_lines)
    verb_score = round(ratio * 15)
    score += verb_score
    breakdown.append(f'+{verb_score} action verbs ({verb_count}/{len(bullet_lines)} bullets start with action verb)')

# ─── 4. QUANTIFIED ACHIEVEMENTS (15 pts) ──────────────────────────────────────
quant_pat = re.compile(
    r'\d+\s*%|\$[\d,]+|\d+\s*(employees?|people|managers?|countries|years?|months?|team|FTEs?|accounts?|clients?|million|billion|thousand|regions?|installations?|projects?|courses?|students?|groups?)',
    re.IGNORECASE
)
quant_count = sum(1 for bl in bullet_lines if quant_pat.search(bl))
quant_score = min(15, quant_count * 2)
score += quant_score
breakdown.append(f'+{quant_score} quantified achievements ({quant_count} bullets with numbers/metrics)')

# ─── 5. NO PERSONAL PRONOUNS (10 pts) ─────────────────────────────────────────
pronoun_matches = len(re.findall(r'\b(I|me|my|mine|we|our|ours|myself)\b', content))
pronoun_penalty = min(10, pronoun_matches * 2)
pronoun_score   = 10 - pronoun_penalty
score += pronoun_score
breakdown.append(f'+{pronoun_score} no personal pronouns (found {pronoun_matches})')

# ─── 6. CONTENT COMPLETENESS — industry + academic merge (15 pts) ────────────
has_phd        = bool(re.search(r'ph\.?\s*d\.?|doctoral|dissertation|candidat', content, re.IGNORECASE))
has_oracle     = bool(re.search(r'oracle', content, re.IGNORECASE))
has_research   = bool(re.search(r'research|stata|spss|\bR\b|statistical analysis', content, re.IGNORECASE))
has_teaching   = bool(re.search(r'teach|train|instruct|seminar|workshop|coach', content, re.IGNORECASE))
has_tech       = bool(re.search(r'python|sql|mysql|oracle\s+db|iot|mqtt|raspberry', content, re.IGNORECASE))
has_dates      = bool(re.search(r'\d{4}\s*[–\-]\s*(present|\d{4})', content, re.IGNORECASE))

if has_phd:      score += 3;  breakdown.append('+3  PhD/academic credentials included')
if has_oracle:   score += 3;  breakdown.append('+3  Oracle industry experience included')
if has_research: score += 2;  breakdown.append('+2  research/analytical skills included')
if has_teaching: score += 2;  breakdown.append('+2  teaching/training experience included')
if has_tech:     score += 3;  breakdown.append('+3  technical skills included')
if has_dates:    score += 2;  breakdown.append('+2  consistent date ranges present')

# ─── 7. HARVARD FORMATTING (10 pts) ──────────────────────────────────────────
has_bold_headers = bool(re.search(r'^#{1,3}\s+[A-Z]{3,}', content, re.MULTILINE)) or \
                   bool(re.search(r'\*\*[A-Z]{3,}', content))
has_italic_titles = bool(re.search(r'_[\w\s,–\-]+_', content)) or \
                    bool(re.search(r'\*[\w\s,–\-]+\*', content))
no_excess_blanks  = len(re.findall(r'\n{4,}', content)) == 0

# Reverse-chron: Oracle (2017-Present) before Marriott (1998-2000)
oracle_idx   = lower.find('oracle')
marriott_idx = lower.find('marriott')
reverse_chron = oracle_idx != -1 and marriott_idx != -1 and oracle_idx < marriott_idx

if has_bold_headers:   score += 3;  breakdown.append('+3  formatted section headers')
if has_italic_titles:  score += 3;  breakdown.append('+3  italic job titles')
if no_excess_blanks:   score += 2;  breakdown.append('+2  clean spacing')
if reverse_chron:      score += 2;  breakdown.append('+2  reverse-chronological order')

# ─── CAP & OUTPUT ─────────────────────────────────────────────────────────────
score = min(100, score)
print(score)

if os.environ.get('VERBOSE'):
    sys.stderr.write('\n=== Resume Score Breakdown ===\n')
    for b in breakdown:
        sys.stderr.write('  ' + b + '\n')
    sys.stderr.write(f'\nFINAL SCORE: {score}/100\n')
