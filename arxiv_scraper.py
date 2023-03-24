import os
from dotenv import load_dotenv
import requests
import openai
import feedparser

load_dotenv()  # .envファイルを読み込む

# ArXivから論文を取得して要約を生成する
def get_arxiv_papers(search_query, max_results=2):
    base_url = 'http://export.arxiv.org/api/query?'

    query = f"search_query={search_query}&start=0&max_results={max_results}"
    url = base_url + query
    response = requests.get(url)

    if response.status_code == 200:
        feed = feedparser.parse(response.content)
        papers = []

        for entry in feed.entries:
            paper = {
                'title': entry.title,
                'authors': [author.name for author in entry.authors],
                'link': entry.link,
                'published': entry.published,
                'summary': entry.summary
            }
            papers.append(paper)

        return papers

    else:
        print(f"Error: {response.status_code}")
        return None

search_query = "all:electron"  # ここで検索クエリを指定
papers = get_arxiv_papers(search_query, max_results=5)

def generate_summary(title, text):
    # APIキーを環境変数から読み込む
    openai.api_key = os.environ["OPENAI_API_KEY"]
    
    # GPT-3.5を使用して要約を生成する
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"あなたは自然科学系を専門とする記者です。以下の文章は論文のタイトルと要約です。ある程度の学識者を対象として以下の文章を日本語で200字程度で要約してください:\n\n{title}\n\n{text}",
        temperature=0.7,
        max_tokens=500,
        n = 1,
        stop=None,
    )

    # 要約を取得して返す
    summary = response.choices[0].text.strip()
    return summary


# 論文の要約を生成して出力する
if papers:
    for i, paper in enumerate(papers[:2]):
        print(f"論文 {i + 1}:")
        print(f"タイトル: {paper['title']}")
        print(f"著者: {', '.join(paper['authors'])}")
        print(f"リンク: {paper['link']}")
        print(f"掲載日: {paper['published']}")
        print(f"要約:")
        print(generate_summary(paper['title'], paper['summary']))
        print("\n")
