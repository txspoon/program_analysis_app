import streamlit as st

st.title("📺 番組視聴率分析ツール（β版）")
st.write("ここに分析したい番組のSUSIE_CSVデータをアップロードしてください")

uploaded_files = st.file_uploader("CSVファイルを選択、またはドロップ", accept_multiple_files=True)

if st.button("分析スタート"):
    st.success("分析が開始されました！（※これはテスト画面です）")