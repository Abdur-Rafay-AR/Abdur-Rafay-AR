import requests
import os
from datetime import datetime, timedelta

class GitHubAPI:
    def __init__(self, token):
        self.token = token
        self.headers = {"Authorization": f"Bearer {token}"}
        self.api_url = "https://api.github.com/graphql"

    def run_query(self, query, variables):
        request = requests.post(self.api_url, json={'query': query, 'variables': variables}, headers=self.headers)
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception(f"Query failed to run by returning code of {request.status_code}. {query}")

    def get_contribution_data(self, username):
        query = """
        query($userName:String!) {
          user(login: $userName) {
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
          }
        }
        """
        variables = {"userName": username}
        result = self.run_query(query, variables)
        return result['data']['user']['contributionsCollection']['contributionCalendar']

    def get_repository_languages(self, username):
        query = """
        query($userName:String!) {
          user(login: $userName) {
            repositories(ownerAffiliations: OWNER, isFork: false, first: 100, orderBy: {field: PUSHED_AT, direction: DESC}) {
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
        """
        variables = {"userName": username}
        result = self.run_query(query, variables)
        return result['data']['user']['repositories']['nodes']

    def calculate_streak(self, calendar_data):
        # Flatten the weeks into a list of days
        days = []
        for week in calendar_data['weeks']:
            days.extend(week['contributionDays'])
        
        # Sort by date just in case
        days.sort(key=lambda x: x['date'])
        
        current_streak = 0
        longest_streak = 0
        
        # Iterate backwards from today
        today = datetime.now().date()
        
        # Check if we have data for today, if not, maybe timezone issue, but let's look at the last available day
        # The API returns data up to today usually.
        
        # Convert string dates to objects
        for day in days:
            day['date_obj'] = datetime.strptime(day['date'], '%Y-%m-%d').date()

        # Filter out future days (if any)
        days = [d for d in days if d['date_obj'] <= today]
        
        # Reverse to count backwards
        days_reversed = sorted(days, key=lambda x: x['date_obj'], reverse=True)
        
        streak = 0
        # Check if today has contributions
        if days_reversed and days_reversed[0]['date_obj'] == today:
            if days_reversed[0]['contributionCount'] > 0:
                streak = 1
            else:
                # If no contribution today, check yesterday. If yesterday has contribution, streak is still active (just not incremented for today yet)
                # But usually "current streak" implies consecutive days ending today or yesterday.
                pass
        
        # Actually, a simpler logic for "Current Streak":
        # Count backwards. If a day has 0 contributions, stop.
        # Exception: If today has 0, but yesterday had > 0, the streak is still alive (it's just 0 for today so far).
        
        temp_streak = 0
        streak_active = True
        
        # Find the index of today or yesterday
        start_index = 0
        if days_reversed[0]['date_obj'] == today:
            if days_reversed[0]['contributionCount'] == 0:
                # If today is 0, we start counting from yesterday
                start_index = 1
                # If yesterday was also 0, streak is broken/0.
                if len(days_reversed) > 1 and days_reversed[1]['contributionCount'] == 0:
                    streak_active = False
            else:
                # Today has contributions
                pass
        
        if streak_active:
            for i in range(start_index, len(days_reversed)):
                if days_reversed[i]['contributionCount'] > 0:
                    temp_streak += 1
                else:
                    break
        
        return temp_streak

    def process_languages(self, repos):
        lang_stats = {}
        total_size = 0
        
        for repo in repos:
            if repo['languages']['edges']:
                for edge in repo['languages']['edges']:
                    lang_name = edge['node']['name']
                    size = edge['size']
                    color = edge['node']['color']
                    
                    if lang_name not in lang_stats:
                        lang_stats[lang_name] = {'size': 0, 'color': color}
                    
                    lang_stats[lang_name]['size'] += size
                    total_size += size
        
        # Calculate percentages and sort
        result = []
        for lang, data in lang_stats.items():
            percentage = (data['size'] / total_size) * 100
            result.append({
                'name': lang,
                'percentage': percentage,
                'color': data['color'],
                'size': data['size']
            })
            
        result.sort(key=lambda x: x['size'], reverse=True)
        return result[:5] # Top 5
