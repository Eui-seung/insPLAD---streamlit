from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision
from datasets import Dataset

from langchain_openai import ChatOpenAI
# from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_huggingface import HuggingFaceEmbeddings
from ragas.llms import BaseRagasLLM
# from ragas.llms.base import PromptValue
import requests, os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPEN_AI_API_KEY")

@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

class LuxiaRagasLLM(BaseRagasLLM):
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://bridge.luxiacloud.com/llm/openai/chat/completions/gpt-4o-mini/create"

    def is_finished(self, *args):
        return True
    
    def set_usage(self, usage, *args):
        pass

    def generate_text(self, prompt, n=1, temperature=1e-8, stop=None, **kwargs):
        headers = {"apikey": self.api_key, "Content-Type": "application/json"}
        data = {
            "model": "gpt-4o-mini-2024-07-18",
            "messages": [{"role": "user", "content": prompt.to_string()}],
        }
        prompt_str = prompt.to_string() if hasattr(prompt, 'to_string') else str(prompt)
        response = requests.post(self.url, headers=headers, json=data)
        res_json = response.json()
        
        from ragas.llms.base import LLMResult
        from ragas.llms.base import Generation
        
        text = res_json['choices'][0]['message']['content']
        return LLMResult(generations=[[Generation(text=text)]])

    async def agenerate_text(self, prompt, n=1, temperature=1e-8, stop=None, **kwargs):
        return self.generate_text(prompt, n, temperature, stop)


def evaluate_report(question, answer, contexts):

    ragas_llm = LuxiaRagasLLM(api_key=API_KEY)

    hf_embeddings = get_embeddings()

    ragas_embeddings = LangchainEmbeddingsWrapper(hf_embeddings)

    data = {
        "question": [question],
        "answer": [answer],
        "contexts": [contexts],
        # "reference": [reference],
    }
    dataset = Dataset.from_dict(data)
    result = evaluate(dataset, 
                      metrics=[faithfulness, answer_relevancy],
                      llm=ragas_llm,
                      embeddings=ragas_embeddings)
    return {
        "faithfulness": round(result["faithfulness"][0], 3),
        "answer_relevancy": round(result["answer_relevancy"][0], 3),
        # "context_precision": round(result["context_precision"][0], 3),
    }

# pipeline/evaluation.py 맨 밑에 추가

# if __name__ == "__main__":

#     # 가짜 데이터로 평가
#     question = "What are common defects in glass insulators?"
#     answer   = "Common defects include surface cracks, contamination, and partial discharge which can lead to failure."
#     contexts = [
#         "Glass insulators can develop surface cracks due to mechanical stress.",
#         "Contamination on glass insulators causes partial discharge and eventual failure.",
#     ]
#     # reference = "The common defects in glass insulators are surface cracks, contamination, and partial discharge."

#     scores = evaluate_report(question, answer, contexts)

#     print("RAGAS 평가 결과:")
#     for metric, score in scores.items():
#         print(f"  {metric:25s}: {score}")