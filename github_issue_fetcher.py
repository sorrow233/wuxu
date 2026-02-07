import requests
import json
import time
import re
import sys
import os

def fetch_data(url, params=None):
    results = []
    page = 1
    per_page = 100
    
    while True:
        current_params = params.copy() if params else {}
        current_params.update({'per_page': per_page, 'page': page})
        
        response = requests.get(url, params=current_params)
        
        if response.status_code != 200:
            print(f"Error fetching {url} page {page}: {response.status_code}")
            if response.status_code == 422: # Common for page limit
                 break
            return results # Return what we have on other errors
            
        data = response.json()
        if not data:
            break
            
        results.extend(data)
        print(f"Fetched {len(results)} items from {url}...")
        
        # Rate limit handling
        remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
        if remaining == 0:
            reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
            sleep_time = max(reset_time - time.time(), 0) + 2
            print(f"Rate limited. Reset at {time.ctime(reset_time)}.")
            if sleep_time > 120: 
                print(f"Wait time too long ({sleep_time:.2f}s). Saving partial results.")
                return results
            print(f"Sleeping for {sleep_time:.2f} seconds...")
            time.sleep(sleep_time)
            
        page += 1
        
    return results

def extract_os(text):
    if not text: return "Unknown"
    match = re.search(r'(?:macOS|MacOS|OS X)\s*(?:version)?\s*(\d+\.\d+(?:\.\d+)?)', text, re.IGNORECASE)
    if match:
        return f"macOS {match.group(1)}"
    if "macOS" in text or "MacOS" in text:
        return "macOS (Version unspecified)"
    return "Unknown"

def analyze_thread(issue, comments):
    body = issue.get('body', '') or ''
    # Extract discussion summary
    if not comments:
        # Check if it was closed with a linked PR in the body
        pr_match = re.search(r'(?:fix|close|resolve)s?\s*#(\d+)', body, re.IGNORECASE)
        if pr_match and issue['state'] == 'closed':
            return "No discussion in issue, but linked to PR #" + pr_match.group(1), f"Fixed in PR #{pr_match.group(1)}"
        return "No discussion (only problem report).", "No fix found in comments."
    
    # 1. Summarize Discussion
    discussion_points = []
    # Keywords indicating a solution or confirmed insight
    insight_keywords = ['try', 'setting', 'model', 'resolution', 'aspect', 'driver', 'metal', 'lock']
    
    for c in comments:
        c_body = c.get('body', '') or ''
        if any(kw in c_body.lower() for kw in insight_keywords):
            line = c_body.split('\n')[0].strip()
            if len(line) > 15:
                discussion_points.append(line)
    
    if not discussion_points:
        for c in comments[:3]:
            line = c.get('body', '').split('\n')[0].strip()
            if len(line) > 10: discussion_points.append(line)

    discussion_summary = " | ".join(discussion_points[:3])
    if not discussion_summary: discussion_summary = "Discussion in progress."

    # 2. Extract Detailed Fix
    fix = "Unknown/Unresolved"
    # Check body for "Edit/Fixed"
    fixed_matches = re.findall(r'(?:edit|fixed|solution|workaround|fix|resolved by):\s*(.*)', body, re.IGNORECASE)
    if fixed_matches:
        fix = fixed_matches[-1].strip()
    else:
        # Search comments for "works", "fixed", "solved", "try this"
        for c in reversed(comments):
            c_body = c.get('body', '') or ''
            # Check for PR links in comments
            pr_match = re.search(r'(?:merged|fixed in)\s*#(\d+)', c_body, re.IGNORECASE)
            if pr_match:
                fix = f"Resolved in PR #{pr_match.group(1)}"
                break
                
            if any(word in c_body.lower() for word in ['works', 'fixed', 'solved', 'fix', 'solution', 'workaround', 'confirmed']):
                # Find the sentence containing the fix
                sentences = re.split(r'[.!?\n]', c_body)
                for s in sentences:
                    if any(w in s.lower() for w in ['works', 'fixed', 'solved', 'try', 'use', 'change', 'model', 'settings']):
                        if len(s.strip()) > 10:
                            fix = s.strip()
                            break
                if fix != "Unknown/Unresolved": break
                fix = c_body[:150].replace('\n', ' ') + "..." # Fallback
                break
                
    if issue['state'] == 'closed' and issue.get('state_reason') == 'completed' and fix == "Unknown/Unresolved":
        fix = "Closed as completed (likely fixed in a specific PR or version)."
        
    return discussion_summary, fix

def extract_game(title):
    # Common games in PlayCover
    games = {
        "Arknights": ["arknights", "明日方舟"],
        "Genshin": ["genshin", "原神"],
        "Honkai Star Rail": ["star rail", "hsr", "崩坏", "星穹铁道"],
        "Zenless Zone Zero": ["zzz", "zenless", "绝区零"],
        "Wuthering Waves": ["wuthering", "waves", "鸣潮"],
        "Nikke": ["nikke", "胜利女神"],
        "Endfield": ["endfield", "终末地"]
    }
    title_low = title.lower()
    for game, keywords in games.items():
        if any(kw in title_low for kw in keywords):
            return game
    return "Other"

def refine_deep(issues, comments_list):
    comment_map = {}
    for comment in comments_list:
        try:
            issue_num = int(comment['issue_url'].split('/')[-1])
            if issue_num not in comment_map:
                comment_map[issue_num] = []
            comment_map[issue_num].append(comment)
        except: continue
        
    refined = []
    for issue in issues:
        if 'pull_request' in issue: continue
        
        num = issue['number']
        title = issue['title']
        body = issue.get('body', '') or ''
        state = issue['state']
        
        game = extract_game(title)
        os_info = extract_os(body)
        relevant_comments = comment_map.get(num, [])
        discussion, fix = analyze_thread(issue, relevant_comments)
        
        refined.append({
            "number": num,
            "problem": title,
            "game": game,
            "os": os_info,
            "status": "Solved" if state == 'closed' and issue.get('state_reason') == 'completed' else "Open",
            "discussion": discussion,
            "fix": fix,
            "url": issue['html_url']
        })
    return refined

def main():
    repo = "PlayCover/PlayCover"
    issues_file = "playcover_issues.json"
    comments_file = "playcover_comments.json"
    
    # Load Issues
    if os.path.exists(issues_file):
        with open(issues_file, 'r') as f: issues = json.load(f)
    else:
        print("Fetching issues...")
        issues = fetch_data(f"https://api.github.com/repos/{repo}/issues", {'state': 'all'})
        with open(issues_file, 'w') as f: json.dump(issues, f, indent=2)

    # Load or Fetch Comments
    if os.path.exists(comments_file):
        print(f"Loading comments from {comments_file}...")
        with open(comments_file, 'r') as f: comments = json.load(f)
    else:
        print("Fetching comments (this may take time)...")
        comments = fetch_data(f"https://api.github.com/repos/{repo}/issues/comments")
        with open(comments_file, 'w') as f: json.dump(comments, f, indent=2)

    print("Analyzing and Refining...")
    deep_data = refine_deep(issues, comments)
    # Sort by Game then number
    deep_data.sort(key=lambda x: (x['game'], x['status'] != 'Solved', -x['number']))

    # Save Results
    with open("playcover_issues_deep.json", 'w') as f:
        json.dump(deep_data, f, ensure_ascii=False, indent=2)

    with open("playcover_issues_report.md", 'w') as f:
        f.write("# PlayCover Issues Deep Report\n\n")
        f.write("## ⚠️ Arknights Custom Analysis (Metal Validation Crash)\n")
        f.write("- **Root Cause**: `MTLTextureDescriptor` validation failure. Likely invalid resolution or incompatible device model.\n")
        f.write("- **Workaround**: Set fixed resolution (e.g. 1080p), disable 'Force aspect ratio', and try 'iPad Pro M2' model.\n\n")
        
        current_game = None
        for item in deep_data:
            if item['game'] != current_game:
                current_game = item['game']
                f.write(f"\n### {current_game} Issues\n")
                f.write("| # | Problem | OS | Status | Discussion | Fix |\n")
                f.write("|---|---|---|---|---|---|\n")
            
            prob = item['problem'].replace('|', '\\|')
            disc = item['discussion'].replace('|', '\\|')
            fix = item['fix'].replace('|', '\\|').replace('\n', ' ')
            f.write(f"| {item['number']} | [{prob}]({item['url']}) | {item['os']} | {item['status']} | {disc} | {fix} |\n")

    print("Done! Reports generated.")

if __name__ == "__main__":
    main()
