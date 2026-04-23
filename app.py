import streamlit as st
import json
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel
import vertexai

st.title("🚀 Gemini 接続テスト")

# 1. 金庫（Secrets）から鍵を取り出す
if "gcp_json_raw" in st.secrets:
    try:
        # 文字列として保存したJSONを解析
        creds_dict = json.loads(st.secrets["gcp_json_raw"])
        creds = service_account.Credentials.from_service_account_info(creds_dict)
        
        # 2. Vertex AIの初期化
        vertexai.init(project=creds_dict["project_id"], location="asia-northeast1", credentials=creds)
        
        st.success("✅ Google Cloudへの認証に成功しました！")
        
        if st.button("Geminiを呼んでみる"):
            with st.spinner("Geminiが考え中..."):
                # 3. Gemini 1.5 Flashモデルを呼び出し
                model = GenerativeModel("gemini-1.5-flash")
                response = model.generate_content("こんにちは！テレビ東京の視聴率分析アプリを一緒に作ってください。意気込みを短くお願いします！")
                
                st.write("---")
                st.write("🤖 Geminiからの返答:")
                st.info(response.text)
                st.balloons()
    except Exception as e:
        st.error(f"❌ エラーが発生しました: {e}")
else:
    st.error("❌ Secretsに 'gcp_json_raw' が設定されていません。SettingsのSecretsを確認してください。")
