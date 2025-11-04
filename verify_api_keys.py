#!/usr/bin/env python3
"""
API密钥验证脚本
验证Google API Key, DeepSeek API Key, Finnhub API Key的有效性
"""

import requests
import json
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def verify_google_api():
    """验证Google API Key"""
    api_key = os.getenv('GOOGLE_API_KEY')
    print(f"🔍 验证 Google API Key: {api_key[:20]}...")
    
    if not api_key:
        print("❌ Google API Key 未设置")
        return False
    
    try:
        # 使用Google Generative AI API测试
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Google API Key 有效 - 找到 {len(models)} 个模型")
            return True
        elif response.status_code == 400:
            print(f"❌ Google API Key 无效: API密钥格式错误")
        elif response.status_code == 403:
            print(f"❌ Google API Key 无效: 权限被拒绝或密钥已禁用")
        else:
            print(f"❌ Google API Key 验证失败: HTTP {response.status_code}")
        return False
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Google API 网络请求失败: {e}")
        return False
    except Exception as e:
        print(f"❌ Google API Key 验证异常: {e}")
        return False

def verify_deepseek_api():
    """验证DeepSeek API Key"""
    api_key = os.getenv('DEEPSEEK_API_KEY')
    print(f"🔍 验证 DeepSeek API Key: {api_key[:20]}...")
    
    if not api_key:
        print("❌ DeepSeek API Key 未设置")
        return False
    
    try:
        # 使用DeepSeek API测试
        url = "https://api.deepseek.com/v1/models"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            models = response.json().get('data', [])
            print(f"✅ DeepSeek API Key 有效 - 找到 {len(models)} 个模型")
            return True
        elif response.status_code == 401:
            print(f"❌ DeepSeek API Key 无效: 认证失败")
        elif response.status_code == 403:
            print(f"❌ DeepSeek API Key 无效: 权限被拒绝")
        else:
            print(f"❌ DeepSeek API Key 验证失败: HTTP {response.status_code}")
            print(f"响应内容: {response.text[:200]}")
        return False
        
    except requests.exceptions.RequestException as e:
        print(f"❌ DeepSeek API 网络请求失败: {e}")
        return False
    except Exception as e:
        print(f"❌ DeepSeek API Key 验证异常: {e}")
        return False

def verify_finnhub_api():
    """验证Finnhub API Key"""
    api_key = os.getenv('FINNHUB_API_KEY')
    print(f"🔍 验证 Finnhub API Key: {api_key[:20]}...")
    
    if not api_key:
        print("❌ Finnhub API Key 未设置")
        return False
    
    try:
        # 使用Finnhub API测试 - 获取股票基本信息
        url = f"https://finnhub.io/api/v1/quote?symbol=AAPL&token={api_key}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'c' in data:  # 'c' 是当前价格字段
                print(f"✅ Finnhub API Key 有效 - AAPL当前价格: ${data['c']}")
                return True
            else:
                print(f"❌ Finnhub API 响应异常: {data}")
        elif response.status_code == 401:
            print(f"❌ Finnhub API Key 无效: 认证失败")
        elif response.status_code == 403:
            print(f"❌ Finnhub API Key 无效: 权限被拒绝或超出配额")
        else:
            print(f"❌ Finnhub API Key 验证失败: HTTP {response.status_code}")
            print(f"响应内容: {response.text[:200]}")
        return False
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Finnhub API 网络请求失败: {e}")
        return False
    except Exception as e:
        print(f"❌ Finnhub API Key 验证异常: {e}")
        return False

def main():
    print("=" * 60)
    print("🔐 API密钥验证工具")
    print("=" * 60)
    
    results = {}
    
    # 验证各个API密钥
    results['Google'] = verify_google_api()
    print()
    
    results['DeepSeek'] = verify_deepseek_api()
    print()
    
    results['Finnhub'] = verify_finnhub_api()
    print()
    
    # 总结结果
    print("=" * 60)
    print("📊 验证结果总结:")
    print("=" * 60)
    
    for service, is_valid in results.items():
        status = "✅ 有效" if is_valid else "❌ 无效"
        print(f"{service:10} : {status}")
    
    valid_count = sum(results.values())
    total_count = len(results)
    print(f"\n总计: {valid_count}/{total_count} 个API密钥有效")
    
    if valid_count == total_count:
        print("🎉 所有API密钥都有效！")
    elif valid_count > 0:
        print("⚠️  部分API密钥有效，建议检查无效的密钥")
    else:
        print("🚨 所有API密钥都无效，请检查配置")

if __name__ == "__main__":
    main()