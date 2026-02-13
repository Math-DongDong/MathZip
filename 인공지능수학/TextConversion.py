import streamlit as st
import pandas as pd
import re
import numpy as np
from itertools import zip_longest

# ==============================================================================
# 1. 페이지 설정 및 스타일 정의
# ==============================================================================
st.set_page_config(page_title="TF-IDF 분석기", layout="wide", page_icon="🧮")

st.markdown("""
<style>
    /* 단어 배지 스타일 */
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
    /* 가방 컨테이너 스타일 */
    .bag-container {
        border: 2px dashed #ff4b4b;
        border-radius: 10px;
        padding: 20px;
        background-color: #fff9f9;
        text-align: center;
        min-height: 200px;
    }
    /* 테이블 스타일 */
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
# 2. 헬퍼 함수 및 초기화
# ==============================================================================

# [함수] 인덱스 자동 생성 (0->A, 1->B, ... 26->AA)
def generate_doc_label(n):
    label = ""
    if n < 0: return ""
    while n >= 0:
        label = chr(65 + (n % 26)) + label
        n = n // 26 - 1
    return label

# 초기 데이터 설정
default_data = {
    "내용": [
        "경치가 좋고 사진 찍기 좋은 캠핑장",
        "시설이 깨끗하고 뷰가 좋은 캠핑장",
        "온수 잘 나오고 화장실이 깨끗하다"
    ]
}

# 세션 상태 초기화
if "doc_df" not in st.session_state:
    df = pd.DataFrame(default_data, index=["A", "B", "C"])
    df.index.name = "문서명"
    st.session_state.doc_df = df

if "wide_token_df" not in st.session_state:
    st.session_state.wide_token_df = None

# ==============================================================================
# 3. [Step 0] 텍스트 데이터 입력 (자동 인덱스 관리)
# ==============================================================================
with st.expander("📝 문서 데이터 입력 및 수정", expanded=True):
    st.info("내용을 입력하거나 행을 추가(+)하세요. **문서명(A, B...)은 자동으로 관리됩니다.**")
    
    # 1. 데이터 에디터 (인덱스 수정 불가)
    input_df = st.data_editor(
        st.session_state.doc_df,
        num_rows="dynamic",       # 행 추가/삭제 허용
        use_container_width=True,
        key="input_editor",
        disabled=["_index"]       # 인덱스 컬럼 비활성화 (읽기 전용)
    )
    
    # 2. 변경 감지 및 인덱스 자동 재정렬 로직
    if not st.session_state.doc_df.equals(input_df):
        current_rows = len(input_df)
        # 행 개수에 맞춰 A, B, C... 인덱스 재생성
        new_index = [generate_doc_label(i) for i in range(current_rows)]
        
        input_df.index = new_index
        input_df.index.name = "문서명"
        
        st.session_state.doc_df = input_df
        st.rerun()
    
    # 3. 분석 시작 버튼
    if st.button("🚀 분석 시작 (토큰화)", type="primary", use_container_width=True):
        st.session_state.doc_df = input_df
        
        # 문서별 토큰 리스트 생성
        token_lists = []
        doc_names = []
        
        for doc_name, row in st.session_state.doc_df.iterrows():
            content = str(row["내용"])
            # 특수문자 제거 후 공백 기준 분리
            cleaned = re.sub(r'[^\w\s]', '', content)
            tokens = cleaned.split()
            
            token_lists.append(tokens)
            doc_names.append(str(doc_name))
            
        # [핵심] 리스트들을 세로(Column)로 배치 (zip_longest)
        # 행(문서) 기반 데이터를 열(문서) 기반 데이터로 변환
        combined_tokens = list(zip_longest(*token_lists, fillvalue=None))
        wide_df = pd.DataFrame(combined_tokens, columns=doc_names)
        
        st.session_state.wide_token_df = wide_df
        st.rerun()

# ==============================================================================
# 4. 분석 프로세스
# ==============================================================================
if st.session_state.wide_token_df is not None:
    st.divider()
    
    # --- [Step 1] 불용어 처리 및 단어가방 ---
    col_edit, col_bag = st.columns([0.5, 0.5], gap="large")
    
    # 1-1. 왼쪽: 문서별 단어 편집 (문서가 열Column로 배치됨)
    with col_edit:
        st.subheader("1️⃣ 단어 분리 및 불용어 제거")
        st.caption("각 문서(열)에 포함된 단어들입니다. 수정하거나 지우면 결과에 반영됩니다.")
        
        edited_wide_df = st.data_editor(
            st.session_state.wide_token_df,
            use_container_width=True,
            height=400,
            num_rows="dynamic", # 단어 추가/삭제 가능
            key="wide_editor"
        )
        
        # 변경 감지 및 동기화
        if not st.session_state.wide_token_df.equals(edited_wide_df):
            st.session_state.wide_token_df = edited_wide_df
            st.rerun()

    # --- 데이터 재구성 (Wide DF -> Tokens List & Validated Vocab) ---
    doc_names = edited_wide_df.columns.tolist()
    tokens_by_doc = []
    all_valid_tokens_flat = []

    for doc in doc_names:
        # 해당 열(문서)에서 None과 빈칸을 제외한 단어들 추출
        col_tokens = edited_wide_df[doc].dropna().astype(str).tolist()
        valid_tokens = [t for t in col_tokens if t.strip() != "" and t != "None"]
        
        tokens_by_doc.append(valid_tokens)
        all_valid_tokens_flat.extend(valid_tokens)

    # 1-2. 오른쪽: 단어 가방 시각화
    with col_bag:
        st.subheader("2️⃣ 단어 가방 (Bag of Words)")
        st.caption("모든 문서에서 추출된 고유 단어 목록입니다.")
        
        # 전체 단어장(Vocabulary) 생성
        all_words = sorted(list(set(all_valid_tokens_flat)))
        
        if all_words:
            html_badges = ""
            for word in all_words:
                # 전체 문서에서의 총 등장 횟수
                count = all_valid_tokens_flat.count(word)
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

    # --------------------------------------------------------------------------
    # [Step 2] 단어빈도 (TF)
    # --------------------------------------------------------------------------
    st.divider()
    st.header("3️⃣ 단어빈도 (TF: Term Frequency)")
    st.markdown("각 문서에 등장하는 단어들의 빈도수입니다.")
    
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
    st.markdown("단어별로 그 단어가 등장하는 **문서의 개수**입니다.")
    
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
            # 요청하신 공식: n / DF
            idf_values.append(n_docs / df_val)
    
    # 소수점 포맷팅
    idf_display = [f"{v:.2f}".rstrip('0').rstrip('.') if v != 0 else "0" for v in idf_values]
    df_idf = pd.DataFrame([idf_display], columns=all_words, index=["IDF"])
    st.table(df_idf)

    # --------------------------------------------------------------------------
    # [Step 5] TF-IDF
    # --------------------------------------------------------------------------
    st.header("6️⃣ TF-IDF 구하기")
    st.markdown("단어의 중요도를 나타내는 최종 값입니다.")
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
    
    # 0이 아닌 값만 소수점 표시
    df_tfidf_display = df_tfidf.applymap(lambda x: f"{x:.2f}".rstrip('0').rstrip('.') if x != 0 else "0")
    
    st.table(df_tfidf_display)
    
    # [인사이트] 결과 해석
    st.divider()
    st.subheader("💡 분석 결과 인사이트")
    
    for idx, doc_name in enumerate(doc_names):
        row_series = df_tfidf.iloc[idx]
        max_val = row_series.max()
        
        if max_val > 0:
            # 최대값을 가진 단어들 찾기
            top_words = row_series[row_series == max_val].index.tolist()
            top_words_str = ", ".join([f"'{w}'" for w in top_words])
            st.success(f"📄 **문서 {doc_name}**의 핵심 키워드: **{top_words_str}** (점수: {max_val:.2f})")
        else:
            st.info(f"📄 문서 {doc_name}에는 특징적인 단어가 없습니다.")

else:
    st.info("👆 상단의 '분석 시작' 버튼을 눌러주세요.")