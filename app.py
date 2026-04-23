import streamlit as st
import json
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel
import vertexai

st.title("🚀 Gemini 最終接続テスト")

if "gcp_json_raw" in st.secrets:
    try:
        # 1. JSONから情報を読み取る
        creds_dict = json.loads(st.secrets["gcp_json_raw"])
        # JSON内のプロジェクトIDを確実に使う
        target_project = creds_dict.get("project_id")
        
        # 2. 認証オブジェクトを作成
        creds = service_account.Credentials.from_service_account_info(creds_dict)
        
        # 3. Vertex AIの初期化（リージョンは東京を指定）
        vertexai.init(project=target_project, location="asia-northeast1", credentials=creds)
        
        st.success(f"✅ プロジェクト '{target_project}' (asia-northeast1) で認証準備完了")
        
        if st.button("今度こそGeminiを呼ぶ"):
            with st.spinner("通信中..."):
                try:
                    # 4. モデル作成時にもcredentialsを渡す（ここが重要！）
                    model = GenerativeModel("gemini-1.5-flash")
                    
                    # 5. 生成実行
                    response = model.generate_content("こんにちは、接続テストです。")
                    
                    st.success("🎉 ついに成功しました！")
                    st.write(f"🤖 返答: {response.text}")
                    st.balloons()
                    
                except Exception as inner_e:
                    st.error(f"⚠️ 呼び出しエラー: {inner_e}")
                    st.info("※このエラーが出る場合は、Google Cloudコンソールで 'Vertex AI API' が有効か再確認してください。")
                    
    except Exception as e:
        st.error(f"❌ 根本的なエラー: {e}")
else:
    st.error("Secretsに 'gcp_json_raw' が見つかりません。")
