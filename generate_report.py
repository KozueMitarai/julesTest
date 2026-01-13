import os
from google import genai
from google.genai import types
from datetime import datetime, timedelta

# 1. クライアントの初期化
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY is not set.")

client = genai.Client(api_key=api_key)

# 2. 日付の計算
today_dt = datetime.now()
today = today_dt.strftime('%Y-%m-%d')
one_week_ago = (today_dt - timedelta(days=7)).strftime('%Y-%m-%d')

# 3. プロンプトと検索ツールの設定
# 検索期間を絞り込むための演算子を含めています
prompt = f"""
最新のAIニュースを検索し、非エンジニアのビジネスパーソン向けにレポートを作成してください。

【検索条件】
- 期間: {one_week_ago} から {today} まで（直近1週間以内）
- 検索時は必ず `after:{one_week_ago}` を考慮し、最新の情報を取得してください。

【構成】
1. 今週の主要AIトピック
2. ビジネス現場での具体的な活用イメージ
3. 明日から使えるツールやTips
"""

# ご提示いただいた最新のツール設定
grounding_tool = types.Tool(
    google_search=types.GoogleSearch()
)
config = types.GenerateContentConfig(
    tools=[grounding_tool],
    system_instruction="あなたは親切なIT専門ライターです。Markdown形式で出力してください。"
)

try:
    print(f"[{today}] Gemini 3 Flash で最新情報をリサーチ中...")
    
    # コンテンツ生成の実行
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
        config=config,
    )

    # 4. 本文の取得
    report_body = response.text

    # 5. 引用元（Grounding Metadata）の抽出
    sources_section = "\n\n---\n### 📊 参考ソース一覧（直近1週間）\n"
    sources_list = []

    if response.candidates[0].grounding_metadata:
        metadata = response.candidates[0].grounding_metadata
        # 検索結果のチャンク（断片）からタイトルとURLを取得
        if metadata.grounding_chunks:
            for chunk in metadata.grounding_chunks:
                if chunk.web:
                    title = chunk.web.title or "参照記事"
                    url = chunk.web.uri
                    sources_list.append(f"- [{title}]({url})")

    # 重複を排除して結合
    if sources_list:
        final_report = report_body + sources_section + "\n".join(list(dict.fromkeys(sources_list)))
    else:
        final_report = report_body

    # 6. 保存処理
    os.makedirs("reports", exist_ok=True)
    filename = f"reports/ai_report_{today}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(final_report)
        
    print(f"成功: {filename} に保存されました。")

except Exception as e:
    print(f"エラーが発生しました: {e}")
    exit(1)
