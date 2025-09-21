#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将vod.list文件中的站点信息导入到sites_export_2025-09-21.json文件中

功能：
- 解析vod.list文件中的站点名称和URL
- 将解析的数据转换为JSON格式
- 更新sites_export_2025-09-21.json文件

参数：无
返回值：无
异常处理：文件读写异常、JSON解析异常
"""

import json
import re
from datetime import datetime

def parse_vod_list(file_path):
    """
    解析vod.list文件
    
    参数：
    file_path (str): vod.list文件路径
    
    返回值：
    list: 包含站点信息的列表
    
    异常处理：文件不存在、编码错误
    """
    sites = []
    seen_names = set()  # 用于去重的集合，存储已见过的站点名称
    seen_urls = set()   # 用于去重的集合，存储已见过的URL
    site_id = 1         # 站点ID计数器
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            
            # 跳过空行和标题行
            if not line or line == '定制源':
                continue
            
            # 使用正则表达式匹配站点名称和URL，支持空格和冒号分隔符
            match = re.match(r'^(.+?)[:：]\s*(https?://.+)$', line)
            if not match:
                match = re.match(r'^(.+?)\s+(https?://.+)$', line)
            
            if match:
                name = match.group(1).strip()
                url = match.group(2).strip()
                
                # 去重检查：如果站点名称或URL已存在，则跳过
                if name in seen_names:
                    print(f"跳过重复站点名称: {name} (第{line_num}行)")
                    continue
                if url in seen_urls:
                    print(f"跳过重复URL: {url} (第{line_num}行)")
                    continue
                
                # 添加到已见集合
                seen_names.add(name)
                seen_urls.add(url)
                
                # 创建站点对象
                site = {
                    "id": site_id,
                    "key": name.lower().replace(" ", "").replace("资源", "").replace("网", "").replace("采集", "")[:10],
                    "name": name,
                    "api": url,
                    "type": 2,
                    "isActive": 1,
                    "time": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "+08:00",
                    "isDefault": 0,
                    "remark": "",
                    "tags": [],
                    "priority": 0
                }
                sites.append(site)
                site_id += 1
            else:
                print(f"警告: 第{line_num}行格式不正确: {line}")
    
    except FileNotFoundError:
        print(f"错误: 文件 {file_path} 不存在")
        return []
    except UnicodeDecodeError:
        print(f"错误: 文件 {file_path} 编码错误")
        return []
    
    return sites

def update_sites_json(json_path, sites):
    """
    更新sites_export_2025-09-21.json文件
    
    参数：
    json_path (str): JSON文件路径
    sites (list): 站点信息列表
    
    返回值：
    bool: 更新是否成功
    
    异常处理：文件读写异常、JSON格式错误
    """
    try:
        # 读取现有JSON文件
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 更新站点信息
        data['sites'] = sites
        data['total'] = len(sites)
        data['exportTime'] = datetime.now().isoformat() + "Z"
        
        # 写回JSON文件
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return True
    
    except FileNotFoundError:
        print(f"错误: 文件 {json_path} 不存在")
        return False
    except json.JSONDecodeError:
        print(f"错误: 文件 {json_path} JSON格式错误")
        return False
    except Exception as e:
        print(f"错误: 更新文件时发生异常: {e}")
        return False

def main():
    """
    主函数：执行导入操作
    
    参数：无
    返回值：无
    异常处理：捕获所有异常并输出错误信息
    """
    vod_list_path = '/Users/qinxiaoqiang/Downloads/omnibox/vod.list'
    json_path = '/Users/qinxiaoqiang/Downloads/omnibox/sites_export_2025-09-21.json'
    
    try:
        print("开始解析vod.list文件...")
        sites = parse_vod_list(vod_list_path)
        
        if not sites:
            print("没有找到有效的站点信息")
            return
        
        print(f"成功解析 {len(sites)} 个站点")
        
        print("更新JSON文件...")
        if update_sites_json(json_path, sites):
            print(f"成功将 {len(sites)} 个站点导入到 {json_path}")
        else:
            print("更新JSON文件失败")
    
    except Exception as e:
        print(f"程序执行出错: {e}")

if __name__ == '__main__':
    main()