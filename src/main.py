import os
import sys
from dotenv import load_dotenv
from github_api import GitHubAPI
from svg_generator import SVGGenerator

# Load environment variables from .env file
load_dotenv()

def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN environment variable not set.")
        sys.exit(1)

    repo_name = os.environ.get("GITHUB_REPOSITORY")
    if not repo_name:
        print("Error: GITHUB_REPOSITORY environment variable not set.")
        # Fallback for local testing if needed, or just exit
        sys.exit(1)
    
    username = repo_name.split("/")[0]
    print(f"Processing for user: {username}")

    try:
        api = GitHubAPI(token)
        svg_gen = SVGGenerator()

        # Determine assets directory path relative to this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        assets_dir = os.path.join(project_root, "assets")

        if not os.path.exists(assets_dir):
            os.makedirs(assets_dir)

        # 1. Streak Card
        print("Fetching contribution data...")
        calendar_data = api.get_contribution_data(username)
        streak_data = api.calculate_streak(calendar_data)
        total_contributions = calendar_data['totalContributions']
        
        print(f"Streak: {streak_data['currentStreak']}, Longest: {streak_data['longestStreak']}, Total: {total_contributions}")
        streak_svg = svg_gen.generate_streak_svg(streak_data, total_contributions)
        
        with open(os.path.join(assets_dir, "github-streak.svg"), "w", encoding="utf-8") as f:
            f.write(streak_svg)
        print(f"Generated {os.path.join(assets_dir, 'github-streak.svg')}")

        # 2. Top Languages Card
        print("Fetching repository languages...")
        repos = api.get_repository_languages(username)
        top_languages = api.process_languages(repos)
        
        print(f"Top Languages: {[l['name'] for l in top_languages]}")
        lang_svg = svg_gen.generate_languages_svg(top_languages)
        
        with open(os.path.join(assets_dir, "top-languages.svg"), "w", encoding="utf-8") as f:
            f.write(lang_svg)
        print(f"Generated {os.path.join(assets_dir, 'top-languages.svg')}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
