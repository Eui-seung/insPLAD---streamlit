# from optimum.intel import OVModelForFeatureExtraction
from optimum.intel import OVSentenceTransformer
# from transformers import AutoTokenizer

save_path = "./models/bge-small-ov2"
model_id = "./models/bge-small-local"

model = OVSentenceTransformer.from_pretrained(model_id, export=True)

model.save_pretrained(save_path)

print("OpenVINO 모델 저장 완료!")