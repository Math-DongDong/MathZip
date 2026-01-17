import streamlit as st
import pandas as pd
import numpy as np
import string
import os
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

st.title("🏗️ 원자력 발전소 기중기의 이동 경로 최적화")
# 탭 생성
tab1, tab2 = st.tabs(["🚚 외판원 문제 ", "🏗️ 원자력 발전소 기중기의 이동 경로"])

# -----------------------------------------------------------
# TSP 알고리즘 함수 (출력 부분 수정: 행렬 제거, 단순화)
# -----------------------------------------------------------
def solve_tsp_and_display(distance_matrix, city_names):
    distance_matrix = np.asarray(distance_matrix, dtype=int)
    
    # 데이터 모델
    data = {
        "distance_matrix": distance_matrix,
        "num_vehicles": 1,
        "depot": 0,
    }

    # OR-Tools 매니저 및 라우팅 모델 설정
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    solution = routing.SolveWithParameters(search_parameters)

    # 결과 처리
    if solution:
        index = routing.Start(0)
        route_path = []
        
        while not routing.IsEnd(index):
            from_node = manager.IndexToNode(index)
            route_path.append(city_names[from_node])
            index = solution.Value(routing.NextVar(index))
            
        last_node = manager.IndexToNode(index)
        route_path.append(city_names[last_node])
        
        total_distance = solution.ObjectiveValue()

        # [수정됨] 오른쪽 열 안에서 간결하게 결과 출력
        st.subheader("📍 **최적 이동 경로**")
        st.code(" -> ".join(route_path), language="text")
        
        st.metric(label="총 이동 거리", value=total_distance)
        
    else:
        st.error("해를 찾지 못했습니다. 입력된 거리 행렬을 다시 확인해주세요.")


with tab1:
    # -----------------------------------------------------------
    # 상수 설정 (도시 개수 4개 고정)
    # -----------------------------------------------------------
    NUM_CITIES = 4
    CITY_NAMES = list(string.ascii_uppercase)[:NUM_CITIES]  # ['A', 'B', 'C', 'D']

    # -----------------------------------------------------------
    # 메인 레이아웃 분할 (2열)
    # -----------------------------------------------------------
    col_img, col_input = st.columns([1, 1])  # 1:1 비율로 분할

    # [왼쪽 컬럼] 이미지 출력
    with col_img:
        st.subheader("1. 가중 그래프")
        
        image_path = "./기타/외판원_문제.jpg"
        st.image(image_path,width='stretch')

    # [오른쪽 컬럼] 행렬 입력 + 버튼 + 결과 출력
    with col_input:
        # 1. 헤더와 버튼 배치
        header_col, btn_col = st.columns([7, 3])
        
        with header_col:
            st.subheader("2. 가중치행렬")
            
        with btn_col:
            # 버튼을 우측 상단에 배치
            run_btn = st.button("🚀 경로 계산하기", type="primary", width='stretch')

        st.caption(f"A, B, C, D {NUM_CITIES}개 도시 간의 거리를 입력해주세요.")

        # 데이터프레임 초기화
        if "matrix_df" not in st.session_state:
            default_matrix = np.zeros((NUM_CITIES, NUM_CITIES), dtype=int)
            st.session_state.matrix_df = pd.DataFrame(
                default_matrix, 
                columns=CITY_NAMES, 
                index=CITY_NAMES
            )

        # 2. 행렬 입력창 (높이 4줄 고정)
        edited_df = st.data_editor(
            st.session_state.matrix_df,
            key="editor",
            width='stretch',
            height=178,      
            num_rows="fixed" 
        )
        
        distance_matrix_input = edited_df.to_numpy()

        # 3. 결과 출력 로직 (오른쪽 컬럼 내부에서 실행)
        if run_btn:
            # 대각선 0 체크
            if np.any(np.diag(distance_matrix_input) != 0):
                st.warning("⚠️ 주의: 자기 자신으로의 거리(대각선)가 0이 아닙니다.")
            
            with st.spinner("계산 중..."):
                # 함수 호출 시 CITY_NAMES도 함께 전달
                solve_tsp_and_display(distance_matrix_input, CITY_NAMES)