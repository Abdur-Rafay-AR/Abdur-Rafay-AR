const fs = require('fs');
const path = require('path');
require('dotenv').config();

const TOKEN = process.env.GH_TOKEN || process.env.GITHUB_TOKEN;
const USERNAME = process.env.GH_USERNAME || process.env.GITHUB_REPOSITORY_OWNER || 'Abdur-Rafay-AR';

const GRAPHQL_ENDPOINT = 'https://api.github.com/graphql';

const query = `
  query($username: String!) {
    user(login: $username) {
      contributionsCollection {
        contributionCalendar {
          totalContributions
          weeks {
            contributionDays {
              contributionCount
              date
            }
          }
        }
      }
      repositories(first: 100, ownerAffiliations: OWNER, isFork: false, orderBy: {field: PUSHED_AT, direction: DESC}) {
        nodes {
          name
          languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
            edges {
              size
              node {
                name
                color
              }
            }
          }
        }
      }
    }
  }
`;

async function fetchData() {
    const response = await fetch(GRAPHQL_ENDPOINT, {
        method: 'POST',
        headers: {
            'Authorization': `bearer ${TOKEN}`,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query, variables: { username: USERNAME } }),
    });

    const json = await response.json();
    if (json.errors) {
        console.error('GraphQL Errors:', JSON.stringify(json.errors, null, 2));
        process.exit(1);
    }
    return json.data.user;
}

function calculateLanguages(repositories) {
    const langStats = {};
    let totalSize = 0;

    repositories.nodes.forEach(repo => {
        repo.languages.edges.forEach(edge => {
            const { size, node } = edge;
            const { name, color } = node;
            
            if (!langStats[name]) {
                langStats[name] = { size: 0, color: color || '#ccc' };
            }
            langStats[name].size += size;
            totalSize += size;
        });
    });

    const sortedLangs = Object.entries(langStats)
        .map(([name, data]) => ({ name, ...data, percentage: (data.size / totalSize) * 100 }))
        .sort((a, b) => b.size - a.size)
        .slice(0, 5); // Top 5

    return sortedLangs;
}

function calculateStreak(contributionCalendar) {
    const weeks = contributionCalendar.weeks;
    const days = weeks.flatMap(w => w.contributionDays);
    
    const today = new Date().toISOString().split('T')[0];
    let currentStreak = 0;
    let longestStreak = 0;
    let tempStreak = 0;
    
    // Sort days just in case, though usually sorted
    days.sort((a, b) => new Date(a.date) - new Date(b.date));

    // Check if today has contribution or yesterday (to keep streak alive)
    // We iterate backwards for current streak
    let streakBroken = false;
    for (let i = days.length - 1; i >= 0; i--) {
        const day = days[i];
        if (day.date > today) continue; // Future days

        if (day.contributionCount > 0) {
            if (!streakBroken) currentStreak++;
        } else {
            // If it's today and 0, streak might not be broken if yesterday was active
            if (day.date === today) {
                // do nothing, wait for yesterday
            } else {
                streakBroken = true;
            }
        }
    }

    // Longest streak
    for (const day of days) {
        if (day.contributionCount > 0) {
            tempStreak++;
            if (tempStreak > longestStreak) longestStreak = tempStreak;
        } else {
            tempStreak = 0;
        }
    }

    return {
        totalContributions: contributionCalendar.totalContributions,
        currentStreak,
        longestStreak
    };
}

// Gruvbox Dark palette shared by both cards
const THEME = {
    bg0: '#1d2021',
    bg: '#282828',
    bgSoft: '#32302f',
    fg: '#ebdbb2',
    subtext: '#a89984',
    border: '#3c3836',
    barBg: '#3c3836',
    yellow: '#fabd2f',
    orange: '#fe8019',
    aqua: '#8ec07c',
    red: '#fb4934',
    green: '#b8bb26',
};

// Round to 2 decimals for clean SVG coordinate output
function r(n) {
    return Math.round(n * 100) / 100;
}

// Escape text that is interpolated into SVG markup (language names, etc.)
function esc(str) {
    return String(str).replace(/[&<>"']/g, c => (
        { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
    ));
}

function generateLanguageCard(languages) {
    const width = 340;
    const padding = 22;
    const rowGap = 38;
    const top = 70;
    const height = top + languages.length * rowGap + 10;
    const barWidth = width - padding * 2;

    const rows = languages.map((lang, i) => {
        const y = top + i * rowGap;
        const fill = (lang.color || '#ccc');
        const filled = r(Math.max(2, barWidth * (lang.percentage / 100)));
        const delay = r(0.15 + i * 0.12);
        return `
        <g transform="translate(${padding}, ${y})" class="row" style="animation-delay:${delay}s">
            <circle cx="6" cy="7" r="6" fill="${fill}" />
            <text x="20" y="11" class="lang-name">${esc(lang.name)}</text>
            <text x="${barWidth}" y="11" class="lang-pct" text-anchor="end">${lang.percentage.toFixed(1)}%</text>
            <rect x="0" y="22" width="${barWidth}" height="8" rx="4" fill="${THEME.barBg}" />
            <rect x="0" y="22" width="${filled}" height="8" rx="4" fill="${fill}" class="bar" style="animation-delay:${delay}s" />
        </g>`;
    }).join('');

    return `<svg width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Top languages">
    <defs>
        <linearGradient id="cardGradLang" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="${THEME.bg}"/>
            <stop offset="100%" stop-color="${THEME.bg0}"/>
        </linearGradient>
    </defs>
    <style>
        .card-bg { fill: url(#cardGradLang); stroke: ${THEME.border}; stroke-width: 1.5px; }
        .header { font: 700 19px 'Segoe UI', Ubuntu, Sans-Serif; fill: ${THEME.yellow}; }
        .lang-name { font: 500 13px 'Segoe UI', Ubuntu, Sans-Serif; fill: ${THEME.fg}; }
        .lang-pct { font: 600 12px 'Segoe UI', Ubuntu, Sans-Serif; fill: ${THEME.subtext}; }
        .row { opacity: 0; animation: fadeIn 0.6s ease forwards; }
        .bar { transform: scaleX(0); transform-origin: left; animation: growIn 0.9s cubic-bezier(0.4,0,0.2,1) forwards; }
        @keyframes fadeIn { to { opacity: 1; } }
        @keyframes growIn { to { transform: scaleX(1); } }
    </style>
    <rect x="0.75" y="0.75" rx="12" height="${height - 1.5}" width="${width - 1.5}" class="card-bg"/>
    <text x="${padding}" y="40" class="header">💻 Top Languages</text>
    ${rows}
</svg>`;
}

function generateActivityCard(stats) {
    const width = 480;
    const height = 210;
    const padding = 24;
    const gap = 16;
    const tileW = r((width - padding * 2 - gap * 2) / 3);
    const tileY = 74;
    const tileH = 108;

    const tiles = [
        { icon: '📦', label: 'Total', sub: 'Contributions', value: stats.totalContributions, color: THEME.aqua },
        { icon: '🔥', label: 'Current', sub: 'Streak', value: stats.currentStreak, color: THEME.yellow },
        { icon: '🏆', label: 'Longest', sub: 'Streak', value: stats.longestStreak, color: THEME.red },
    ];

    const tileSvg = tiles.map((t, i) => {
        const x = r(padding + i * (tileW + gap));
        const cx = r(tileW / 2);
        const delay = r(0.15 + i * 0.15);
        return `
        <g transform="translate(${x}, ${tileY})" class="tile" style="animation-delay:${delay}s">
            <rect width="${tileW}" height="${tileH}" rx="8" class="sub-card"/>
            <rect width="${tileW}" height="3" rx="1.5" fill="${t.color}"/>
            <text x="${cx}" y="34" class="stat-label" text-anchor="middle">${t.icon} ${t.label}</text>
            <text x="${cx}" y="52" class="stat-label" text-anchor="middle">${t.sub}</text>
            <text x="${cx}" y="88" class="stat-value" text-anchor="middle" style="fill:${t.color}">${t.value}</text>
        </g>`;
    }).join('');

    return `<svg width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="GitHub activity">
    <defs>
        <linearGradient id="cardGradAct" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="${THEME.bg}"/>
            <stop offset="100%" stop-color="${THEME.bg0}"/>
        </linearGradient>
        <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000000" flood-opacity="0.35"/>
        </filter>
    </defs>
    <style>
        .card-bg { fill: url(#cardGradAct); stroke: ${THEME.border}; stroke-width: 1.5px; }
        .header { font: 700 22px 'Segoe UI', Ubuntu, Sans-Serif; fill: ${THEME.orange}; }
        .stat-label { font: 500 12px 'Segoe UI', Ubuntu, Sans-Serif; fill: ${THEME.subtext}; }
        .stat-value { font: 700 26px 'Segoe UI', Ubuntu, Sans-Serif; }
        .sub-card { fill: ${THEME.bgSoft}; filter: url(#shadow); }
        .tile { opacity: 0; animation: fadeIn 0.6s ease forwards; }
        @keyframes fadeIn { to { opacity: 1; } }
    </style>
    <rect x="0.75" y="0.75" rx="12" height="${height - 1.5}" width="${width - 1.5}" class="card-bg"/>
    <text x="${padding}" y="42" class="header">⚡ GitHub Activity</text>
    ${tileSvg}
</svg>`;
}

async function main() {
    try {
        if (!TOKEN) {
            console.error('Error: GH_TOKEN or GITHUB_TOKEN is required.');
            process.exit(1);
        }
        if (!USERNAME) {
            console.error('Error: GH_USERNAME or GITHUB_REPOSITORY_OWNER is required.');
            process.exit(1);
        }
        console.log(`Fetching data for ${USERNAME}...`);
        const data = await fetchData();
        
        console.log('Calculating stats...');
        const languages = calculateLanguages(data.repositories);
        const activity = calculateStreak(data.contributionsCollection.contributionCalendar);
        
        console.log('Generating SVGs...');
        const langSvg = generateLanguageCard(languages);
        const activitySvg = generateActivityCard(activity);
        
        const outputDir = path.join(__dirname, 'stats');
        if (!fs.existsSync(outputDir)) {
            fs.mkdirSync(outputDir);
        }
        
        fs.writeFileSync(path.join(outputDir, 'top-languages.svg'), langSvg);
        fs.writeFileSync(path.join(outputDir, 'activity.svg'), activitySvg);
        
        console.log('Done! Stats saved to stats/ directory.');
    } catch (error) {
        console.error(error);
        process.exit(1);
    }
}

if (require.main === module) {
    main();
}

module.exports = { generateLanguageCard, generateActivityCard, calculateLanguages, calculateStreak };
