import os
import google.generativeai as genai
from datetime import datetime, timedelta

# 1. APIキーの設定
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEYが設定されていません。GitHubのSecretsを確認してください。")

genai.configure(api_key=api_key)

# 2. モデルの設定 (最新のGemini 3 Flash Preview + Google検索ツール)
model = genai.GenerativeModel(
    model_name='gemini-3-flash-preview',
    tools=[{'google_search': {}}] 
)

# 3. 日付の計算（今日と7日前）
today_dt = datetime.now()
today = today_dt.strftime('%Y-%m-%d')
one_week_ago = (today_dt - timedelta(days=7)).strftime('%Y-%m-%d')

# 4. プロンプトの作成
prompt = f"""
あなたは最新テクノロジーに精通した親しみやすいITライターです。
Google検索を使用して、以下の条件でレポートを作成してください。

【検索の制約】
- 期間: {one_week_ago} から {today} まで（直近1週間以内）の情報に限定してください。
- 検索時は必ず `after:{one_week_ago}` 演算子を活用し、古い情報を除外してください。

【ターゲット】
- AIに興味はあるが、専門用語には詳しくない一般のビジネスパーソン。

【レポート構成】
1. 今週の重要AIニュースTOP3（何が起きたのか？）
2. 非エンジニアが注目すべきポイント（なぜ重要なのか？）
3. 明日から仕事で使えるAI活用のヒント（具体的な活用法）

【執筆スタイル】
- 専門用語を避け、中学生でも理解できる言葉で解説してください。
- 読者がワクワクするような、前向きで明るいトーンで執筆してください。
- 出力はMarkdown形式。
- タイトルは「【{today}版】AIを味方に！今週の最新活用トレンド」としてください。
"""

try:
    print(f"[{today}] レポート作成を開始します...")
    
    # コンテンツ生成
    response = model.generate_content(prompt)
    content = response.text

    # 5. 引用元（ソース）情報の抽出
    sources = []
    if response.candidates and response.candidates[0].grounding_metadata:
        metadata = response.candidates[0].grounding_metadata
        if hasattr(metadata, 'grounding_chunks'):
            for chunk in metadata.grounding_chunks:
                if chunk.web:
                    title = chunk.web.title if chunk.web.title else "参照記事"
                    uri = chunk.web.uri
                    sources.append(f"- [{title}]({uri})")

    # 本文とソース一覧を結合
    final_report = content
    if sources:
        unique_sources = "\n".join(list(dict.fromkeys(sources))) # 重複排除
        final_report += f"\n\n---\n### 📊 この記事の参照元（直近1週間のニュース）\n{unique_sources}"

    # 6. Markdownファイルとして保存
    output_dir = "reports"
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{output_dir}/ai_report_{today}.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(final_report)
        
    print(f"成功: {filename} を保存しました。")

except Exception as e:
    print(f"エラーが発生しました: {e}")
    exit(1)
