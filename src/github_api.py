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
        
        # Sort by date
        days.sort(key=lambda x: x['date'])
        
        today = datetime.now().date()
        valid_days = []
        
        for day in days:
            date_obj = datetime.strptime(day['date'], '%Y-%m-%d').date()
            if date_obj <= today:
                valid_days.append({'date': date_obj, 'count': day['contributionCount']})
        
        valid_days.sort(key=lambda x: x['date'])
        
        # Calculate Longest Streak
        longest_streak = 0
        temp_streak = 0
        for day in valid_days:
            if day['count'] > 0:
                temp_streak += 1
            else:
                if temp_streak > longest_streak:
                    longest_streak = temp_streak
                temp_streak = 0
        # Final check
        if temp_streak > longest_streak:
            longest_streak = temp_streak
            
        # Calculate Current Streak
        current_streak = 0
        if not valid_days:
            return {'currentStreak': 0, 'longestStreak': 0}
            
        last_day = valid_days[-1]
        # If today is the last day in the list
        if last_day['date'] == today:
            if last_day['count'] > 0:
                # Streak is active including today
                for i in range(len(valid_days) - 1, -1, -1):
                    if valid_days[i]['count'] > 0:
                        current_streak += 1
                    else:
                        break
            else:
                # Today is 0, check yesterday
                if len(valid_days) > 1:
                    yesterday = valid_days[-2]
                    if yesterday['count'] > 0:
                        # Streak is active ending yesterday
                        for i in range(len(valid_days) - 2, -1, -1):
                            if valid_days[i]['count'] > 0:
                                current_streak += 1
                            else:
                                break
        
        return {'currentStreak': current_streak, 'longestStreak': longest_streak}

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
