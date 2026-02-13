import streamlit as st
import pandas as pd
import re
import numpy as np

# ==============================================================================
# 1. 페이지 설정 및 스타일
# ==============================================================================
st.markdown("""
<style>
    /* 테이블 헤더 스타일 */
    th {
        text-align: center !important;
        background-color: #e8f4f8 !important;
    }
    /* 테이블 본문 스타일 */
    td {
        text-align: center !important;
        font-weight: 500;
    }
    /* 강조 스타일 */
    .highlight {
        background-color: #fff3cd;
        padding: 2px 5px;
        border-radius: 4px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧮 텍스트 데이터에서 유용한 정보 찾기")
st.caption("문서 내의 단어 빈도(TF)와 역문서 빈도(IDF)를 계산하여 각 단어의 중요도를 평가해봅시다.")

# ==============================================================================
# 2. 세션 상태 초기화
# ==============================================================================
# 초기 예시 데이터
default_data = [
    {"문서명": "A", "내용": "경치가 좋고 사진 찍기 좋은 캠핑장"},
    {"문서명": "B", "내용": "시설이 깨끗하고 뷰가 좋은 캠핑장"},
    {"문서명": "C", "내용": "온수 잘 나오고 화장실이 깨끗하다"}
]

if "doc_df" not in st.session_state:
    st.session_state.doc_df = pd.DataFrame(default_data)

if "final_tokens" not in st.session_state:
    st.session_state.final_tokens = None

# ==============================================================================
# 3. [Step 0] 텍스트 데이터 입력 (행 추가 가능)
# ==============================================================================
with st.expander("📝 문서 데이터 입력 및 수정", expanded=True):
    st.info("문서 내용을 입력하세요. 행을 추가하거나 삭제할 수 있습니다.")
    
    input_df = st.data_editor(
        st.session_state.doc_df,
        num_rows="dynamic",
        use_container_width=True,
        key="input_editor"
    )
    
    if st.button("🚀 분석 시작 (토큰화)", type="primary", use_container_width=True):
        st.session_state.doc_df = input_df
        
        # 전처리 및 토큰화
        tokenized_data = []
        for idx, row in input_df.iterrows():
            content = str(row["내용"])
            # 특수문자 제거
            cleaned = re.sub(r'[^\w\s]', '', content)
            tokens = cleaned.split()
            tokenized_data.append(tokens)
        
        st.session_state.final_tokens = tokenized_data
        st.rerun()

# ==============================================================================
# 4. 분석 결과 표시
# ==============================================================================
if st.session_state.final_tokens is not None:
    tokens_list = st.session_state.final_tokens
    doc_names = st.session_state.doc_df["문서명"].tolist()
    
    # 전체 단어장(Vocabulary) 생성 (중복 제거 & 정렬)
    # 2차원 리스트를 1차원으로 펴기(flatten) -> 집합(set) -> 정렬
    all_words = sorted(list(set([word for sublist in tokens_list for word in sublist])))
    
    if not all_words:
        st.warning("분석할 단어가 없습니다.")
        st.stop()

    st.divider()

    # --------------------------------------------------------------------------
    # [Step 1] 단어빈도 (TF)
    # --------------------------------------------------------------------------
    st.header("1️⃣ 단어빈도 (TF: Term Frequency)")
    st.markdown("각 문서에 등장하는 단어들의 빈도수입니다.")
    
    tf_rows = []
    for tokens in tokens_list:
        # 각 단어가 현재 문서에 몇 번 나왔는지 계산
        counts = [tokens.count(word) for word in all_words]
        tf_rows.append(counts)
    
    df_tf = pd.DataFrame(tf_rows, columns=all_words, index=doc_names)
    st.table(df_tf)

    # --------------------------------------------------------------------------
    # [Step 2] 문서빈도 (DF)
    # --------------------------------------------------------------------------
    st.header("2️⃣ 문서빈도 (DF: Document Frequency)")
    st.markdown("단어별로 그 단어가 등장하는 **문서의 개수**입니다.")
    
    # 각 단어가 몇 개의 문서에 등장했는지 계산
    # (문서 내에 여러 번 나와도 1번으로 카운트 -> set 활용)
    df_counts = []
    for word in all_words:
        count = 0
        for tokens in tokens_list:
            if word in tokens:
                count += 1
        df_counts.append(count)
        
    df_df_table = pd.DataFrame([df_counts], columns=all_words, index=["DF"])
    st.table(df_df_table)

    # --------------------------------------------------------------------------
    # [Step 3] 역문서빈도 (IDF)
    # --------------------------------------------------------------------------
    st.header("3️⃣ 역문서빈도 (IDF: Inverse Document Frequency)")
    n_docs = len(tokens_list)
    
    # LaTeX 수식 렌더링
    st.latex(r"IDF = \frac{\text{전체 문서의 개수}(n)}{\text{문서빈도}(DF)}")
    st.caption(f"현재 전체 문서의 개수(n)는 **{n_docs}**개입니다.")

    # IDF 계산 (이미지 공식: n / DF)
    # 분모가 0이 될 일은 없음 (단어장에서 가져왔으므로 최소 1번 등장)
    idf_values = [n_docs / df_val for df_val in df_counts]
    
    # 소수점 포맷팅 (정수면 정수처럼, 소수면 2자리까지)
    idf_display = [f"{v:.2f}".rstrip('0').rstrip('.') for v in idf_values]
    
    df_idf = pd.DataFrame([idf_display], columns=all_words, index=["IDF"])
    st.table(df_idf)

    # --------------------------------------------------------------------------
    # [Step 4] TF-IDF
    # --------------------------------------------------------------------------
    st.header("4️⃣ TF-IDF 구하기")
    st.markdown("단어의 중요도를 나타내는 최종 값입니다.")
    st.latex(r"\text{TF-IDF} = \text{TF} \times \text{IDF}")

    # TF-IDF 계산 (행렬 곱셈이 아닌, 요소별 곱셈)
    tfidf_rows = []
    for i in range(n_docs): # 문서별 반복
        row_vals = []
        for j in range(len(all_words)): # 단어별 반복
            tf_val = tf_rows[i][j]
            idf_val = idf_values[j] # 계산된 실수값 사용
            
            val = tf_val * idf_val
            row_vals.append(val)
        tfidf_rows.append(row_vals)

    # 데이터프레임 생성 및 포맷팅
    df_tfidf = pd.DataFrame(tfidf_rows, columns=all_words, index=doc_names)
    
    # 시각적 포맷팅 (0은 그대로 0, 나머지는 소수점 표시)
    df_tfidf_display = df_tfidf.applymap(lambda x: f"{x:.2f}".rstrip('0').rstrip('.') if x != 0 else "0")
    
    st.table(df_tfidf_display)
    
    # [인사이트] 가장 높은 TF-IDF 단어 찾기
    st.divider()
    st.subheader("💡 분석 결과 인사이트")
    
    # 각 문서별로 가장 TF-IDF가 높은 단어 찾기
    for idx, doc_name in enumerate(doc_names):
        # 시리즈로 변환
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