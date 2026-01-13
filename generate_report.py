import os
import google.generativeai as genai
from datetime import datetime

# APIキーの設定
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY is not set")

genai.configure(api_key=api_key)

# モデルの設定 (Gemini 1.5 Flashを使用)
# ※将来的に新しいモデルが出た場合は model_name を変更してください
model = genai.GenerativeModel('gemini-3-flash-preview')

# 今日の日付
today = datetime.now().strftime('%Y-%m-%d')

# プロンプト（指示書）の作成
prompt = f"""
あなたはIT専門のジャーナリストです。
「非エンジニア」のビジネスパーソンや一般の方に向けて、
今知っておくべき「最新のAI活用トレンド」や「便利なAIツール」について、
分かりやすく解説する記事を書いてください。

【条件】
- 専門用語は極力使わず、使う場合は噛み砕いて説明すること。
- 今日の日付: {today}
- 文字数は2000文字程度。
- 読んだ人が「明日から使ってみよう」と思えるような具体的な活用例を入れること。
- 出力はMarkdown形式で、見出しや箇条書きを使って読みやすくすること。
- タイトルは「【{today}版】非エンジニアのための最新AI活用ニュース」とすること。
"""

try:
    # コンテンツの生成
    response = model.generate_content(prompt)
    content = response.text

    # ファイルへの保存 (output ディレクトリがない場合は作成)
    os.makedirs("reports", exist_ok=True)
    filename = f"reports/ai_report_{today}.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Success: Report generated at {filename}")

except Exception as e:
    print(f"Error: {e}")
    exit(1)
