import os
import sys
from openai import OpenAI
from tavily import TavilyClient
from datetime import datetime

# 1. クライアントの初期化
# OpenRouter は OpenAI 互換の SDK で動作します
openrouter_key = os.environ.get("OPENROUTER_API_KEY")
tavily_key = os.environ.get("TAVILY_API_KEY")

if not openrouter_key or not tavily_key:
    print("エラー: APIキー (OPENROUTER_API_KEY または TAVILY_API_KEY) が設定されていません。")
    sys.exit(1)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=openrouter_key,
)
tavily = TavilyClient(api_key=tavily_key)

# 2. 日付の取得
today = datetime.now().strftime('%Y-%m-%d')

# 3. Tavily Search で最新情報を取得
print(f"[{today}] Tavily で最新のAIニュースを検索中...")
try:
    # 検索クエリを調整してビジネスニュースに特化
    search_result = tavily.search(
        query="latest AI technology and business news", 
        search_depth="advanced", 
        max_results=5
    )

    context = ""
    sources_list = []
    for result in search_result['results']:
        context += f"タイトル: {result['title']}\n内容: {result['content']}\nURL: {result['url']}\n\n"
        sources_list.append(f"- [{result['title']}]({result['url']})")

except Exception as e:
    print(f"Tavily 検索中にエラーが発生しました: {e}")
    sys.exit(1)

# 4. OpenRouter 経由で Gemini 3 Flash Preview にレポート執筆を依頼
prompt = f"""
以下の最新情報を元に、非エンジニアのビジネスパーソン向けにAIニュースレポートを作成してください。

【最新情報（コンテキスト）】
{context}

【構成案】
1. 今週の主要AIトピック
2. ビジネス現場での具体的な活用イメージ
3. 明日から使えるツールやTips
"""

try:
    print(f"OpenRouter 経由で Gemini 3 Flash Preview で執筆中...")
    response = client.chat.completions.create(
        model="google/gemini-3-flash-preview", 
        messages=[
            {"role": "system", "content": "あなたは親切で洞察力のあるIT専門ライターです。Markdown形式で出力してください。"},
            {"role": "user", "content": prompt}
        ],
        # ↓ ここを追加（確保するトークン量を減らして、無料枠の範囲内に収めます）
        max_tokens=2000 
    )

    report_body = response.choices[0].message.content

    # 5. ファイルの保存
    final_report = f"# AI Business Report ({today})\n\n{report_body}\n\n---\n### 📊 参考ソース一覧\n" + "\n".join(sources_list)
    
    os.makedirs("reports", exist_ok=True)
    filename = f"reports/ai_report_{today}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(final_report)
        
    print(f"成功: {filename} が作成されました。")

except Exception as e:
    print(f"レポート生成中にエラーが発生しました: {e}")
    sys.exit(1)
