const fs = require('fs');
const path = require('path');
require('dotenv').config();

const TOKEN = process.env.GH_TOKEN || process.env.GITHUB_TOKEN;
const USERNAME = process.env.GH_USERNAME || process.env.GITHUB_REPOSITORY_OWNER || 'Abdur-Rafay-AR';

if (!TOKEN) {
    console.error('Error: GH_TOKEN or GITHUB_TOKEN is required.');
    process.exit(1);
}

if (!USERNAME) {
    console.error('Error: GH_USERNAME or GITHUB_REPOSITORY_OWNER is required.');
    process.exit(1);

}

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

function generateLanguageCard(languages) {
    const width = 300;
    const height = 150 + (languages.length * 25);
    const padding = 20;
    
    // Gruvbox Dark Theme
    const theme = {
        bg: '#282828',
        fg: '#ebdbb2',
        header: '#fabd2f', // Yellow
        subtext: '#a89984',
        border: '#3c3836',
        barBg: '#3c3836'
    };

    let svgContent = `
    <svg width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg">
        <style>
            .header { font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif; fill: ${theme.header}; }
            .lang-name { font: 400 12px 'Segoe UI', Ubuntu, Sans-Serif; fill: ${theme.fg}; }
            .lang-pct { font: 400 12px 'Segoe UI', Ubuntu, Sans-Serif; fill: ${theme.subtext}; }
            .card-bg { fill: ${theme.bg}; stroke: ${theme.border}; stroke-width: 2px; }
        </style>
        <rect x="1" y="1" rx="10" height="${height - 2}" width="${width - 2}" class="card-bg"/>
        <text x="${padding}" y="35" class="header">Top Languages</text>
    `;

    let yOffset = 60;
    languages.forEach(lang => {
        svgContent += `
        <g transform="translate(${padding}, ${yOffset})">
            <circle cx="5" cy="6" r="5" fill="${lang.color}" />
            <text x="15" y="10" class="lang-name">${lang.name}</text>
            <text x="${width - padding * 2 - 10}" y="10" class="lang-pct" text-anchor="end">${lang.percentage.toFixed(1)}%</text>
            <rect x="0" y="20" width="${width - padding * 2}" height="6" rx="3" fill="${theme.barBg}" />
            <rect x="0" y="20" width="${(width - padding * 2) * (lang.percentage / 100)}" height="6" rx="3" fill="${lang.color}" />
        </g>
        `;
        yOffset += 35;
    });

    svgContent += `</svg>`;
    return svgContent;
}

function generateActivityCard(stats) {
    const width = 300;
    const height = 160;
    const padding = 20;

    // Gruvbox Dark Theme
    const theme = {
        bg: '#282828',
        fg: '#ebdbb2',
        header: '#fe8019', // Orange
        label: '#a89984',
        value: '#8ec07c', // Aqua
        border: '#3c3836'
    };

    return `
    <svg width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg">
        <style>
            .header { font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif; fill: ${theme.header}; }
            .stat-label { font: 400 12px 'Segoe UI', Ubuntu, Sans-Serif; fill: ${theme.label}; }
            .stat-value { font: 600 20px 'Segoe UI', Ubuntu, Sans-Serif; fill: ${theme.value}; }
            .card-bg { fill: ${theme.bg}; stroke: ${theme.border}; stroke-width: 2px; }
        </style>
        <rect x="1" y="1" rx="10" height="${height - 2}" width="${width - 2}" class="card-bg"/>
        <text x="${padding}" y="35" class="header">GitHub Activity</text>
        
        <g transform="translate(${padding}, 70)">
            <text x="0" y="0" class="stat-label">Total Contributions</text>
            <text x="0" y="30" class="stat-value">${stats.totalContributions}</text>
        </g>
        
        <g transform="translate(${padding + 110}, 70)">
            <text x="0" y="0" class="stat-label">Current Streak</text>
            <text x="0" y="30" class="stat-value" style="fill: #fabd2f">${stats.currentStreak}</text>
        </g>
        
        <g transform="translate(${padding + 200}, 70)">
            <text x="0" y="0" class="stat-label">Longest Streak</text>
            <text x="0" y="30" class="stat-value" style="fill: #fb4934">${stats.longestStreak}</text>
        </g>
    </svg>
    `;
}

async function main() {
    try {
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

main();
