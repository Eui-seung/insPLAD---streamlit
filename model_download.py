from sentence_transformers import SentenceTransformer

# 모델을 온라인에서 다운로드 후 로컬 폴더에 저장
model = SentenceTransformer("BAAI/bge-small-en-v1.5")
model.save("./models/bge-small-local")