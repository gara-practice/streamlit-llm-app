import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

# Streamlit アプリタイトルと説明
st.title("悩み相談 LLM アプリ")
st.markdown("""
このアプリは、悩みを入力すると、選択した専門家の立場からAIがアドバイスをしてくれるツールです。  
「悩み相談のプロ」として、あなたに寄り添った回答を行います。
""")

# 専門家の選択
selected_expert = st.radio(
    "相談したい専門家を選んでください：",
    ("悩み相談解決のプロ", "ファッションのプロ", "キャリアアドバイザー")
)

# 入力フォーム
user_input = st.text_area("悩みを入力してください：")

# LLM応答関数
def get_llm_response(user_input, expert_type):
    try:
        # モデルの初期化（gpt-4o-mini を使用）
        llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

        # 専門家に応じたシステムプロンプト
        expert_prompts = {
            "悩み相談解決のプロ": "あなたは優秀な悩み相談の専門家です。親身になって丁寧にアドバイスしてください。",
            "ファッションのプロ": "あなたは一流のファッションスタイリストです。トレンドとTPOを考慮して提案してください。",
            "キャリアアドバイザー": "あなたは経験豊富なキャリアアドバイザーです。転職や将来のキャリアに関して的確な助言をしてください。"
        }

        system_message = SystemMessage(content=expert_prompts[expert_type])
        human_message = HumanMessage(content=user_input)

        # モデルにメッセージを送信
        response = llm([system_message, human_message])

        return response.content
    
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

# 実行ボタン
if st.button("実行"):
    if user_input.strip() == "":
        st.warning("悩みの内容を入力してください。")
    else:
        result = get_llm_response(user_input, selected_expert)
        st.markdown("#### AIからのアドバイス：")
        st.write(result)