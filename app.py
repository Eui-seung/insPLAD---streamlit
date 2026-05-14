import streamlit as st
from PIL import Image


st.title("insPLAD Anomaly Detection")

uploaded = st.file_uploader("image upload", type=["jpg","png","jpeg"])

with st.sidebar:
    st.header("Setting")
    compare_mode = st.toggle("Comparative evaluation mode", value=False)
    if compare_mode:
        st.caption("Run all three conditions and compare RAGAS scores")
        st.markdown("""
        - **A** gpt-4o + RAG *(baseline)*  
        - **B** gpt-4o-mini, No RAG  
        - **C** gpt-4o-mini + RAG *(curr)*
        """)


if uploaded:
    image = Image.open(uploaded).convert("RGB")
    st.image(image, caption="Image uploaded", width=300)

    if st.button("Starting"):
        from pipeline.classify import classify
        with st.spinner("classifying..."):
            class_id, class_name = classify(image)
        st.success(f"class: {class_name}")

        with st.spinner("Anomaly detection..."):
            from pipeline.anomaly import run_anomaly
            score, is_anomaly, heatmap, overlay = run_anomaly(image, class_id)

        col1, col2, col3 = st.columns(3)
        col1.image(image,   caption="original")
        col2.image(heatmap, caption="heatmap")
        col3.image(overlay, caption="overlay")

        status = "이상" if is_anomaly else "정상"
        st.metric("Anomaly Score", f"{score:.4f}", delta=status)

        with st.spinner("RAG Searching..."):
            from pipeline.rag import search
            query = f"{class_name} {'anomaly defect inspection' if is_anomaly else 'normal inspection'}"
            docs = search(query, class_name)

        from pipeline.llm import generate_report

        if compare_mode:
            # 세 조건 모두 생성
            with st.spinner("Making report (three condition)..."):
                report_a = generate_report(class_name, score, is_anomaly, docs,        model="gpt-4o")
                report_b = generate_report(class_name, score, is_anomaly, context_docs=None, model="gpt-4o-mini")
                report_c = generate_report(class_name, score, is_anomaly, docs,        model="gpt-4o-mini")

            # ── 3. 평가 ─────────────────────────────────────
            with st.spinner("RAGAS evaluating (three condition)..."):
                from pipeline.evaluation import evaluate_report
                scores = evaluate_report(query, docs, report_a, report_b, report_c)

            # ── 4. 탭으로 나란히 비교 ────────────────────────
            st.markdown("### result")

            # 점수 요약 테이블 (탭 위에 한눈에)
            import pandas as pd
            df = pd.DataFrame({
                "condition":               ["A: gpt-4o+RAG",      "B: mini, no RAG",    "C: mini+RAG"],
                "faithfulness":       [scores["A_gpt4o_rag"].get("faithfulness","-"),  scores["B_mini_no_rag"].get("faithfulness","-"),  scores["C_mini_rag"].get("faithfulness","-")],
                "answer_relevancy":   [scores["A_gpt4o_rag"].get("answer_relevancy","-"), scores["B_mini_no_rag"].get("answer_relevancy","-"), scores["C_mini_rag"].get("answer_relevancy","-")],
                "context_precision":  [scores["A_gpt4o_rag"].get("context_precision","-"), "-", scores["C_mini_rag"].get("context_precision","-")],
                "context_recall":     [scores["A_gpt4o_rag"].get("context_recall","-"),    "-", scores["C_mini_rag"].get("context_recall","-")],
            }).set_index("condition")
            st.dataframe(df, use_container_width=True)

            # 탭별 리포트 전문
            tab_a, tab_b, tab_c = st.tabs([
                "A: gpt-4o + RAG",
                "B: mini, No RAG",
                "C: mini + RAG",
            ])
            with tab_a:
                st.json(scores["A_gpt4o_rag"])
                st.markdown(report_a)
            with tab_b:
                st.json(scores["B_mini_no_rag"])
                st.markdown(report_b)
            with tab_c:
                st.json(scores["C_mini_rag"])
                st.markdown(report_c)

            # 저장은 현재 시스템(C) 기준
            report, ragas = report_c, scores["C_mini_rag"]

        else:
            # 기존 단일 모드
            with st.spinner("Making report..."):
                report = generate_report(class_name, score, is_anomaly, docs, model="gpt-4o-mini")
            st.markdown("### Inspection report")
            st.markdown(report)

            with st.spinner("evaluating..."):
                from pipeline.evaluation import evaluate_single
                ragas = evaluate_single(query, docs, report)
            st.markdown("### RAGAS evaluate score")
            st.json(ragas)

        # ── 5. 저장 ─────────────────────────────────────────
        with st.spinner("Saving..."):
            from pipeline.storage import save_result
            rid = save_result(class_name, score, is_anomaly, report,
                              image, heatmap, overlay, ragas)
        st.success(f"Save complete! ID: {rid}")