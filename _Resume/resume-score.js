const fs = require('fs');

const resume = fs.readFileSync('resume.md', 'utf-8');
const harvard = fs.readFileSync('harvard_guide.md', 'utf-8');

let score = 0;
const lines = resume.split('\n');

// Check length (1-2 pages ~ 400-800 words)
const wordCount = resume.split(/\s+/).length;
if (wordCount >= 400 && wordCount <= 800) score += 20;

// Check for key sections
const sections = ['experience', 'education', 'skills', 'summary'];
sections.forEach(s => {
    if (resume.toLowerCase().includes(s)) score += 10;
});

// Check for action verbs
const actionVerbs = ['led', 'managed', 'developed', 'designed', 'implemented', 'achieved', 'improved', 'delivered'];
actionVerbs.forEach(v => {
    if (resume.toLowerCase().includes(v)) score += 5;
});

// Check for quantifiable results (numbers/percentages)
const numbers = resume.match(/\d+%|\$\d+|\d+ (people|teams|projects|years)/gi);
if (numbers && numbers.length >= 3) score += 20;

console.log(`SCORE: ${score}`);
process.exit(0);