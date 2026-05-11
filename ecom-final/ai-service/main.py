"""
AI Service — FastAPI (lightweight demo version)
Mô phỏng LSTM + RAG pipeline không cần PyTorch/ChromaDB.
Đủ để chạy demo và minh họa API cho tiểu luận.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import numpy as np
import random
import httpx
import os

app = FastAPI(
    title="AI Service — E-Commerce Recommendation & Chatbot",
    description="LSTM + RAG recommendation system (demo mode)",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product-service:8001")

# ─── Pydantic Schemas ─────────────────────────────────────────────────────────

class RecommendRequest(BaseModel):
    user_id: int
    behavior_sequence: List[int]
    top_k: int = 5

class ChatRequest(BaseModel):
    user_id: int
    message: str
    chat_history: Optional[List[dict]] = []

# ─── Lightweight LSTM Simulator ───────────────────────────────────────────────

class LSTMLite:
    """
    Mô phỏng LSTM bằng numpy — đủ để demo API.
    Trong production thay bằng PyTorch LSTMRecommender.
    """
    def __init__(self, num_products: int = 200, seed: int = 42):
        rng = np.random.default_rng(seed)
        # Giả lập embedding matrix (num_products x 32)
        self.embeddings = rng.standard_normal((num_products + 1, 32))
        # Giả lập item-item similarity từ embedding
        norms = np.linalg.norm(self.embeddings, axis=1, keepdims=True)
        self.normed = self.embeddings / (norms + 1e-8)

    def predict_top_k(self, sequence: List[int], k: int = 5) -> List[dict]:
        """
        Tính score cho từng sản phẩm dựa trên cosine similarity
        với trung bình vector của sequence đầu vào.
        """
        valid = [s for s in sequence if 0 < s <= len(self.embeddings) - 1]
        if not valid:
            valid = [1, 2, 3]

        # Trung bình vector của sequence (mô phỏng LSTM hidden state)
        seq_vec = self.normed[valid].mean(axis=0)
        scores  = self.normed @ seq_vec           # cosine similarity với mọi item
        scores[valid] = -1                         # loại bỏ items đã xem

        top_idx = np.argpartition(scores, -k)[-k:]
        top_idx = top_idx[np.argsort(scores[top_idx])[::-1]]

        return [
            {"product_id": int(idx), "score": round(float(scores[idx]), 4)}
            for idx in top_idx if idx > 0
        ]


class RAGLite:
    """
    Mô phỏng RAG pipeline với keyword matching.
    Trong production thay bằng ChromaDB + sentence-transformers.
    """
    # (name, product_type, price, product_id_in_db)
    # IDs khớp với seed_data.py: electronics=1-8, books=9-13, fashion=14-17
    PRODUCT_KEYWORDS = {
        "laptop":     [("Laptop ASUS ROG G15 (2024)",  "electronics", 19500000, 1),
                       ("Màn hình LG UltraWide 34\"",  "electronics",  9990000, 5),
                       ("Bàn phím cơ Keychron K2 Pro", "electronics",  2190000, 7)],
        "điện thoại": [("iPhone 15 Pro Max 256GB",     "electronics", 34990000, 2),
                       ("Samsung Galaxy S24 Ultra",    "electronics", 32990000, 3),
                       ("Apple Watch Series 9",        "electronics", 11990000, 6)],
        "tai nghe":   [("Tai nghe Sony WH-1000XM5",   "electronics",  8490000, 4),
                       ("Apple Watch Series 9",        "electronics", 11990000, 6),
                       ("Chuột Razer DeathAdder V3",   "electronics",  1890000, 8)],
        "sách":       [("Clean Code - Robert C. Martin","book",         180000, 9),
                       ("Domain-Driven Design",        "book",          350000, 10),
                       ("Atomic Habits - James Clear", "book",          168000, 13),
                       ("The Psychology of Money",     "book",          145000, 12)],
        "áo":         [("Áo Polo Lacoste Classic Fit", "fashion",      1290000, 14),
                       ("Áo khoác The North Face",     "fashion",      3490000, 17)],
        "giày":       [("Giày Nike Air Force 1 White", "fashion",      2490000, 15),
                       ("Giày Adidas Ultraboost 22",   "fashion",      3290000, 16)],
        "thời trang": [("Áo Polo Lacoste Classic Fit", "fashion",      1290000, 14),
                       ("Giày Nike Air Force 1 White", "fashion",      2490000, 15),
                       ("Giày Adidas Ultraboost 22",   "fashion",      3290000, 16),
                       ("Áo khoác The North Face",     "fashion",      3490000, 17)],
        "gaming":     [("Laptop ASUS ROG G15 (2024)",  "electronics", 19500000, 1),
                       ("Chuột Razer DeathAdder V3",   "electronics",  1890000, 8),
                       ("Bàn phím cơ Keychron K2 Pro", "electronics",  2190000, 7)],
        "đồng hồ":    [("Apple Watch Series 9 GPS",   "electronics", 11990000, 6),
                       ("Samsung Galaxy S24 Ultra",    "electronics", 32990000, 3)],
        "default":    [("Laptop ASUS ROG G15 (2024)",  "electronics", 19500000, 1),
                       ("iPhone 15 Pro Max 256GB",     "electronics", 34990000, 2),
                       ("Tai nghe Sony WH-1000XM5",   "electronics",  8490000, 4),
                       ("Atomic Habits - James Clear", "book",          168000, 13),
                       ("Giày Nike Air Force 1 White", "fashion",      2490000, 15)],
    }

    RESPONSES = {
        "laptop":     "Với nhu cầu laptop, tôi gợi ý **{products}**. Đây là những dòng máy được đánh giá cao về hiệu năng và độ bền!",
        "điện thoại": "Về điện thoại, **{products}** đang là những lựa chọn hot nhất với camera xuất sắc và hiệu năng mạnh mẽ.",
        "tai nghe":   "Cho trải nghiệm âm thanh đỉnh cao, **{products}** là lựa chọn hàng đầu — chống ồn tốt, âm bass sâu.",
        "sách":       "Các cuốn sách **{products}** rất được yêu thích, sẽ giúp bạn mở rộng tư duy và kiến thức.",
        "áo":         "Về thời trang, **{products}** đang rất được ưa chuộng với chất liệu cao cấp và thiết kế hiện đại.",
        "giày":       "**{products}** là những đôi giày đang hot hiện nay, thoải mái và phong cách.",
        "gaming":     "Để setup gaming đỉnh, **{products}** là lựa chọn không thể bỏ qua!",
        "đồng hồ":    "**{products}** là những chiếc đồng hồ thông minh tốt nhất hiện tại.",
        "default":    "Dựa trên yêu cầu của bạn, tôi gợi ý **{products}**. Bạn muốn tư vấn chi tiết hơn không?",
    }

    # Ảnh khớp với seed_data.py — ID → Unsplash URL
    PRODUCT_IMAGES = {
        1:  'https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=480&q=80',
        2:  'https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=480&q=80',
        3:  'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=480&q=80',
        4:  'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=480&q=80',
        5:  'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=480&q=80',
        6:  'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=480&q=80',
        7:  'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=480&q=80',
        8:  'https://images.unsplash.com/photo-1527814050087-3793815479db?w=480&q=80',
        9:  'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=480&q=80',
        10: 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=480&q=80',
        11: 'https://images.unsplash.com/photo-1532012197267-da84d127e765?w=480&q=80',
        12: 'https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=480&q=80',
        13: 'https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=480&q=80',
        14: 'https://images.unsplash.com/photo-1581655353564-df123a1eb820?w=480&q=80',
        15: 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=480&q=80',
        16: 'https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=480&q=80',
        17: 'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=480&q=80',
    }

    def search(self, query: str, n: int = 5) -> list:
        query_lower = query.lower()
        matched_key = next(
            (k for k in self.PRODUCT_KEYWORDS if k in query_lower and k != "default"),
            "default"
        )
        products = list(self.PRODUCT_KEYWORDS[matched_key])
        random.shuffle(products)
        return [
            {
                "product_id":     str(item[3]),
                "name":           item[0],
                "product_type":   item[1],
                "price":          str(item[2]),
                "image_url":      self.PRODUCT_IMAGES.get(item[3], ''),
                "relevance_score": round(0.95 - i * 0.07, 2),
            }
            for i, item in enumerate(products[:n])
        ]

    def generate(self, query: str, products: list) -> str:
        query_lower = query.lower()
        matched_key = next(
            (k for k in self.RESPONSES if k in query_lower and k != "default"),
            "default"
        )
        names = ", ".join(p["name"] for p in products[:3])
        return self.RESPONSES[matched_key].format(products=names)


# Singleton instances
lstm = LSTMLite(num_products=17)  # Khớp với số sản phẩm đã seed
rag  = RAGLite()

# ─── Endpoints ────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok", "service": "ai-service", "mode": "demo", "version": "1.0.0"}


@app.post("/recommend")
async def recommend(req: RecommendRequest):
    """Gợi ý sản phẩm dựa trên chuỗi hành vi (LSTM demo)."""
    if not req.behavior_sequence:
        raise HTTPException(400, "behavior_sequence không được rỗng.")

    results = lstm.predict_top_k(req.behavior_sequence, k=req.top_k)

    # Thử lấy thông tin thật từ product-service
    enriched = []
    async with httpx.AsyncClient(timeout=3) as client:
        for item in results:
            try:
                r = await client.get(f"{PRODUCT_SERVICE_URL}/products/{item['product_id']}/")
                if r.status_code == 200:
                    product = r.json()
                    product["recommendation_score"] = item["score"]
                    enriched.append(product)
                    continue
            except Exception:
                pass
            # Fallback: trả mock product
            enriched.append({
                "product_id": item["product_id"],
                "name": f"Sản phẩm #{item['product_id']}",
                "price": str(random.randint(200, 35000) * 1000),
                "product_type": random.choice(["electronics", "book", "fashion"]),
                "rating": round(random.uniform(3.8, 5.0), 1),
                "recommendation_score": item["score"],
            })

    return {
        "user_id":        req.user_id,
        "model":          "LSTM (numpy demo)",
        "sequence_length": len(req.behavior_sequence),
        "recommendations": enriched,
    }


@app.get("/recommend")
async def recommend_get(user_id: int = 1,
                        behavior_sequence: str = "10,12,15,20",
                        top_k: int = 6):
    """GET version — dễ test trên browser."""
    seq = [int(x) for x in behavior_sequence.split(",") if x.strip().isdigit()]
    req = RecommendRequest(user_id=user_id, behavior_sequence=seq, top_k=top_k)
    return await recommend(req)


@app.post("/chatbot")
async def chatbot(req: ChatRequest):
    """Chatbot tư vấn sản phẩm (RAG demo)."""
    products = rag.search(req.message, n=5)
    answer   = rag.generate(req.message, products)
    return {
        "user_id":              req.user_id,
        "question":             req.message,
        "answer":               answer,
        "recommended_products": products,
        "sources":              [p["name"] for p in products],
        "model":                "RAG (keyword-matching demo)",
    }


@app.get("/recommend/hybrid")
async def hybrid(user_id: int = 1, query: str = "laptop", top_k: int = 5):
    """Hybrid LSTM + RAG."""
    lstm_results = lstm.predict_top_k([10, 12, 15, 20], k=top_k)
    rag_results  = rag.search(query, n=top_k)

    merged = []
    for i, (l, r) in enumerate(zip(lstm_results, rag_results)):
        merged.append({
            **r,
            "lstm_score":  round(l["score"], 3),
            "rag_score":   r["relevance_score"],
            "final_score": round(0.6 * l["score"] + 0.4 * r["relevance_score"], 3),
        })
    merged.sort(key=lambda x: x["final_score"], reverse=True)

    return {"user_id": user_id, "query": query,
            "model": "Hybrid (LSTM + RAG)", "recommendations": merged}
