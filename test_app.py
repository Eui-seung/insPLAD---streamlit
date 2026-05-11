import streamlit as st
print("1. Streamlit 시작")

from pipelines.classify import classify
print("2. 분류 모듈 임포트 완료")

from pipelines.anomaly import run_anomaly
print("3. 이상탐지 모듈 임포트 완료")

from pipelines.evaluation import evaluate_report
print("4. 평가 모듈 임포트 완료 (의심)")

from pipelines.storage import save_result
print("5. 저장 모듈 임포트 완료")

st.title("insPLAD 시스템")
print("6. UI 그리기 시작")