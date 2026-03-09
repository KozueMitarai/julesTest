import os
from google import genai
from tavily import TavilyClient
from datetime import datetime, timedelta

# 1. クライアントの初期化
gemini_key = os.environ.get("GEMINI_API_KEY")
tavily_key = os.environ.get("TAVILY_API_KEY")

if not gemini_key or not tavily_key:
    raise ValueError("APIキー（GEMINI または TAVILY）が設定されていません。")

client = genai.Client(api_key=gemini_key)
tavily = TavilyClient(api_key=tavily_key)

# 2. 日付の計算
today = datetime.now().strftime('%Y-%m-%d')

# 3. Tavily で最新AIニュースを検索
print(f"[{today}] Tavily で最新のAIニュースを検索中...")
search_query = "latest AI news business technology"
# search_depth="advanced" でより深い情報を取得
search_result = tavily.search(query=search_query, search_depth="advanced", max_results=5)

# 検索結果をテキストにまとめる
context = ""
sources_list = []
for result in search_result['results']:
    context += f"タイトル: {result['title']}\n内容: {result['content']}\nURL: {result['url']}\n\n"
    sources_list.append(f"- [{result['title']}]({result['url']})")

# 4. Gemini 3 Flash にレポート執筆を依頼
prompt = f"""
以下の検索結果（コンテキスト）を元に、非エンジニアのビジネスパーソン向けに最新AIレポートを作成してください。

【検索結果（コンテキスト）】
{context}

【構成】
1. 今週の主要AIトピック
2. ビジネス現場での具体的な活用イメージ
3. 明日から使えるツールやTips
"""

try:
    print(f"Gemini 3 Flash でレポートを執筆中...")
    # 検索機能(tools)を使わず、コンテキストとして情報を渡すので 503 エラーを回避しやすい
    response = client.models.generate_content(
        model="gemini-3-flash",
        contents=prompt,
        config={'system_instruction': "あなたは親切なIT専門ライターです。Markdown形式で出力してください。"}
    )

    # 5. 保存処理
    report_body = response.text
    sources_section = "\n\n---\n### 📊 参考ソース一覧（Tavily Search）\n"
    final_report = report_body + sources_section + "\n".join(sources_list)

    os.makedirs("reports", exist_ok=True)
    filename = f"reports/ai_report_{today}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(final_report)
        
    print(f"成功: {filename} に保存されました。")

except Exception as e:
    print(f"エラーが発生しました: {e}")
    exit(1)
