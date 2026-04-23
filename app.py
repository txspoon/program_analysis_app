import streamlit as st
import json
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel
import vertexai

st.title("🚀 Gemini 再接続テスト")

if "gcp_json_raw" in st.secrets:
    try:
        creds_dict = json.loads(st.secrets["gcp_json_raw"])
        creds = service_account.Credentials.from_service_account_info(creds_dict)
        
        # リージョンを us-central1 に変更してテスト
        vertexai.init(project=creds_dict["project_id"], location="us-central1", credentials=creds)
        
        st.success(f"✅ プロジェクト '{creds_dict['project_id']}' への認証は成功しました")
        
        if st.button("Geminiを呼んでみる"):
            with st.spinner("通信中..."):
                try:
                    # モデルの初期化
                    model = GenerativeModel("gemini-1.5-flash")
                    # シンプルな生成を試行
                    response = model.generate_content("こんにちは")
                    st.success("🎉 Geminiとの通信に成功しました！")
                    st.write(response.text)
                    st.balloons()
                except Exception as inner_e:
                    st.error(f"⚠️ 認証後の呼び出しで失敗しました。権限またはAPI有効化の問題です: {inner_e}")
                    
    except Exception as e:
        st.error(f"❌ 根本的なエラー: {e}")
else:
    st.error("Secretsの設定が見つかりません。")
