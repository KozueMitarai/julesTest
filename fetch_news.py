import os
import google.generativeai as genai

# GitHub SecretsからAPIキーを取得
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def fetch_ai_news():
    # モデルの設定（Google検索機能を有効化）
    # ※2026年現在の最新安定モデルを使用
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        tools=[{"google_search_lighting": {}}] 
    )

    prompt = """
    ここ1週間以内の「非エンジニア向けのAI活用」に関する最新情報を3つピックアップしてください。
    以下の形式のマークダウンで出力してください。
    
    ## [タイトル]
    - **概要**: (200文字程度で要約)
    - **ソース**: (URL)
    - **活用イメージ**: (非エンジニアがどう使えるか)
    ---
    """

    response = model.generate_content(prompt)
    
    # 取得した内容をMarkdownファイルとして保存
    with open("ai_news_latest.md", "w", encoding="utf-8") as f:
        f.write("# 週間AI活用情報 (非エンジニア向け)\n\n")
        f.write(response.text)

if __name__ == "__main__":
    fetch_ai_news()