#!/usr/bin/env node
/**
 * resume-score.js
 * Scores resume.md against Harvard style guide criteria.
 * Outputs a single integer 0-100 to stdout.
 * Set VERBOSE=1 for breakdown.
 */

const fs = require('fs');
const path = require('path');

const resumePath = path.join(__dirname, '..', 'resume.md');

if (!fs.existsSync(resumePath)) {
  console.log(0);
  process.exit(0);
}

const content = fs.readFileSync(resumePath, 'utf-8');
const lines = content.split('\n');
const lower = content.toLowerCase();

let score = 0;
const breakdown = [];

// ─── 1. CONTACT INFORMATION (15 pts) ──────────────────────────────────────────
const hasEmail = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/.test(content);
const hasPhone = /\(?\d{3}\)?[\s.\-]?\d{3}[\s.\-]?\d{4}/.test(content);
const hasLinkedIn = /linkedin\.com\/in\//i.test(content);
// Name = first non-empty line is bold or H1/H2
const firstNonEmpty = lines.find(l => l.trim().length > 0) || '';
const hasName = /^#{1,3}\s+\S/.test(firstNonEmpty) || /^\*\*\S/.test(firstNonEmpty);

if (hasName)    { score += 3;  breakdown.push('+3  name at top'); }
if (hasEmail)   { score += 5;  breakdown.push('+5  email present'); }
if (hasPhone)   { score += 4;  breakdown.push('+4  phone present'); }
if (hasLinkedIn){ score += 3;  breakdown.push('+3  LinkedIn present'); }

// ─── 2. REQUIRED SECTIONS (20 pts) ────────────────────────────────────────────
const hasSummary      = /summary|qualifications|objective|profile/i.test(content);
const hasExperience   = /experience|work history|employment/i.test(content);
const hasEducation    = /\beducation\b/i.test(content);
const hasSkills       = /\bskills?\b|competencies|technical/i.test(content);
const hasVolunteer    = /volunteer|community service|mentoring/i.test(content);
const hasCertif       = /certif|training|credential/i.test(content);

if (hasSummary)    { score += 6;  breakdown.push('+6  summary/qualifications section'); }
if (hasExperience) { score += 5;  breakdown.push('+5  experience section'); }
if (hasEducation)  { score += 4;  breakdown.push('+4  education section'); }
if (hasSkills)     { score += 2;  breakdown.push('+2  skills section'); }
if (hasVolunteer)  { score += 2;  breakdown.push('+2  volunteer section'); }
if (hasCertif)     { score += 1;  breakdown.push('+1  certifications section'); }

// ─── 3. ACTION VERBS (15 pts) ─────────────────────────────────────────────────
const ACTION_VERBS = [
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
];

const bulletLines = lines.filter(l => /^\s*[-•]\s+/.test(l));
const verbCount = bulletLines.filter(l => {
  const text = l.trim().replace(/^[-•]\s*/, '').toLowerCase();
  const firstWord = text.split(/\s+/)[0].replace(/[^a-z]/g, '');
  return ACTION_VERBS.some(v => firstWord === v || firstWord.startsWith(v));
}).length;

if (bulletLines.length > 0) {
  const ratio = verbCount / bulletLines.length;
  const verbScore = Math.round(ratio * 15);
  score += verbScore;
  breakdown.push(`+${verbScore} action verbs (${verbCount}/${bulletLines.length} bullets start with action verb)`);
}

// ─── 4. QUANTIFIED ACHIEVEMENTS (15 pts) ──────────────────────────────────────
const quantPattern = /\d+\s*%|\$[\d,]+|\d+\s*(employees?|people|managers?|countries|years?|months?|team|FTEs?|accounts?|clients?|million|billion|thousand|regions?|installations?|projects?|courses?|students?|groups?)/i;
const quantCount = bulletLines.filter(l => quantPattern.test(l)).length;
const quantScore = Math.min(15, quantCount * 2);
score += quantScore;
breakdown.push(`+${quantScore} quantified achievements (${quantCount} bullets with numbers/metrics)`);

// ─── 5. NO PERSONAL PRONOUNS (10 pts) ─────────────────────────────────────────
const pronounMatches = (content.match(/\b(I|me|my|mine|we|our|ours|myself)\b/g) || []).length;
const pronounPenalty = Math.min(10, pronounMatches * 2);
const pronounScore = 10 - pronounPenalty;
score += pronounScore;
breakdown.push(`+${pronounScore} no personal pronouns (found ${pronounMatches})`);

// ─── 6. CONTENT COMPLETENESS — industry + academic merge (15 pts) ────────────
const hasPhD        = /ph\.?\s*d\.?|doctoral|dissertation|candidat/i.test(content);
const hasOracleExp  = /oracle/i.test(content);
const hasResearch   = /research|stata|spss|\bR\b|statistical analysis/i.test(content);
const hasTeaching   = /teach|train|instruct|seminar|workshop|coach/i.test(content);
const hasTechSkills = /python|sql|mysql|oracle\s+db|iot|mqtt|raspberry/i.test(content);
const hasDateConsist= /\d{4}\s*[–\-]\s*(present|\d{4})/i.test(content);

if (hasPhD)        { score += 3; breakdown.push('+3  PhD/academic credentials included'); }
if (hasOracleExp)  { score += 3; breakdown.push('+3  Oracle industry experience included'); }
if (hasResearch)   { score += 2; breakdown.push('+2  research/analytical skills included'); }
if (hasTeaching)   { score += 2; breakdown.push('+2  teaching/training experience included'); }
if (hasTechSkills) { score += 3; breakdown.push('+3  technical skills included'); }
if (hasDateConsist){ score += 2; breakdown.push('+2  consistent date ranges present'); }

// ─── 7. HARVARD FORMATTING (10 pts) ──────────────────────────────────────────
const hasBoldHeaders    = /^#{1,3}\s+[A-Z]{3,}/m.test(content) || /\*\*[A-Z]{3,}/.test(content);
const hasItalicTitles   = /_([\w\s,–\-]+)_/.test(content) || /\*([\w\s,–\-]+)\*/.test(content);
const noExcessiveBlanks = (content.match(/\n{4,}/g) || []).length === 0;
// Reverse-chron check: Oracle (2017-Present) appears before earlier jobs in Experience
const oracleIdx = lower.indexOf('oracle');
const marriottIdx = lower.indexOf('marriott');
const reverseChron = oracleIdx !== -1 && marriottIdx !== -1 && oracleIdx < marriottIdx;

if (hasBoldHeaders)    { score += 3; breakdown.push('+3  formatted section headers (bold/heading)'); }
if (hasItalicTitles)   { score += 3; breakdown.push('+3  italic job titles'); }
if (noExcessiveBlanks) { score += 2; breakdown.push('+2  clean spacing (no 4+ consecutive blank lines)'); }
if (reverseChron)      { score += 2; breakdown.push('+2  reverse-chronological order'); }

// ─── CAP & OUTPUT ─────────────────────────────────────────────────────────────
score = Math.min(100, score);
console.log(score);

if (process.env.VERBOSE) {
  process.stderr.write('\n=== Resume Score Breakdown ===\n');
  breakdown.forEach(b => process.stderr.write('  ' + b + '\n'));
  process.stderr.write(`\nFINAL SCORE: ${score}/100\n`);
}
