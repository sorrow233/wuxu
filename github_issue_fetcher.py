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
            break
            
        data = response.json()
        if not data:
            break
            
        results.extend(data)
        print(f"Fetched {len(results)} items from {url}...")
        
        # Rate limit handling
        remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
        if remaining == 0:
            reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
            sleep_time = max(reset_time - time.time(), 0) + 1
            print(f"Rate limited. Reset at {time.ctime(reset_time)}.")
            if sleep_time > 60: # If we have to sleep more than a minute, return what we have
                print(f"Sleep time ({sleep_time:.2f}s) too long. Returning partial results.")
                return results
            print(f"Sleeping for {sleep_time:.2f} seconds...")
            time.sleep(sleep_time)
            
        page += 1
        
    return results

def extract_os(text):
    if not text: return "Unknown"
    # Match MacOS/macOS version patterns
    match = re.search(r'(?:macOS|MacOS|OS X)\s*(?:version)?\s*(\d+\.\d+(?:\.\d+)?)', text, re.IGNORECASE)
    if match:
        return f"macOS {match.group(1)}"
    if "macOS" in text or "MacOS" in text:
        return "macOS (Version unspecified)"
    return "Unknown"

def extract_solution(issue, comments):
    # Check issue body for "Edit" or "Fixed" sections
    body = issue.get('body', '') or ''
    fixed_matches = re.findall(r'(?:edit|fixed|solution|workaround):\s*(.*)', body, re.IGNORECASE)
    if fixed_matches:
        return fixed_matches[-1].strip()
    
    # Check comments for potential solutions (last few comments often have it)
    if not comments:
        return "No solution found in comments."
    
    # Heuristic: look for comments with positive reactions or keywords
    for comment in reversed(comments):
        c_body = comment.get('body', '') or ''
        if any(word in c_body.lower() for word in ['works', 'fixed', 'solved', 'solution', 'workaround', 'helped']):
            # Return a cleaned snippet
            snippet = c_body.split('\n')[0]
            if len(snippet) < 10 and len(c_body) > 10:
                snippet = c_body[:100] + "..."
            return snippet.strip()
            
    return "Issue may still be unresolved or solution is in discussion."

def refine_issues(issues, comments_list):
    # Map comments to issues
    comment_map = {}
    for comment in comments_list:
        # issue_url looks like: https://api.github.com/repos/PlayCover/PlayCover/issues/123
        issue_num = int(comment['issue_url'].split('/')[-1])
        if issue_num not in comment_map:
            comment_map[issue_num] = []
        comment_map[issue_num].append(comment)
        
    refined = []
    for issue in issues:
        if 'pull_request' in issue: continue
        
        num = issue['number']
        title = issue['title']
        body = issue.get('body', '') or ''
        state = issue['state']
        state_reason = issue.get('state_reason')
        
        os_info = extract_os(body)
        relevant_comments = comment_map.get(num, [])
        solution = extract_solution(issue, relevant_comments)
        
        status = "Solved" if state == 'closed' and state_reason == 'completed' else "Open/Unresolved"
        if state == 'closed' and state_reason != 'completed':
            status = "Closed (Not necessarily solved)"

        refined.append({
            "number": num,
            "problem": title,
            "os": os_info,
            "status": status,
            "solution": solution,
            "url": issue['html_url']
        })
    return refined

def main():
    issues_file = "playcover_issues.json"
    
    if not os.path.exists(issues_file):
        print(f"Error: {issues_file} not found. Please run the script without refinement first.")
        return

    print(f"Loading issues from {issues_file}...")
    with open(issues_file, 'r', encoding='utf-8') as f:
        issues = json.load(f)
    
    print("Refining issue data (using local data only)...")
    refined_data = []
    
    for issue in issues:
        if 'pull_request' in issue: continue
        
        num = issue['number']
        title = issue['title']
        body = issue.get('body', '') or ''
        state = issue['state']
        state_reason = issue.get('state_reason')
        
        os_info = extract_os(body)
        
        # In local-only mode, we can only look at the body for solutions
        solution = "Look in comments for details."
        fixed_matches = re.findall(r'(?:edit|fixed|solution|workaround|fix):\s*(.*)', body, re.IGNORECASE)
        if fixed_matches:
            solution = fixed_matches[-1].strip()
        elif state == 'closed' and state_reason == 'completed':
            solution = "Issue closed as completed (check comments for fix)."
        
        status = "Solved" if state == 'closed' and state_reason == 'completed' else "Open/Unresolved"
        if state == 'closed' and state_reason != 'completed':
            status = "Closed (Not solved/Duplicate/Invalid)"

        refined_data.append({
            "number": num,
            "problem": title,
            "os": os_info,
            "status": status,
            "solution": solution,
            "url": issue['html_url']
        })
    
    # Sort: solved first, then by number descending
    refined_data.sort(key=lambda x: (x['status'] != 'Solved', -x['number']))
    
    # Save JSON
    with open("playcover_issues_refined.json", 'w', encoding='utf-8') as f:
        json.dump(refined_data, f, ensure_ascii=False, indent=2)
        
    # Generate Markdown Summary
    with open("playcover_issues_summary.md", 'w', encoding='utf-8') as f:
        f.write(f"# PlayCover Issues Summary\n\n")
        f.write(f"Total: {len(refined_data)} | Solved: {len([i for i in refined_data if i['status'] == 'Solved'])}\n\n")
        f.write("| # | Problem | OS | Status | Solution |\n")
        f.write("|---|---|---|---|---|\n")
        
        for item in refined_data[:200]: # Show more in summary now that it's faster
            sol = item['solution'].replace('|', '\\|').replace('\n', ' ')
            if len(sol) > 100: sol = sol[:97] + "..."
            prob = item['problem'].replace('|', '\\|')
            f.write(f"| {item['number']} | [{prob}]({item['url']}) | {item['os']} | {item['status']} | {sol} |\n")
            
    print("Done! Simplified refinement complete.")

if __name__ == "__main__":
    main()
