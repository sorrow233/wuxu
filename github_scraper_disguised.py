import requests
from bs4 import BeautifulSoup
import json
import time
import random
import re
import os

# Disguised headers to mimic a real browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Referer': 'https://github.com/PlayCover/PlayCover/issues',
    'DNT': '1',
    'Connection': 'keep-alive'
}

def scrape_issue_details(issue_number):
    url = f"https://github.com/PlayCover/PlayCover/issues/{issue_number}"
    print(f"Scraping {url}...")
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            print(f"Error {response.status_code} for issue {issue_number}")
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. Discussion Summary (First few comments)
        comments = []
        comment_containers = soup.select('.comment-body')
        for idx, container in enumerate(comment_containers):
            text = container.get_text(strip=True)
            if text:
                comments.append(text)
            if len(comments) >= 5: break # Limit discussion depth
            
        discussion = " | ".join([c[:100] + "..." if len(c) > 100 else c for c in comments[:3]])
        
        # 2. Extract Fix
        fix = "Unknown/Unresolved"
        # Heuristic: look for checkboxes or keywords in the last few comments
        for c in reversed(comments):
            low_c = c.lower()
            if any(word in low_c for word in ['works', 'fixed', 'solved', 'solution', 'workaround', 'fix']):
                # Try to extract a specific sentence
                sentences = re.split(r'[.!?\n]', c)
                for s in sentences:
                    if any(w in s.lower() for w in ['works', 'fixed', 'solved', 'try', 'use', 'change']):
                        if len(s.strip()) > 10:
                            fix = s.strip()
                            break
                if fix != "Unknown/Unresolved": break
                fix = c[:200] + "..." if len(c) > 200 else c
                break
        
        # 3. OS info (often in the first comment)
        os_info = "Unknown"
        if comments:
            match = re.search(r'(?:macOS|MacOS|OS X)\s*(?:version)?\s*(\d+\.\d+(?:\.\d+)?)', comments[0], re.IGNORECASE)
            if match:
                os_info = f"macOS {match.group(1)}"
            elif "macOS" in comments[0] or "MacOS" in comments[0]:
                os_info = "macOS (Version unspecified)"

        return {
            "number": issue_number,
            "os": os_info,
            "discussion": discussion or "No comments found.",
            "fix": fix
        }
            
    except Exception as e:
        print(f"Failed to scrape issue {issue_number}: {e}")
        return None

def main():
    issues_file = "playcover_issues.json"
    if not os.path.exists(issues_file):
        print("Error: playcover_issues.json not found.")
        return

    with open(issues_file, 'r') as f:
        issues = json.load(f)

    # Load existing progress if any
    output_file = "playcover_issues_deep.json"
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            deep_data = json.load(f)
    else:
        deep_data = []

    # Target closed issues for solutions, most recent first
    target_issues = [i for i in issues if i.get('state') == 'closed']
    target_issues.sort(key=lambda x: -x['number'])
    
    # For this run, let's just force scrape the top 20 issues to show the user
    # We can expand this later.
    target_issues = target_issues[:20] 
    
    print(f"Total issues to scrape in this batch: {len(target_issues)}")
    
    # Process in batches to show progress
    count = 0
    for issue in target_issues:
        num = issue['number']
        result = scrape_issue_details(num)
        if result:
            deep_data.append({
                "number": num,
                "problem": issue['title'],
                "os": result['os'],
                "status": "Solved" if issue.get('state_reason') == 'completed' else "Closed",
                "discussion": result['discussion'],
                "fix": result['fix'],
                "url": issue['html_url']
            })
            count += 1
            
            # Save every 5 issues
            if count % 5 == 0:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(deep_data, f, ensure_ascii=False, indent=2)
                print(f"Saved progress: {len(deep_data)} issues total.")

        # Randomized delay to mimic human behavior
        time.sleep(random.uniform(1.2, 2.5))
        
        if count >= 30: # Limit one run to 30 issues for now to show user the result
            print("Batch limit reached. Finalizing report...")
            break

    # Save final JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(deep_data, f, ensure_ascii=False, indent=2)

    # Generate Report
    with open("playcover_issues_report.md", 'w', encoding='utf-8') as f:
        f.write("# PlayCover Issues Deep Report\n\n")
        f.write("| # | Problem | OS | Status | Discussion | Fix |\n")
        f.write("|---|---|---|---|---|---|\n")
        # Sort by number descending
        deep_data.sort(key=lambda x: -x['number'])
        for item in deep_data:
            prob = item['problem'].replace('|', '\\|')
            disc = item['discussion'].replace('|', '\\|').replace('\n', ' ')
            fix = item['fix'].replace('|', '\\|').replace('\n', ' ')
            f.write(f"| {item['number']} | [{prob}]({item['url']}) | {item['os']} | {item['status']} | {disc} | {fix} |\n")

    print(f"Done! Scraped {count} new issues.")

if __name__ == "__main__":
    main()
