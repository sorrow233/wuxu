import requests
import json
import time
import sys

def fetch_issues(repo, state='all'):
    print(f"Fetching {state} issues for {repo}...")
    issues = []
    page = 1
    per_page = 100
    
    while True:
        url = f"https://api.github.com/repos/{repo}/issues"
        params = {
            'state': state,
            'per_page': per_page,
            'page': page,
            'sort': 'created',
            'direction': 'asc'
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            print(f"Error fetching page {page}: {response.status_code}")
            print(response.text)
            break
            
        page_issues = response.json()
        if not page_issues:
            break
            
        # Filter out Pull Requests (GitHub API /issues returns both issues and PRs)
        issues.extend([issue for issue in page_issues if 'pull_request' not in issue])
        
        print(f"Fetched {len(issues)} issues so far (page {page})...")
        
        # Check for rate limiting
        remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
        if remaining == 0:
            reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
            sleep_time = max(reset_time - time.time(), 0) + 1
            print(f"Rate limited. Sleeping for {sleep_time:.2f} seconds...")
            time.sleep(sleep_time)
            
        page += 1
        
    return issues

def main():
    repo = "PlayCover/PlayCover"
    all_issues = fetch_issues(repo)
    
    output_file = "playcover_issues.json"
    print(f"Saving {len(all_issues)} issues to {output_file}...")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_issues, f, ensure_ascii=False, indent=2)
    
    print("Done!")

if __name__ == "__main__":
    main()
