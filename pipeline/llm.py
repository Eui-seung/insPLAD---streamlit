import requests, json, os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPEN_AI_API_KEY")

def generate_report(class_name, anomaly_score, is_anomaly, context_docs=None, model="gpt-4o-mini"):
    url = f"https://bridge.luxiacloud.com/llm/openai/chat/completions/{model}/create"

    headers = {
        "apikey": API_KEY,
        "Content-Type": "application/json"
    }
    context = "\n\n".join(context_docs)
    status = "ANOMALY DETECTED" if is_anomaly else "NORMAL"

    if context_docs:
        context = "\n\n".join(context_docs)
        prompt = f"""You are an industrial inspection expert analyzing insPLAD dataset results.
Reference documents (Use ONLY the information below):
{context}

Inspection result data:
- Component class: {class_name}
- Anomaly score: {anomaly_score:.4f}
- Status: {status}

[Strict Constraints]
1. DO NOT use any outside knowledge. Base the entire report ONLY on the provided Reference documents and Inspection result.
2. If the Reference documents do not contain specific information for a section, state "Information not available in reference standards" rather than speculating.
3. Match the Anomaly score and Status exactly as provided.
4. Ensure every claim in the 'Root cause analysis' can be traced back to a specific line in the Reference documents.

[Report Structure]
Generate a structured inspection report in English:
1. Summary: Brief overview of the current inspection state.
2. Root cause analysis: Identify potential causes based solely on the provided context.
3. Recommendations: Technical actions derived from the reference standards.
4. Reference standards: Cite specific guidelines or thresholds mentioned in the context.

Be concise and technical."""
    else:
        # RAG 없음 — 모델 자체 지식 사용
        prompt = f"""You are an industrial inspection expert analyzing insPLAD dataset results.

Inspection result data:
- Component class: {class_name}
- Anomaly score: {anomaly_score:.4f}
- Status: {status}

[Report Structure]
Generate a structured inspection report in English:
1. Summary: Brief overview of the current inspection state.
2. Root cause analysis: Identify potential causes based on your expert knowledge.
3. Recommendations: Technical actions to address the findings.
4. Reference standards: Cite relevant industry standards if applicable.

Be concise and technical."""

    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False 
    }  

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        if response.status_code == 200:
            result_json = response.json()
            # Luxia 응답 구조가 OpenAI 표준과 동일하다면 아래와 같이 추출
            return result_json['choices'][0]['message']['content']
        else:
            return f"Error: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"An exception occurred: {str(e)}"


# if __name__ == "__main__":

#     test_contexts = [
#         "Glass insulators are used in high-voltage transmission lines to support conductors.",
#         "Common defects include surface cracks, contamination, and partial discharge.",
#         "Anomaly detection threshold is typically set at 0.5 for PatchCore models.",
#     ]

#     report = generate_report(
#         class_name="glass-insulator",
#         anomaly_score=0.823,
#         is_anomaly=True,
#         context_docs=test_contexts
#     )

#     print("=" * 60)
#     print(report)
#     print("=" * 60)