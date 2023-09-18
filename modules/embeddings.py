from sentence_transformers import SentenceTransformer, util


def embeddings(sentences):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print(model.max_seq_length)

    model.max_seq_length = 512
    query = model.encode(sentences, normalize_embeddings=True)
    print(query)
    return query