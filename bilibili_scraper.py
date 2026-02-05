#!/usr/bin/env python3
"""
B站UP主视频网盘链接抓取器 (包含工坊链接解析)
Target UP: 2255628
Start Date: 2024-06-09
"""

import sys
import time
import json
import re
import datetime
import requests
import hashlib
import urllib.parse
from functools import reduce
from typing import List, Dict, Set

# 配置
UP_MID = 2255628
START_DATE_STR = "2024-06-09"
START_TS = int(time.mktime(time.strptime(START_DATE_STR, "%Y-%m-%d")))

# 常见网盘链接正则
CLOUD_PATTERNS = [
    (r'(https?://pan\.baidu\.com/s/[a-zA-Z0-9_-]+)', '百度网盘'),
    (r'(https?://www\.aliyundrive\.com/s/[a-zA-Z0-9]+)', '阿里云盘'),
    (r'(https?://www\.alipan\.com/s/[a-zA-Z0-9]+)', '阿里云盘'),
    (r'(https?://[a-z0-9]+\.lanzou[a-z]?\.com/[a-zA-Z0-9]+)', '蓝奏云'),
    (r'(https?://cloud\.189\.cn/[a-zA-Z0-9/]+)', '天翼云盘'),
    (r'(https?://www\.123pan\.com/s/[a-zA-Z0-9-]+)', '123云盘'),
    (r'(https?://pan\.quark\.cn/s/[a-zA-Z0-9]+)', '夸克网盘'),
]

# 工坊/商品链接正则
WORKSHOP_PATTERNS = [
    r'(https?://gf\.bilibili\.com/item/detail/[0-9]+)',
    r'(https?://mall\.bilibili\.com/[^\s]+)',
]

# 提取码正则
PASSWORD_PATTERNS = [
    r'[提取码|密码|code][：:\s]*([a-zA-Z0-9]{4})'
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://space.bilibili.com/',
}

# Wbi mixin table
mixinKeyEncTab = [
    46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
    33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
    61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
    36, 20, 34, 44, 52
]

def getMixinKey(orig: str):
    'For Wbi signature'
    return reduce(lambda s, i: s + orig[i], mixinKeyEncTab, '')[:32]

def encWbi(params: dict, img_key: str, sub_key: str):
    'Generate Wbi signature'
    mixin_key = getMixinKey(img_key + sub_key)
    curr_time = round(time.time())
    params['wts'] = curr_time
    # sort params
    params = dict(sorted(params.items()))
    # filter invalid chars
    query = urllib.parse.urlencode(params)
    return params, hashlib.md5((query + mixin_key).encode()).hexdigest()

class BilibiliScraper:
    def __init__(self, mid, start_ts):
        self.mid = mid
        self.start_ts = start_ts
        self.output_file = "cursor_links.txt"
        self.processed_bvids = set()
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        
        # Init Wbi keys
        self.img_key, self.sub_key = self.get_wbi_keys()

    def get_wbi_keys(self):
        print("🔑 Getting Wbi keys...")
        try:
            resp = self.session.get("https://api.bilibili.com/x/web-interface/nav", timeout=10)
            data = resp.json()
            wbi_img = data['data']['wbi_img']
            img_url = wbi_img['img_url']
            sub_url = wbi_img['sub_url']
            img_key = img_url.split('/')[-1].split('.')[0]
            sub_key = sub_url.split('/')[-1].split('.')[0]
            return img_key, sub_key
        except Exception as e:
            print(f"⚠️ Failed to get Wbi keys: {e}, using default/empty might fail.")
            return "", ""

    def fetch_video_list(self) -> List[Dict]:
        """获取UP主视频列表，直到指定日期"""
        videos = []
        page = 1
        keep_fetching = True
        
        print(f"🔍 开始获取UP主 {self.mid} 的视频列表...")

        while keep_fetching:
            url = "https://api.bilibili.com/x/space/wbi/arc/search"
            params = {
                'mid': self.mid,
                'ps': 30,
                'tid': 0,
                'pn': page,
                'order': 'pubdate',
                'jsonp': 'jsonp'
            }
            
            # Wbi Sign
            if self.img_key and self.sub_key:
                signed_params, w_rid = encWbi(params, self.img_key, self.sub_key)
                signed_params['w_rid'] = w_rid
                params = signed_params

            try:
                resp = self.session.get(url, params=params, timeout=10)
                data = resp.json()
                
                if data['code'] != 0:
                    print(f"❌ API Error: {data.get('message', 'Unknown')}")
                    # 如果只是第一页就失败，可能是反爬严重
                    break
                    
                vlist = data['data']['list']['vlist']
                if not vlist:
                    break
                
                for v in vlist:
                    created = v['created']
                    if created < self.start_ts:
                        keep_fetching = False
                        continue 
                        
                    videos.append({
                        'bvid': v['bvid'],
                        'title': v['title'],
                        'created': created,
                        'aid': v['aid'] 
                    })
                
                print(f"  已获取第 {page} 页，累计视频: {len(videos)}")
                page += 1
                time.sleep(2) # be nice
                
            except Exception as e:
                print(f"❌ 请求视频列表失败: {e}")
                break
                
        return videos

    def get_video_details(self, bvid: str) -> str:
        """获取视频简介"""
        url = "https://api.bilibili.com/x/web-interface/view"
        params = {'bvid': bvid}
        try:
            resp = requests.get(url, headers=HEADERS, params=params, timeout=10)
            data = resp.json()
            if data['code'] == 0:
                return data['data']['desc']
        except Exception:
            pass
        return ""

    def get_pinned_comment(self, aid: int) -> str:
        """获取置顶评论 (通常包含链接)"""
        url = "https://api.bilibili.com/x/v2/reply/main"
        params = {
            'oid': aid,
            'type': 1, # 1 for video
            'mode': 3  # 0: all, 1: hot, 2: time, 3: hot?
        }
        try:
            resp = requests.get(url, headers=HEADERS, params=params, timeout=10)
            data = resp.json()
            if data['code'] == 0:
                # 检查置顶
                upper = data['data'].get('upper', {})
                if upper and upper.get('top'):
                    content = upper['top'].get('content', {}).get('message', '')
                    return content
                    
                # 同时也检查热评第一条，有时候置顶是第一条热评
                replies = data['data'].get('replies', [])
                if replies:
                    # 简单拼接前3条热评内容，增加命中率
                    comments = [r['content']['message'] for r in replies[:3]]
                    return "\n".join(comments)
        except Exception:
            pass
        return ""

    def resolve_workshop_link(self, url: str) -> str:
        """解析工坊链接，获取内部描述"""
        print(f"    🛠 正在解析工坊链接: {url}")
        try:
            # 工坊详情页通常是 SSR 或者 API 加载
            # 简单尝试 Get 页面提取 JSON 或 直接 regex
            # 这里的 URL 可能是 mall.bilibili.com 或 gf.bilibili.com
            
            # 如果是 mobile Url，尝试转换为 PC 或直接请求
            resp = requests.get(url, headers=HEADERS, timeout=10)
            content = resp.text
            
            # 方法1: 尝试在 HTML 中寻找 window.__INITIAL_STATE__ 或类似数据
            # 方法2: 直接暴力匹配 HTML 中的 http 链接
            # 工坊详情通常在 detail 字段
            
            return content
        except Exception as e:
            print(f"    ❌ 工坊解析失败: {e}")
            return ""

    def extract_links_from_text(self, text: str, source_name: str) -> List[Dict]:
        """从文本提取链接，如果是工坊链接则递归解析"""
        results = []
        
        # 1. 提取网盘链接
        for pattern, type_name in CLOUD_PATTERNS:
            matches = re.finditer(pattern, text)
            for m in matches:
                link = m.group(1)
                # 寻找紧跟的提取码
                ctx_end = min(m.end() + 20, len(text))
                ctx = text[m.end():ctx_end]
                pwd = ""
                for pwd_pat in PASSWORD_PATTERNS:
                    pm = re.search(pwd_pat, ctx)
                    if pm:
                        pwd = pm.group(1)
                        break
                
                results.append({
                    'type': type_name,
                    'url': link,
                    'pwd': pwd,
                    'source': source_name
                })

        # 2. 提取并递归工坊链接
        for pattern in WORKSHOP_PATTERNS:
            matches = re.finditer(pattern, text)
            for m in matches:
                ws_url = m.group(1)
                # 避免死循环？
                ws_content = self.resolve_workshop_link(ws_url)
                if ws_content:
                    # 递归从工坊内容中提取网盘链接
                    sub_links = self.extract_links_from_text(ws_content, f"{source_name} -> 工坊")
                    results.extend(sub_links)
        
        return results

    def run(self):
        videos = self.fetch_video_list()
        print(f"✅ 筛选出 {len(videos)} 个视频 (2024-06-09 至今)")
        
        all_data = []

        for i, v in enumerate(videos):
            print(f"[{i+1}/{len(videos)}] 处理: {v['title']} ({v['bvid']})")
            
            # 1. 获取简介
            desc = self.get_video_details(v['bvid'])
            
            # 2. 获取置顶/热评
            comments = self.get_pinned_comment(v['aid'])
            
            combined_text = f"{desc}\n{comments}"
            
            links = self.extract_links_from_text(combined_text, "直接简介/评论")
            
            # 去重
            unique_links = {}
            for l in links:
                key = l['url']
                if key not in unique_links:
                    unique_links[key] = l
            
            if unique_links:
                print(f"  🎉 发现 {len(unique_links)} 个链接")
                item = {
                    'title': v['title'],
                    'bvid': v['bvid'],
                    'date': time.strftime("%Y-%m-%d", time.localtime(v['created'])),
                    'links': list(unique_links.values())
                }
                all_data.append(item)
            else:
                print("  ⚠️ 未发现链接")
            
            # 避免请求过快
            time.sleep(1.5)

        # 保存结果
        self.save_results(all_data)

    def save_results(self, data):
        output_txt = "bilibili_cursors.txt"
        with open(output_txt, 'w', encoding='utf-8') as f:
            for item in data:
                f.write(f"标题: {item['title']}\n")
                f.write(f"时间: {item['date']}\n")
                f.write(f"视频: https://www.bilibili.com/video/{item['bvid']}\n")
                f.write("链接:\n")
                for l in item['links']:
                    pwd_str = f"  提取码: {l['pwd']}" if l['pwd'] else ""
                    f.write(f"  - [{l['type']}] {l['url']} {pwd_str} (来源: {l['source']})\n")
                f.write("-" * 50 + "\n")
        
        print(f"\n✅ 抓取完成! 结果已保存至 {output_txt}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # 测试模式
        scraper = BilibiliScraper(UP_MID, START_TS)
        print("Test mode...")
    else:
        scraper = BilibiliScraper(UP_MID, START_TS)
        scraper.run()
