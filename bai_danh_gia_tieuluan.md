# BÀI ĐÁNH GIÁ TIỂU LUẬN
## Môn học: Kiến trúc và Thiết kế Phần mềm (SoAD)
## Đề tài: Xây dựng Hệ thống E-Commerce theo Microservices và AI
### GVHD: Trần Đình Quế

---

## I. TỔNG QUAN

Tiểu luận trình bày quá trình thiết kế và xây dựng một hệ thống thương mại điện tử (EcomAI) theo kiến trúc Microservices kết hợp với AI tư vấn sản phẩm. Hệ thống bao gồm 7 microservice Django/FastAPI, 1 API Gateway Nginx, 6 database riêng biệt, cùng với giao diện frontend hiện đại. Bài đánh giá này phân tích mức độ đáp ứng từng tiêu chí theo từng chương.

**Thang điểm đánh giá từng tiêu chí:**
- **Xuất sắc (A)**: Trình bày đầy đủ, chi tiết, có minh họa rõ ràng
- **Tốt (B)**: Đáp ứng yêu cầu, còn thiếu một số chi tiết nhỏ
- **Đạt (C)**: Đáp ứng cơ bản, cần bổ sung thêm
- **Chưa đạt (D)**: Thiếu hoặc sơ sài

---

## II. ĐÁNH GIÁ CHƯƠNG 1: Từ Monolithic đến Microservices và DDD

### Tiêu chí 1.1 — Hình so sánh Monolithic và Microservices

**Đánh giá: B (Tốt)**

Tiểu luận cung cấp **sơ đồ ASCII trực quan** thể hiện sự khác biệt giữa hai kiến trúc. Phía Monolithic minh họa đầy đủ 3 layer (Presentation, Business Logic, Data Access) cùng với một database duy nhất. Phía Microservices thể hiện rõ 7 service độc lập với port riêng, database riêng và kết nối qua API Gateway.

**Điểm mạnh:**
- Sơ đồ so sánh song song ("MONOLITHIC vs MICROSERVICES") giúp người đọc nắm bắt nhanh sự khác biệt về cấu trúc
- Chú thích rõ ràng về số port, loại database cho từng service
- Thể hiện được sự chuyển đổi từ "1 deploy toàn bộ" sang "deploy độc lập từng service"

**Điểm cần cải thiện:**
- Sơ đồ ASCII có giới hạn về tính trực quan so với hình vẽ thực (draw.io/Visual Paradigm)
- Chưa có hình minh họa dạng flow diagram thể hiện luồng request qua API Gateway

**Gợi ý bổ sung:** Bổ sung hình vẽ bằng công cụ đồ họa (draw.io) để tiểu luận in ra nhìn chuyên nghiệp hơn.

---

### Tiêu chí 1.2 — Bảng so sánh Monolithic và Microservices

**Đánh giá: A (Xuất sắc)**

Tiểu luận trình bày **bảng so sánh 12 tiêu chí** toàn diện, bao gồm: Triển khai, Scale, Coupling, Database, Ngôn ngữ/Framework, Fault Isolation, Team size, Complexity vận hành, Debug/Trace, CI/CD, Time to market và Chi phí hạ tầng.

**Điểm mạnh:**
- Phủ đầy đủ các khía cạnh kỹ thuật và vận hành
- Phân tích thực tế (ví dụ: "Lỗi 1 chỗ = sập toàn hệ" vs "Lỗi 1 service, còn lại OK")
- Bảng bổ sung về "Thiết kế Microservices khác Monolithic" đi vào chi tiết kỹ thuật (giao tiếp module, xử lý lỗi, transaction, logging, testing)

**Nhận xét:** Đây là phần được trình bày tốt nhất của chương 1. Người đọc có thể dùng hai bảng này như tài liệu tham chiếu khi đánh giá lựa chọn kiến trúc cho dự án thực tế.

---

### Tiêu chí 1.3 — Các Big Tech sử dụng Microservices và quá trình phát triển

**Đánh giá: A (Xuất sắc)**

Tiểu luận phân tích **4 công ty lớn** (Netflix, Amazon, Uber, Shopify) với timeline và số liệu cụ thể:

| Công ty | Điểm nổi bật trong tiểu luận |
|---------|------------------------------|
| **Netflix** | Sự cố 3 ngày downtime 2008, timeline 4 giai đoạn, Chaos Engineering |
| **Amazon** | "API Mandate" của Jeff Bezos, Two-Pizza Team, nền tảng cho AWS |
| **Uber** | Tăng trưởng từ 1 → 70+ quốc gia, 2.200+ microservices |
| **Shopify** | "Majestic Monolith", lựa chọn Modular Monolith thay vì full micro |

**Điểm đặc biệt:**
- Case Shopify là ví dụ "counter-argument" hay — không phải lúc nào Microservices cũng tốt hơn
- Netflix Chaos Engineering được giải thích đúng bản chất (cố tình gây lỗi để kiểm thử độ bền)
- Bảng timeline Netflix 4 giai đoạn (2007 → nay) cung cấp bức tranh toàn cảnh

**Gợi ý:** Có thể thêm số liệu impact cụ thể (ví dụ: Netflix tăng uptime từ bao nhiêu % lên 99.99% sau migration).

---

### Tiêu chí 1.4 — Thiết kế Microservices khác Monolithic như thế nào

**Đánh giá: B (Tốt)**

Tiểu luận trình bày bảng so sánh 8 khía cạnh kỹ thuật thiết kế:
- Giao tiếp module: Gọi hàm trực tiếp → HTTP REST/gRPC/Message Queue
- Xử lý lỗi: Try-catch → Circuit Breaker, Retry, Timeout
- Transaction: ACID → Saga Pattern, Eventual Consistency
- Testing: Unit/Integration → Contract Test, Consumer-driven Test
- API Gateway: Không cần → Bắt buộc

**Điểm mạnh:**
- Bảng rõ ràng, phù hợp cho developer cần tham chiếu khi chuyển đổi kiến trúc
- Đề cập đến các pattern nâng cao (Saga, Circuit Breaker) thể hiện kiến thức sâu

**Điểm cần cải thiện:**
- Chưa có code minh họa cho từng pattern (ví dụ: Circuit Breaker pattern với code Python)
- Chưa giải thích Eventual Consistency và cách xử lý trong hệ thống thực tế

---

### Tiêu chí 1.5 — Healthcare Case Study (phân rã và tạo service với Django)

**Đánh giá: A (Xuất sắc)**

Đây là phần thực hành ấn tượng nhất của chương 1. Tiểu luận thực hiện đầy đủ **4 bước phân rã DDD**:

**Bước 1 — Xác định Domain:** 3 domain rõ ràng với chức năng và entities chính.

**Bước 2 — Bounded Context:** Sơ đồ quan hệ Customer-Supplier giữa 3 context.

**Bước 3 — Phân rã thành 3 Microservices Django** với code thực tế:

```python
# Patient Service — models.py đầy đủ với MedicalHistory
class Patient(models.Model):
    full_name     = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    blood_type    = models.CharField(max_length=5)
    # ... Anti-Corruption: doctor_id không import Doctor model

class MedicalHistory(models.Model):
    patient   = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor_id = models.IntegerField()  # chỉ lưu ID, không import trực tiếp
```

**Bước 4 — Luồng API:** Sequence diagram dạng text mô tả Appointment Service gọi Patient và Doctor service để validate.

**Điểm nổi bật:**
- Code Django thực tế, có thể chạy được ngay
- Áp dụng đúng Anti-Corruption Layer (không import model của service khác, chỉ lưu ID)
- Cấu trúc thư mục 3 service riêng biệt rõ ràng
- Bảng API endpoints đầy đủ với method, endpoint, mô tả

**Tổng điểm Chương 1: 8.5/10**

---

## III. ĐÁNH GIÁ CHƯƠNG 2: Phát triển Hệ E-Commerce Microservices

### Tiêu chí 2.1 — Phân tích yêu cầu

**Đánh giá: A (Xuất sắc)**

**Functional Requirements:** 11 chức năng được liệt kê đầy đủ với Actor và mô tả chi tiết, bao gồm cả FR-09 (AI Recommendation) và FR-10 (Chatbot RAG) — thể hiện tư duy tích hợp AI vào system requirements từ đầu.

**Non-functional Requirements:** 6 thuộc tính với giải pháp cụ thể cho từng thuộc tính (Scalability → Docker + Kubernetes-ready; Security → djangorestframework-simplejwt).

**Use Case Diagram:** Phân chia 3 Actor rõ ràng (Customer, Staff, Admin) với các use case phù hợp từng role.

**Điểm mạnh:**
- FR được đánh số (FR-01 đến FR-11) giúp truy xuất khi cần
- NFR không chỉ liệt kê thuộc tính mà còn nêu giải pháp cụ thể
- Use case phản ánh đúng RBAC (Admin có quyền mà Customer không có)

---

### Tiêu chí 2.2 — Phân rã service và hình ảnh

**Đánh giá: B (Tốt)**

Tiểu luận trình bày **sơ đồ Bounded Context** với 7 service đầy đủ, mỗi service có port và database riêng. Sơ đồ ASCII thể hiện API Gateway như single entry point.

**Nguyên tắc phân rã:** Được phát biểu rõ — mỗi Bounded Context = 1 Microservice, database riêng, giao tiếp qua REST API.

**Điểm cần cải thiện:**
- Sơ đồ ASCII hạn chế tính trực quan; nên có thêm hình vẽ bằng tool chuyên dụng
- Chưa thể hiện rõ luồng data giữa các service (data flow diagram)

---

### Tiêu chí 2.3 — Thiết kế từng service (Use Case, Bảng, Biểu đồ lớp)

**Đánh giá: A (Xuất sắc)**

Tiểu luận thiết kế chi tiết cho từng service với đầy đủ 3 thành phần:

**Class Diagrams:**
- User Service: User (AbstractUser) với đầy đủ attributes và methods
- Product Service: Hierarchy rõ ràng Category → Product → Book/Electronics/Fashion (OneToOne relationship)
- Cart Service: Cart 1:N CartItem với unique_together constraint
- Order Service: Order state machine với 8 trạng thái, 1:N OrderItem

**Bảng RBAC:**
Bảng phân quyền 7 hành động × 3 role thể hiện đầy đủ quyền của Admin/Staff/Customer.

**Bảng API Endpoints:**
Mỗi service có bảng API với Method, Endpoint, Mô tả và Auth requirement.

**Điểm nổi bật:**
- Product Service class diagram thể hiện đúng pattern kế thừa: Product là base, Book/Electronics/Fashion là extension qua OneToOne (không phải OOP inheritance mà là DB-level extension)
- Payment model dùng UUID cho transaction_id — thực hành tốt trong payment systems

---

### Tiêu chí 2.4 — Thể hiện service qua Django

**Đánh giá: A (Xuất sắc)**

Code Django được trình bày đầy đủ và thực tế:

**User Service:**
```python
class User(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES,
                            default='customer', db_index=True)
    @property
    def is_admin(self): return self.role == 'admin'
```

**Product Service:**
```python
class Product(models.Model):
    # 10 loại sản phẩm với db_index trên các field hay query
    class Meta:
        indexes = [models.Index(fields=['product_type', 'is_active'])]
```

Code thể hiện:
- Đúng Django patterns (AbstractUser, ForeignKey, OneToOneField)
- Có performance optimization (db_index, Meta.indexes)
- Anti-Corruption Layer: CartItem lưu `product_price` snapshot tại thời điểm thêm vào giỏ — tránh sai giá khi giá sản phẩm thay đổi

**seed_data management command:**
Đây là điểm cộng quan trọng — không chỉ code model mà còn có script seeding với 17 sản phẩm thực tế có ảnh Unsplash cụ thể cho từng sản phẩm.

---

### Tiêu chí 2.5 — Flow luồng (Sequence Diagram, Activity Diagram)

**Đánh giá: A (Xuất sắc)**

**Sequence Diagram — Luồng mua hàng End-to-End:**
Trình bày đầy đủ 7 actor (Customer, Gateway, User-Svc, Product-Svc, Cart-Svc, Order-Svc, Payment-Svc, Shipping-Svc) với các bước:
1. Login → nhận JWT
2. GET products → hiển thị
3. POST cart/add → verify stock với Product service
4. POST orders/create → lấy cart → tạo order → clear cart
5. POST payment/pay → cập nhật order status → tạo shipment

**Activity Diagram — Thanh toán:**
Flow rẽ nhánh YES/NO rõ ràng:
- Kiểm tra đã thanh toán → tạo Payment → gọi Gateway → phân nhánh success/failed → trigger Order + Shipping

**Điểm mạnh:**
- Sequence diagram thể hiện đúng pattern "saga choreography" — các service tự trigger nhau thay vì một orchestrator tập trung
- Activity diagram có đủ decision points (diamond shape)

---

### Tiêu chí 2.6 — Biểu đồ Data Model và công nghệ Database

**Đánh giá: B (Tốt)**

**Data Model tổng thể:** Liệt kê đầy đủ 6 database với các table chính và foreign key relationships.

**SQL Schema:** Cung cấp CREATE TABLE statements cho tất cả 6 service với kiểu dữ liệu phù hợp:
- UUID cho payment transaction_id
- JSONB cho electronics specifications (tận dụng PostgreSQL)
- UNIQUE constraint hợp lý (order_id UNIQUE trong shipments)

**So sánh MySQL vs PostgreSQL:** Bảng phân tích 6 tiêu chí với lý do chọn từng loại cho từng service.

**Điểm cần bổ sung:**
- Chưa có ERD diagram (Entity Relationship Diagram) dạng đồ họa
- Chưa phân tích indexing strategy cho các query hay dùng

**Tổng điểm Chương 2: 9.0/10**

---

## IV. ĐÁNH GIÁ CHƯƠNG 3: AI Service cho Tư vấn Sản phẩm

### Tiêu chí 3.1 — Mô tả yêu cầu và Pipeline

**Đánh giá: A (Xuất sắc)**

Pipeline được mô tả với **2 luồng chính** rõ ràng:
- **Recommendation flow**: User Behavior → LSTM Model → Score Merger → Top-K Products
- **Chatbot flow**: User Query → Keyword Matching/Embedding → Retrieval → Augment → Generate → Response

Sơ đồ pipeline ASCII thể hiện đủ các thành phần: LSTM, Knowledge Graph, RAG Pipeline, và mối quan hệ với Product Service.

**Điểm mạnh:**
- Phân chia rõ 2 output: Recommendation list (gợi ý sản phẩm) và Chatbot response (tư vấn)
- Mô tả API endpoint tương ứng: `/recommend` và `/chatbot`

---

### Tiêu chí 3.2 — Deep Learning (LSTM)

**Đánh giá: A (Xuất sắc)**

**Kiến trúc LSTM được trình bày ở 2 cấp độ:**

*Cấp lý thuyết:* Sơ đồ các tầng Input → Embedding (64-dim) → LSTM Layer 1 (128, dropout=0.3) → LSTM Layer 2 (128) → Dropout → Linear (128→17) → Softmax → P(next_product).

*Cấp lý giải:* Giải thích từng tầng bằng ngôn ngữ domain-specific:
- Embedding: "ánh xạ product_id → dense vector"
- LSTM: "học phụ thuộc tuần tự trong chuỗi hành vi"
- Dropout: "chống overfitting"
- Output: "xác suất P(next_product | sequence)"

**Lý do chọn LSTM được lập luận đúng:**
- User có pattern hành vi tuần tự (sequential behavior)
- LSTM giải quyết vanishing gradient tốt hơn RNN thông thường
- Giảm cold-start so với Collaborative Filtering (ít lịch sử vẫn gợi ý được)

**Code thực tế (cả 2 phiên bản):**

*NumPy version* (production demo): Giải thích thuật toán bằng cosine similarity, dễ hiểu, không cần PyTorch/GPU.

*PyTorch version* (production-ready): Code class LSTMRecommender đầy đủ với `__init__`, `forward`, `predict_top_k` và training loop.

**Điểm đặc biệt:** Có training loop với Adam optimizer và CrossEntropyLoss — thể hiện hiểu biết về quá trình huấn luyện mô hình.

---

### Tiêu chí 3.3 — Các mô hình sử dụng

**Đánh giá: B (Tốt)**

Tiểu luận trình bày **3 mô hình kết hợp:**

| Mô hình | Vai trò | Implementation |
|---------|---------|----------------|
| **LSTM** | Sequence-based recommendation | NumPy/PyTorch |
| **RAG Pipeline** | Semantic search + generation | Keyword matching → template |
| **Hybrid** | Kết hợp score: 0.6×LSTM + 0.4×RAG | Weighted fusion |

**Điểm mạnh:** Hybrid model được lý giải về tỷ trọng (0.6 LSTM / 0.4 RAG) — ưu tiên behavior-based hơn semantic-based.

**Điểm cần bổ sung:**
- Chưa trình bày Knowledge Graph (Neo4j) — đề cập trong pipeline nhưng không implement
- ChromaDB vector database chỉ được đề cập như "production plan" mà chưa có code

---

### Tiêu chí 3.4 — Code cấu trúc và giải thích

**Đánh giá: A (Xuất sắc)**

Code được trình bày **có giải thích từng phần**:

```python
class LSTMLite:
    """
    Thuật toán:
    1. Mỗi product_id ánh xạ thành vector 32 chiều (embedding)
    2. Trung bình vector trong sequence = "user interest vector"
    3. Cosine similarity với tất cả product vectors
    4. Loại bỏ items đã xem → Top-K score cao nhất
    """
```

RAG Pipeline code với chú thích rõ từng bước:
```python
def search(self, query, n=5):
    # Bước 1: Keyword matching → tìm danh mục
    # Bước 2: Lấy sản phẩm trong danh mục
    # Bước 3: Tính relevance_score giảm dần
    # Bước 4: Gắn image_url từ PRODUCT_IMAGES dict
```

FastAPI endpoint `/chatbot` với docstring mô tả 2 bước Retrieve + Generate.

---

### Tiêu chí 3.5 — Dữ liệu thử nghiệm (2-3 datasets)

**Đánh giá: B (Tốt)**

Cung cấp **3 datasets** với ý nghĩa thực tế:
- Dataset 1: Hành vi Điện tử — pattern "laptop → peripheral setup"
- Dataset 2: Hành vi Sách — pattern "IT books → self-development"
- Dataset 3: Mix — pattern "IT books → laptop purchase"

Mỗi dataset có cột "Nhận xét" giải thích ý nghĩa hành vi.

**Điểm cần cải thiện:**
- Dataset khá nhỏ (4-3-3 rows); cần mô tả rõ đây là "illustrative examples" chứ không phải training data thực
- Chưa có data preprocessing steps (tokenization, normalization, train/val/test split)

---

### Tiêu chí 3.6 — Kết quả so sánh

**Đánh giá: B (Tốt)**

**Bảng kết quả 4 phương pháp × 4 metrics:**

| Phương pháp | Precision@5 | Recall@5 | F1@5 | NDCG@5 |
|------------|------------|----------|------|--------|
| Random | 0.08 | 0.05 | 0.06 | 0.04 |
| Collab. Filtering | 0.31 | 0.24 | 0.27 | 0.29 |
| LSTM | 0.52 | 0.43 | 0.47 | 0.49 |
| Hybrid LSTM+RAG | **0.67** | **0.58** | **0.62** | **0.64** |

**Biểu đồ ASCII:** Thanh ngang so sánh Precision@5 và NDCG@5 trực quan.

**Nhận xét phân tích:** LSTM vượt Collab. Filtering 67%, Hybrid tốt nhất vì kết hợp hai loại thông tin.

**Điểm cần cải thiện:**
- Chưa giải thích cách tính các metrics (bộ test data lấy từ đâu, chia như thế nào)
- Kết quả có thể là ước tính lý thuyết — nên ghi chú rõ "simulated results"
- Nên có biểu đồ cột/đường bằng tool thực (matplotlib/Excel) thay vì ASCII

---

### Tiêu chí 3.7 — Deploy AI Service

**Đánh giá: B (Tốt)**

Tech stack được lý giải rõ ràng:
- FastAPI: "Async, tự động OpenAPI docs"
- NumPy: "Nhẹ, không cần GPU cho demo"
- Template-based: "Có fallback, không cần API key"

Dockerfile đơn giản, gọn, production-ready.

Requirements tối ưu chỉ có 6 packages, tránh dependency nặng (PyTorch chỉ cho production).

---

### Tiêu chí 3.8 — RAG và tích hợp Chat + DL

**Đánh giá: A (Xuất sắc)**

**Pipeline RAG chi tiết 4 bước** với ví dụ cụ thể:
```
Input: "toi can laptop gaming duoi 20 trieu"
    → [Keyword: "laptop"]
    → [Retrieve: ASUS ROG G15 (0.95), LG UltraWide (0.88), Keychron K2 (0.81)]
    → [Augment: build context string]
    → [Generate: "Với nhu cầu laptop gaming..."]
```

**Hybrid /recommend/hybrid endpoint:**
Code rõ ràng với trọng số: `final_score = 0.6 * lstm + 0.4 * rag`

**PRODUCT_IMAGES mapping:** Mỗi product_id được map cứng với Unsplash URL đúng — giải quyết vấn đề ảnh lệch nội dung.

---

### Tiêu chí 3.9 — Tích hợp E-Commerce (giao diện)

**Đánh giá: A (Xuất sắc)**

**Recommendation Widget:**
- 6 card sản phẩm trên trang chủ với ảnh Unsplash thật
- Hover effect, nút "Thêm giỏ" và link product-detail
- Fallback sang MOCK_PRODUCTS khi API lỗi

**Chatbot Widget:**
- Floating button góc phải với pulse animation
- Text trả lời tự nhiên tiếng Việt
- Product cards kèm ảnh, giá, nút "Xem" + "Giỏ" có thể click
- **Lịch sử chat persistent**: Lưu vào localStorage, khôi phục khi đóng/mở lại
- Restore cả product cards (không chỉ text)

**Ví dụ response JSON mẫu:**
```json
{
  "answer": "Với nhu cầu laptop gaming dưới 20 triệu...",
  "recommended_products": [
    {"product_id": "1", "image_url": "https://unsplash...", "price": "19500000"}
  ]
}
```

**Tổng điểm Chương 3: 8.5/10**

---

## V. ĐÁNH GIÁ CHƯƠNG 4: Xây dựng Hệ thống Hoàn chỉnh

### Tiêu chí 4.1 — Mô tả kiến trúc với code toàn hệ thống

**Đánh giá: A (Xuất sắc)**

**System Architecture Diagram:**
Sơ đồ ASCII đầy đủ 10 thành phần — INTERNET → API Gateway → 7 Services → 6 Databases.

**Cấu trúc thư mục hoàn chỉnh:**
```
ecom-final/
├── gateway/nginx.conf
├── user-service/     (Django + MySQL)
├── product-service/  (Django + PostgreSQL, seed_data)
├── cart-service/     (Django, migrations tĩnh)
├── order-service/    (Django, state machine)
├── payment-service/  (Django, UUID transaction)
├── shipping-service/ (Django, tracking)
├── ai-service/       (FastAPI, LSTM+RAG)
├── frontend/         (Nginx, 5 trang Light + 5 trang Dark)
└── infrastructure/   (docker-compose.yml)
```

Cấu trúc thư mục thể hiện đúng nguyên tắc Microservices — mỗi service là một project độc lập.

**nginx.conf production-quality:**
```nginx
resolver 127.0.0.11 valid=10s ipv6=off;  # Docker DNS
limit_req_zone ... rate=60r/m;            # Rate limiting
add_header Access-Control-Allow-Origin *; # CORS
if ($request_method = OPTIONS) { return 204; } # Preflight
```
Đây là cấu hình Nginx đúng chuẩn production với DNS resolver động, rate limiting và CORS handling.

---

### Tiêu chí 4.2 — Các công nghệ sử dụng

**Đánh giá: A (Xuất sắc)**

**Bảng Tech Stack 15 dòng** phân loại theo Layer với lý do chọn cụ thể cho từng technology:

| Layer | Technology | Lý do |
|-------|-----------|-------|
| Gateway | Nginx 1.25 | Reverse proxy, rate limiting |
| Backend | Django 4.2.7 + DRF | ORM mạnh, AbstractUser |
| AI | FastAPI + NumPy | Async, nhẹ cho demo |
| Auth | JWT simplejwt | Stateless, microservice-friendly |
| DB User | MySQL 8.0 | Authentication workload đơn giản |
| DB Others | PostgreSQL 15 | JSONB, complex queries |

**Điểm đặc biệt:**
- Lý giải tại sao MySQL cho User và PostgreSQL cho Product (không phải tùy tiện)
- Docker 24+ và Docker Compose 3.9 đảm bảo nhất quán môi trường
- Frontend dùng Space Grotesk (dark theme) vs Inter (light theme) — chú ý đến typography

---

### Tiêu chí 4.3 — Triển khai

**Đánh giá: A (Xuất sắc)**

**Docker Compose đầy đủ:**
- 15 containers (7 services + 6 databases + 1 gateway + 1 frontend)
- Health check cho databases trước khi service start
- `depends_on` với `condition: service_healthy` đảm bảo thứ tự khởi động đúng

**Hướng dẫn triển khai step-by-step:**
```bash
docker compose up --build              # Bước 1: Build và chạy
docker exec product-service python manage.py seed_data  # Bước 2: Seed
http://localhost:3000                  # Bước 3: Truy cập
```

**Tài khoản mặc định sau seed:**

| Tài khoản | Mật khẩu | Quyền |
|-----------|---------|-------|
| admin | Admin@123 | Toàn quyền |
| staff01 | Staff@123 | Xử lý đơn hàng |
| customer | Customer@123 | Mua hàng |

**Giải quyết vấn đề thực tế:**
- Migrations tĩnh (không dùng `makemigrations` runtime) — đúng best practice
- Cache-busting với `?v=4` query string trên JS files — tránh browser cache stale
- MOCK_PRODUCTS fallback — site hoạt động ngay cả khi backend chưa ready

---

### Tiêu chí 4.4 — Thể hiện kết quả chi tiết

**Đánh giá: A (Xuất sắc)**

Tiểu luận cung cấp **6 API response mẫu** đầy đủ:

**1. Đăng nhập:**
```json
{"user": {"id": 3, "role": "customer"}, "access": "eyJhbGc...", "refresh": "..."}
```

**2. Danh sách sản phẩm:**
```json
{"count": 17, "next": "?page=2", "results": [{
    "id": 13, "name": "Atomic Habits",
    "book_detail": {"author": "James Clear", "isbn": "9780735211292"}
}]}
```

**3. Tạo đơn hàng:**
```json
{"id": 55, "status": "pending", "status_display": "Chờ xác nhận",
 "items": [{"product_name": "Atomic Habits", "subtotal": "168000.00"}]}
```

**4. AI Recommendation:**
```json
{"model": "LSTM (numpy demo)", "recommendations": [
    {"name": "The Psychology of Money", "recommendation_score": 0.3421}
]}
```

**5. Chatbot RAG:**
```json
{"answer": "Các cuốn sách Clean Code... rất được yêu thích",
 "recommended_products": [{"image_url": "https://unsplash..."}]}
```

**6. Tracking vận chuyển:**
```json
{"tracking_code": "GHN2048301762", "status": "processing",
 "history": [{"location": "Kho Hà Nội", "timestamp": "..."}]}
```

**Bảng hiệu năng ước tính:**
| Endpoint | Avg | P95 |
|----------|-----|-----|
| GET /products/ | ~45ms | ~120ms |
| POST /chatbot | ~30ms | ~100ms |

**Đánh giá ưu/nhược điểm hệ thống:**
- Ưu: 6 điểm cụ thể (Fault isolation, Independent deployment, Tech diversity...)
- Nhược: 6 vấn đề thực tế với giải pháp tương lai (Jaeger, RabbitMQ, Prometheus...)

**Tổng điểm Chương 4: 9.5/10**

---

## VI. ĐÁNH GIÁ PHẦN FRONTEND (BONUS)

Phần frontend vượt yêu cầu cơ bản với **2 bộ giao diện hoàn chỉnh**:

**Light Theme (Bootstrap 5 + Inter):**
- 5 trang đầy đủ chức năng
- Ảnh Unsplash thật cho 17 sản phẩm
- Chatbot với lịch sử persistent
- Giỏ hàng riêng theo user_id

**Dark Glassmorphism Theme (Space Grotesk + backdrop-filter):**
- 5 trang tương ứng (`-dark.html`)
- Glass cards với `backdrop-filter: blur(20px)`
- Neon gradient accent (violet-cyan)
- Animated background radial gradient
- Nút switch qua lại giữa 2 theme

Điểm cộng đáng kể cho effort làm thêm giao diện thứ hai.

---

## VII. TỔNG KẾT ĐÁNH GIÁ

### Bảng điểm tổng hợp

| Chương | Tiêu chí | Điểm | Nhận xét |
|--------|---------|------|---------|
| **Ch.1** | Hình so sánh | 7.5/10 | ASCII, cần thêm đồ họa |
| | Bảng so sánh | 9.5/10 | Xuất sắc, đầy đủ 12 tiêu chí |
| | Big Tech | 9.5/10 | Số liệu cụ thể, phân tích sâu |
| | Micro vs Mono | 8.5/10 | Đủ kỹ thuật, thiếu code demo |
| | Healthcare DDD | 9.5/10 | Code thực tế, đúng pattern |
| **Ch.2** | Phân tích yêu cầu | 9.5/10 | 11 FR + 6 NFR đầy đủ |
| | Phân rã service | 8.0/10 | Cần thêm đồ họa |
| | Thiết kế service | 9.0/10 | Class diagram đầy đủ |
| | Django implementation | 9.5/10 | Code thực tế, chạy được |
| | Sequence/Activity | 9.0/10 | 7-actor sequence diagram |
| | Data Model | 8.0/10 | SQL schema tốt, thiếu ERD |
| **Ch.3** | Yêu cầu + Pipeline | 9.0/10 | 2 luồng rõ ràng |
| | Deep Learning | 9.5/10 | Cả theory + code 2 versions |
| | Code + giải thích | 9.0/10 | Có docstring, chú thích |
| | Dữ liệu thử nghiệm | 7.5/10 | 3 datasets nhỏ, đủ minh họa |
| | Kết quả so sánh | 8.0/10 | 4 metrics, thiếu validation |
| | Deploy | 8.5/10 | Dockerfile tối ưu |
| | RAG + tích hợp | 9.5/10 | Pipeline rõ, product cards |
| | Giao diện | 9.5/10 | Widget hoạt động thực tế |
| **Ch.4** | Kiến trúc + code | 9.5/10 | Cấu trúc thư mục đầy đủ |
| | Công nghệ | 9.5/10 | 15-row table với lý do |
| | Triển khai | 9.0/10 | Step-by-step, seed users |
| | Kết quả | 9.5/10 | 6 JSON responses thực tế |

**Điểm trung bình:** **9.0/10**

---

### Điểm mạnh nổi bật

1. **Code thực tế, chạy được** — Không chỉ lý thuyết, toàn bộ code Django/FastAPI có thể deploy ngay
2. **DDD áp dụng đúng** — Anti-Corruption Layer, Database-per-Service, Bounded Context thể hiện hiểu biết sâu
3. **nginx.conf production-grade** — Có DNS resolver động, rate limiting, CORS handling đúng chuẩn
4. **AI tích hợp thực tế** — Chatbot có history persistent, product cards với ảnh thật
5. **2 bộ giao diện** — Light và Dark Glassmorphism, có nút switch qua lại

### Điểm cần cải thiện

1. **Đồ họa** — Thay thế một số sơ đồ ASCII bằng hình vẽ thực từ draw.io/Visual Paradigm
2. **ERD Diagram** — Bổ sung Entity Relationship Diagram cho chương 2
3. **Test data validation** — Ghi rõ kết quả AI là simulated hay thực tế
4. **Knowledge Graph** — Đề cập nhưng chưa implement Neo4j
5. **Monitoring** — Bổ sung phần Prometheus + Grafana cho chương 4

### Nhận xét cuối

Tiểu luận thể hiện **sự hiểu biết toàn diện về kiến trúc Microservices** từ lý thuyết (DDD, Bounded Context) đến thực hành (Django code, Docker deployment). Phần AI được tích hợp tự nhiên vào hệ thống E-Commerce với pipeline rõ ràng. Điểm nổi bật nhất là **toàn bộ hệ thống có thể chạy thực tế** bằng một lệnh `docker compose up` — điều ít tiểu luận nào đạt được.

**Kết luận: Tiểu luận đạt chất lượng tốt, xứng đáng điểm A.**

---

*Bài đánh giá được thực hiện dựa trên các tiêu chí của môn SoAD — Kiến trúc và Thiết kế Phần mềm.*
*Ngày đánh giá: 12/05/2026*
