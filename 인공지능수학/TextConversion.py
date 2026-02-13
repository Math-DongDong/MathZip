import streamlit as st
import pandas as pd
import re
import numpy as np

# ==============================================================================
# 1. 페이지 설정 및 스타일
# ==============================================================================
st.set_page_config(page_title="TF-IDF 분석기", layout="wide", page_icon="🧮")

st.markdown("""
<style>
    .word-badge {
        display: inline-block;
        background-color: #f0f2f6;
        color: #31333F;
        border: 1px solid #d6d6d8;
        border-radius: 15px; 
        padding: 5px 12px;
        margin: 4px;
        font-size: 14px;
        font-weight: 500;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .word-badge:hover {
        transform: scale(1.05); 
        background-color: #e0e2e6;
        border-color: #ff4b4b; 
        cursor: pointer;
    }
    .bag-container {
        border: 2px dashed #ff4b4b;
        border-radius: 10px;
        padding: 20px;
        background-color: #fff9f9;
        text-align: center;
        min-height: 200px;
    }
    th {
        text-align: center !important;
        background-color: #e8f4f8 !important;
    }
    td {
        text-align: center !important;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧮 텍스트 데이터에서 유용한 정보 찾기 (TF-IDF)")

# ==============================================================================
# 2. 세션 상태 초기화
# ==============================================================================
# [핵심 변경 1] 문서명을 인덱스로 설정
default_data = {
    "내용": [
        "경치가 좋고 사진 찍기 좋은 캠핑장",
        "시설이 깨끗하고 뷰가 좋은 캠핑장",
        "온수 잘 나오고 화장실이 깨끗하다"
    ]
}

if "doc_df" not in st.session_state:
    # 인덱스를 A, B, C로 지정하여 생성
    df = pd.DataFrame(default_data, index=["A", "B", "C"])
    df.index.name = "문서명" # 인덱스 컬럼의 이름 지정
    st.session_state.doc_df = df

if "token_df" not in st.session_state:
    st.session_state.token_df = None

# ==============================================================================
# 3. [Step 0] 텍스트 데이터 입력 (인덱스 적용)
# ==============================================================================
with st.expander("📝 문서 데이터 입력 및 수정", expanded=True):
    st.info("왼쪽의 **'문서명'** 열도 수정할 수 있습니다. 행을 추가하면 자동으로 인덱스가 생성됩니다.")
    
    # [핵심 변경 2] data_editor가 인덱스를 보여주도록 설정
    input_df = st.data_editor(
        st.session_state.doc_df,
        num_rows="dynamic",
        use_container_width=True,
        key="input_editor"
    )
    
    if st.button("🚀 분석 시작 (토큰화)", type="primary", use_container_width=True):
        st.session_state.doc_df = input_df
        
        # 1. 문서별로 토큰화 수행
        all_tokens_data = []
        
        # [핵심 변경 3] iterrows()에서 idx(인덱스=문서명)를 바로 사용
        for doc_name, row in input_df.iterrows():
            content = str(row["내용"])
            
            # 전처리 (특수문자 제거)
            cleaned = re.sub(r'[^\w\s]', '', content)
            tokens = cleaned.split()
            
            for t in tokens:
                # 문서명(doc_name)은 인덱스 값이므로 A, B, C 등이 들어옴
                all_tokens_data.append({"문서명": str(doc_name), "단어": t})
        
        st.session_state.token_df = pd.DataFrame(all_tokens_data)
        st.rerun()

# ==============================================================================
# 4. 분석 프로세스
# ==============================================================================
if st.session_state.token_df is not None:
    st.divider()
    
    # --- [Step 1] 불용어 처리 및 단어가방 ---
    col_edit, col_bag = st.columns([0.5, 0.5], gap="large")
    
    with col_edit:
        st.subheader("1️⃣ 단어 분리 및 불용어 제거")
        st.caption("표에서 단어를 수정하거나 지우면 분석 결과에 반영됩니다.")
        
        edited_token_df = st.data_editor(
            st.session_state.token_df,
            use_container_width=True,
            height=400,
            key="token_editor",
            num_rows="dynamic"
        )
        
        if not st.session_state.token_df.equals(edited_token_df):
            st.session_state.token_df = edited_token_df
            st.rerun()

    with col_bag:
        st.subheader("2️⃣ 단어 가방 (Bag of Words)")
        st.caption("모든 문서에서 추출된 고유 단어 목록입니다.")
        
        valid_df = edited_token_df[edited_token_df["단어"].str.strip() != ""]
        valid_df = valid_df.dropna()
        
        all_words = sorted(list(set(valid_df["단어"].tolist())))
        
        if all_words:
            html_badges = ""
            total_counts = valid_df["단어"].value_counts()
            
            for word in all_words:
                count = total_counts.get(word, 0)
                html_badges += f'<span class="word-badge">{word} <small>({count})</small></span>'
            
            st.markdown(f"""
            <div class="bag-container">
                <h4>👜 Vocabulary</h4>
                <div style="margin-top: 15px;">
                    {html_badges}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("단어 가방이 비어있습니다.")
            st.stop()

    # --- 데이터 준비 (문서별 토큰 리스트 재구성) ---
    st.divider()
    
    # 문서명 목록 (인덱스에서 가져옴)
    doc_names = st.session_state.doc_df.index.tolist()
    
    tokens_by_doc = []
    # 문자열로 변환하여 비교 (인덱스가 숫자일 수도 있으므로 안전하게)
    str_doc_names = [str(d) for d in doc_names]
    
    for doc in str_doc_names:
        doc_tokens = valid_df[valid_df["문서명"] == doc]["단어"].tolist()
        tokens_by_doc.append(doc_tokens)

    # --------------------------------------------------------------------------
    # [Step 2] 단어빈도 (TF)
    # --------------------------------------------------------------------------
    st.header("3️⃣ 단어빈도 (TF: Term Frequency)")
    
    tf_rows = []
    for tokens in tokens_by_doc:
        counts = [tokens.count(word) for word in all_words]
        tf_rows.append(counts)
    
    # index를 doc_names(인덱스값)로 설정
    df_tf = pd.DataFrame(tf_rows, columns=all_words, index=doc_names)
    st.table(df_tf)

    # --------------------------------------------------------------------------
    # [Step 3] 문서빈도 (DF)
    # --------------------------------------------------------------------------
    st.header("4️⃣ 문서빈도 (DF: Document Frequency)")
    
    df_counts = []
    for word in all_words:
        count = 0
        for tokens in tokens_by_doc:
            if word in tokens:
                count += 1
        df_counts.append(count)
        
    df_df_table = pd.DataFrame([df_counts], columns=all_words, index=["DF"])
    st.table(df_df_table)

    # --------------------------------------------------------------------------
    # [Step 4] 역문서빈도 (IDF)
    # --------------------------------------------------------------------------
    st.header("5️⃣ 역문서빈도 (IDF: Inverse Document Frequency)")
    n_docs = len(doc_names)
    
    st.latex(r"IDF = \frac{\text{전체 문서의 개수}(n)}{\text{문서빈도}(DF)}")
    st.caption(f"현재 전체 문서의 개수(n)는 **{n_docs}**개입니다.")

    idf_values = []
    for df_val in df_counts:
        if df_val == 0:
            idf_values.append(0)
        else:
            idf_values.append(n_docs / df_val)
    
    idf_display = [f"{v:.2f}".rstrip('0').rstrip('.') if v != 0 else "0" for v in idf_values]
    df_idf = pd.DataFrame([idf_display], columns=all_words, index=["IDF"])
    st.table(df_idf)

    # --------------------------------------------------------------------------
    # [Step 5] TF-IDF
    # --------------------------------------------------------------------------
    st.header("6️⃣ TF-IDF 구하기")
    st.latex(r"\text{TF-IDF} = \text{TF} \times \text{IDF}")

    tfidf_rows = []
    for i in range(n_docs):
        row_vals = []
        for j in range(len(all_words)):
            tf_val = tf_rows[i][j]
            idf_val = idf_values[j]
            val = tf_val * idf_val
            row_vals.append(val)
        tfidf_rows.append(row_vals)

    df_tfidf = pd.DataFrame(tfidf_rows, columns=all_words, index=doc_names)
    df_tfidf_display = df_tfidf.applymap(lambda x: f"{x:.2f}".rstrip('0').rstrip('.') if x != 0 else "0")
    
    st.table(df_tfidf_display)
    
    # [인사이트]
    st.divider()
    st.subheader("💡 분석 결과 인사이트")
    
    for idx, doc_name in enumerate(doc_names):
        row_series = df_tfidf.iloc[idx]
        max_val = row_series.max()
        
        if max_val > 0:
            top_words = row_series[row_series == max_val].index.tolist()
            top_words_str = ", ".join([f"'{w}'" for w in top_words])
            st.success(f"📄 **문서 {doc_name}**의 핵심 키워드: **{top_words_str}** (점수: {max_val:.2f})")
        else:
            st.info(f"📄 문서 {doc_name}에는 특징적인 단어가 없습니다.")

else:
    st.info("👆 상단의 '분석 시작' 버튼을 눌러주세요.")