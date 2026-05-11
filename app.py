import streamlit as st
from PIL import Image

st.title("insPLAD 이상탐지 시스템")

uploaded = st.file_uploader("이미지 업로드", type=["jpg","png","jpeg"])

if uploaded:
    image = Image.open(uploaded).convert("RGB")
    st.image(image, caption="업로드된 이미지", width=300)

    if st.button("분석 시작"):
        from pipelines.classify import classify
        with st.spinner("분류 중..."):
            class_id, class_name = classify(image)
        st.success(f"클래스: {class_name}")

        with st.spinner("이상탐지 중..."):
            from pipelines.anomaly import run_anomaly
            score, is_anomaly, heatmap, overlay = run_anomaly(image, class_id)

        col1, col2, col3 = st.columns(3)
        col1.image(image,   caption="원본")
        col2.image(heatmap, caption="히트맵")
        col3.image(overlay, caption="오버레이")

        status = "이상" if is_anomaly else "정상"
        st.metric("Anomaly Score", f"{score:.4f}", delta=status)

        with st.spinner("RAG 검색 중..."):
            from pipelines.rag import search
            query = f"{class_name} {'anomaly defect inspection' if is_anomaly else 'normal inspection'}"
            docs = search(query, class_name)

        with st.spinner("리포트 생성 중..."):
            from pipelines.llm import generate_report
            report = generate_report(class_name, score, is_anomaly, docs)
        st.markdown("### 검사 리포트")
        st.markdown(report)

        ## 여기에서 evaluate_report에서 reference를 받아야 되는데 어캄 -> reference삭제
        with st.spinner("품질 평가 중..."):
            from pipelines.evaluation import evaluate_report
            ragas = evaluate_report(query, report, docs)
        st.markdown("### RAGAS 평가 점수")
        st.json(ragas)

        with st.spinner("결과 저장 중..."):
            from pipelines.storage import save_result
            rid = save_result(class_name, score, is_anomaly, report,
                              image, heatmap, overlay, ragas)
        st.success(f"저장 완료! ID: {rid}")