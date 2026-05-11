import requests, json, os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPEN_AI_API_KEY")

def generate_report(class_name, anomaly_score, is_anomaly, context_docs):
    url = "https://bridge.luxiacloud.com/llm/openai/chat/completions/gpt-4o-mini/create"

    headers = {
        "apikey": API_KEY,
        "Content-Type": "application/json"
    }
    context = "\n\n".join(context_docs)
    status = "ANOMALY DETECTED" if is_anomaly else "NORMAL"

    prompt = f"""You are an industrial inspection expert analyzing insPLAD dataset results.

Reference documents:
{context}

Inspection result:
- Component class: {class_name}
- Anomaly score: {anomaly_score:.4f}
- Status: {status}

Generate a structured inspection report in English with these sections:
1. Summary
2. Root cause analysis
3. Recommendations
4. Reference standards

Be concise and technical."""


    data = {
        "model": "gpt-4o-mini-2024-07-18",
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