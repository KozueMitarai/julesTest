import os
from google import genai
from google.genai import types

def fetch_ai_news():
    # APIキーの取得
    api_key = os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=api_key)

    # Google検索ツール（Grounding）の設定
    google_search_tool = types.Tool(
        google_search=types.GoogleSearch()
    )

    prompt = """
    ここ1週間以内の「非エンジニア向けのAI活用」に関する最新情報を3つピックアップしてください。
    出力は必ず以下のマークダウン形式にしてください：
    
    ## [タイトル]
    - **概要**: (200文字程度)
    - **ソース**: (URL)
    - **活用イメージ**: (非エンジニアがどう使えるか)
    ---
    """

    # 最新モデル Gemini 3 Flash を使用
    response = client.models.generate_content(
        model='gemini-3-flash-preview', 
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[google_search_tool]
        )
    )
    
    # 保存処理
    with open("ai_news_latest.md", "w", encoding="utf-8") as f:
        f.write("# 週間AI活用情報 (Gemini 3 検索結果)\n\n")
        f.write(response.text)

if __name__ == "__main__":
    fetch_ai_news()
