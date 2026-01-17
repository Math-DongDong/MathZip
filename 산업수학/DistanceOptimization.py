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

with tab1:
    st.markdown("왼쪽의 예시 이미지를 참고하여, 오른쪽 행렬에 **4개 도시** 간의 거리를 입력하세요.")

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
        st.subheader("1. 문제 예시 이미지")
        
        image_path = "./기타/외판원_문제.jpg"
        
        if os.path.exists(image_path):
            st.image(image_path, caption="외판원 문제 (4개 도시)", use_container_width=True)
        else:
            st.warning(f"⚠️ 이미지를 찾을 수 없습니다.\n경로: {image_path}")
            # 이미지가 없을 때를 위한 플레이스홀더 텍스트
            st.info("이미지가 없어도 우측의 입력 기능을 통해 계산 가능합니다.")

    # [오른쪽 컬럼] 행렬 입력
    with col_input:
        st.subheader("2. 거리 행렬 입력")
        st.caption(f"A, B, C, D {NUM_CITIES}개 도시 간의 거리를 입력해주세요.")

        # 데이터프레임 초기화 (최초 실행 시 4x4 0행렬 생성)
        if "matrix_df" not in st.session_state:
            default_matrix = np.zeros((NUM_CITIES, NUM_CITIES), dtype=int)
            st.session_state.matrix_df = pd.DataFrame(
                default_matrix, 
                columns=CITY_NAMES, 
                index=CITY_NAMES
            )

        # st.data_editor 설정
        # num_rows="fixed"를 사용하여 행 추가/삭제를 막음
        edited_df = st.data_editor(
            st.session_state.matrix_df,
            key="editor",
            use_container_width=True,
            height=250,      # 높이 적절히 조절
            num_rows="fixed" # 행 개수 고정
        )
        
        # 입력 데이터 저장
        distance_matrix_input = edited_df.to_numpy()

    # -----------------------------------------------------------
    # TSP 알고리즘 함수
    # -----------------------------------------------------------
    def solve_tsp_streamlit(distance_matrix):
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
            st.success("✅ 최적 경로 계산 완료!")
            
            n_nodes = manager.GetNumberOfNodes()
            A = np.zeros((n_nodes, n_nodes), dtype=int)
            index = routing.Start(0)
            route_path = []
            
            while not routing.IsEnd(index):
                from_node = manager.IndexToNode(index)
                next_index = solution.Value(routing.NextVar(index))
                to_node = manager.IndexToNode(next_index)
                
                A[from_node, to_node] = 1
                route_path.append(CITY_NAMES[from_node])
                
                index = next_index
                
            last_node = manager.IndexToNode(index)
            route_path.append(CITY_NAMES[last_node])
            
            W = A * distance_matrix
            total_distance = solution.ObjectiveValue()

            # 결과 화면 출력
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.subheader("📍 최적 이동 경로")
                st.code(" -> ".join(route_path), language="text")
                st.metric(label="총 이동 거리", value=total_distance)
            
            with res_col2:
                st.subheader("📊 결과 행렬")
                st.dataframe(pd.DataFrame(W, columns=CITY_NAMES, index=CITY_NAMES))
        else:
            st.error("해를 찾지 못했습니다. 입력된 거리 행렬을 다시 확인해주세요.")

    # -----------------------------------------------------------
    # 실행 버튼
    # -----------------------------------------------------------
    st.divider()
    run_btn = st.button("🚀 경로 계산하기", type="primary", use_container_width=True)

    if run_btn:
        # 대각선 0 체크
        if np.any(np.diag(distance_matrix_input) != 0):
            st.warning("⚠️ 주의: 자기 자신으로의 거리(대각선)가 0이 아닙니다.")
        
        with st.spinner("최적 경로를 찾는 중..."):
            solve_tsp_streamlit(distance_matrix_input)