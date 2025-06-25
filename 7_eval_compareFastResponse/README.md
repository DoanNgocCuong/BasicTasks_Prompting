# Fast Response Evaluation System

Hệ thống đánh giá hiệu suất Fast Response API cho chatbot conversations.

## 📁 Cấu trúc Files

### Core Files
- **`main.py`** - File điều phối chính, orchestrate toàn bộ pipeline
- **`get_data_conversation.py`** - Lấy dữ liệu conversation từ API
- **`run_eval_api_fast_response.py`** - Gọi Fast Response API và đo response time
- **`requirements.txt`** - Dependencies cần thiết

### Processing Files (2 versions)
- **`processed_v1_1History.py`** - Version 1: Xử lý conversation với lịch sử ngắn (chỉ conversation gần nhất)
- **`processed_v2_fullHistory_CKP.py`** - Version 2: Xử lý conversation với full history (toàn bộ lịch sử từ đầu)

## 🚀 Cài đặt & Sử dụng

### Cài đặt
```bash
pip install -r requirements.txt
```

### Chạy pipeline
```bash
# Với IDs cụ thể
python main.py --ids 358 359 362 --token YOUR_API_TOKEN

# Với file chứa IDs
python main.py --id_file ids.txt --token YOUR_API_TOKEN

# Test mode (IDs mặc định)
python main.py
```

## 📊 Output Examples

### 🔹 Version 1 (v1_1History) - Context ngắn
Mỗi conversation chỉ chứa context gần nhất từ lần tương tác cuối.

**Input JSON:**
```json
{
  "data": [
    {"character": "BOT_RESPONSE_CONVERSATION", "content": "Xin chào!"},
    {"character": "USER", "content": "Hello"},
    {"character": "BOT_RESPONSE_CONVERSATION", "content": "Bạn cần gì?"},
    {"character": "USER", "content": "Tôi cần giúp đỡ"}
  ]
}
```

**Output Excel (Version 1):**
| BOT_RESPONSE_CONVERSATION_with_USER | FAST_RESPONSE_next | BOT_RESPONSE_CONVERSATION_next |
|---|---|---|
| `[{"role": "assistant", "content": "Xin chào!"}, {"role": "user", "content": "Hello"}]` | "" | "Bạn cần gì?" |
| `[{"role": "assistant", "content": "Bạn cần gì?"}, {"role": "user", "content": "Tôi cần giúp đỡ"}]` | "" | "" |

**→ 2 rows, mỗi row là 1 conversation độc lập**

---

### 🔹 Version 2 (v2_fullHistory_CKP) - Full context
Mỗi conversation chứa toàn bộ lịch sử từ đầu đến hiện tại.

**Same Input JSON**

**Output Excel (Version 2):**
| BOT_RESPONSE_CONVERSATION_with_USER | FAST_RESPONSE_next | BOT_RESPONSE_CONVERSATION_next |
|---|---|---|
| `[{"role": "assistant", "content": "Xin chào!"}, {"role": "user", "content": "Hello"}]` | "" | "Bạn cần gì?" |
| `[{"role": "assistant", "content": "Xin chào!"}, {"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Bạn cần gì?"}, {"role": "user", "content": "Tôi cần giúp đỡ"}]` | "" | "" |

**→ 2 rows, row 2 chứa toàn bộ lịch sử từ đầu**

---

### 📋 Complex Example

**Input JSON:**
```json
{
  "data": [
    {"character": "BOT_RESPONSE_CONVERSATION", "content": "Chào bạn!"},
    {"character": "USER", "content": "Hi"},
    {"character": "FAST_RESPONSE", "content": "Xin chào!"},
    {"character": "BOT_RESPONSE_CONVERSATION", "content": "Bạn cần gì?"},
    {"character": "USER", "content": "Tư vấn sản phẩm"},
    {"character": "FAST_RESPONSE", "content": "Để tôi giúp bạn!"},
    {"character": "BOT_RESPONSE_CONVERSATION", "content": "Bạn quan tâm loại nào?"}
  ]
}
```

### 🔹 Version 1 Output:
| BOT_RESPONSE_CONVERSATION_with_USER | FAST_RESPONSE_next | BOT_RESPONSE_CONVERSATION_next |
|---|---|---|
| `[{"role": "assistant", "content": "Chào bạn!"}, {"role": "user", "content": "Hi"}]` | "Xin chào!" | "Bạn cần gì?" |
| `[{"role": "assistant", "content": "Bạn cần gì?"}, {"role": "user", "content": "Tư vấn sản phẩm"}]` | "Để tôi giúp bạn!" | "Bạn quan tâm loại nào?" |

### 🔹 Version 2 Output:
| BOT_RESPONSE_CONVERSATION_with_USER | FAST_RESPONSE_next | BOT_RESPONSE_CONVERSATION_next |
|---|---|---|
| `[{"role": "assistant", "content": "Chào bạn!"}, {"role": "user", "content": "Hi"}]` | "Xin chào!" | "Bạn cần gì?" |
| `[{"role": "assistant", "content": "Chào bạn!"}, {"role": "user", "content": "Hi"}, {"role": "assistant", "content": "Bạn cần gì?"}, {"role": "user", "content": "Tư vấn sản phẩm"}]` | "Để tôi giúp bạn!" | "Bạn quan tâm loại nào?" |

## 📊 Folder Structure

```
input/          # Raw JSON data
output/         # Processed Excel files  
eval/           # API evaluation results
final/          # Consolidated report
```

## 📋 Excel Columns

- **BOT_RESPONSE_CONVERSATION_with_USER** - Conversation history (JSON format)
- **FAST_RESPONSE_next** - Expected fast response
- **BOT_RESPONSE_CONVERSATION_next** - Next bot response
- **response_time** - API response time (ms)
- **generated_ai** - AI generated response

## 🔧 Khi nào dùng Version nào?

### ✅ Version 1 (v1_1History)
- **Ưu điểm:** Nhanh, ít token, phù hợp real-time
- **Nhược điểm:** Thiếu context dài
- **Sử dụng:** Fast response cần phản hồi tức thì

### ✅ Version 2 (v2_fullHistory_CKP)  
- **Ưu điểm:** Context đầy đủ, hiểu rõ ngữ cảnh
- **Nhược điểm:** Chậm hơn, nhiều token
- **Sử dụng:** Cần hiểu toàn bộ cuộc trò chuyện

## ⚡ Features

- ✅ Multi-ID processing
- ✅ Response time measurement  
- ✅ Excel consolidation with multiple sheets
- ✅ Error handling & backup files
- ✅ Progress tracking
- ✅ Comprehensive reporting