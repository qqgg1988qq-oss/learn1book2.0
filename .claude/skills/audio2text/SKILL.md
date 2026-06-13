---
name: audio2text
description: |
  讯飞语音转写大模型 API 封装 Skill。将音频文件（MP3/WAV/MP4 等）异步转写为文本，支持中英 + 202 种方言免切换识别。

  触发场景：
  - "帮我把这段音频转成文字"
  - "语音转写这个文件"
  - "转录这个录音"
  - 任何需要将音频文件转为文字文本的请求

  输出：结构化的转写文本，按句子分段并附带时间戳
---

# Audio2Text — 讯飞语音转写大模型

## 工作流程

```
用户指定音频文件
    ↓
步骤1: /v2/upload — 上传音频文件，获取 orderId
    ↓
轮询等待转写完成
    ↓
步骤2: /v2/getResult — 通过 orderId 查询转写结果
    ↓
解析并输出结构化文本
```

**注意**：讯飞 API 是异步流程，上传后需要轮询等待转写完成（status=4 表示完成）。

## 快速开始

### 环境变量配置

将以下密钥存入项目环境变量（切勿硬编码在代码中）：

```bash
export XF_APPID="your-appid"
export XF_API_KEY="your-apikey"
export XF_API_SECRET="your-apisecret"
```

### 使用方式

```
/audio2text ./recording.mp3
/audio2text ./meeting.wav --language autodialect
/audio2text ./interview.mp4 --role-type 1 --role-num 2
```

## Python 调用示例

```python
import os, json, time, base64, hmac, hashlib, urllib.parse
from datetime import datetime, timezone, timedelta
import requests

API_URL = "https://office-api-ist-dx.iflyaisol.com"


def load_dotenv(filepath=".env"):
    """极简 .env 文件解析器，无需第三方库"""
    if not os.path.exists(filepath):
        return
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                os.environ.setdefault(key, value)


# 加载项目根目录的 .env（已加入 .gitignore，不会提交）
load_dotenv(".env")

APPID = os.environ.get("XF_APPID", "")
API_KEY = os.environ.get("XF_API_KEY", "")
API_SECRET = os.environ.get("XF_API_SECRET", "")

if not all([APPID, API_KEY, API_SECRET]):
    raise RuntimeError("环境变量未设置。请创建 .env 文件或手动设置 XF_APPID / XF_API_KEY / XF_API_SECRET")


def generate_signature(secret, params):
    """基于 HMAC-SHA1 生成签名"""
    sorted_params = dict(sorted(params.items()))
    sorted_params.pop("signature", None)
    parts = []
    for k, v in sorted_params.items():
        if v is not None and v != "":
            parts.append(f"{k}={urllib.parse.quote(str(v), safe='')}")
    base_string = "&".join(parts)
    mac = hmac.new(secret.encode("utf-8"), base_string.encode("utf-8"), hashlib.sha1)
    return base64.b64encode(mac.digest()).decode("utf-8")

def build_url(base_path, params):
    """构建 URL（仅含查询参数，不含 signature）"""
    query_parts = []
    for k, v in params.items():
        query_parts.append(f"{k}={urllib.parse.quote(str(v), safe='')}")
    return f"{API_URL}{base_path}?" + "&".join(query_parts)

def upload_audio(file_path, language="autodialect"):
    """上传音频文件"""
    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)
    now = datetime.now(timezone(timedelta(hours=8)))
    date_time = now.strftime("%Y-%m-%dT%H:%M:%S") + now.strftime("%z")[:3] + now.strftime("%z")[3:]
    signature_random = os.urandom(8).hex()

    # URL 查询参数（不含 signature）
    url_params = {
        "appId": APPID,
        "accessKeyId": API_KEY,
        "dateTime": date_time,
        "signatureRandom": signature_random,
        "fileSize": str(file_size),
        "fileName": file_name,
        "language": language,
        "durationCheckDisable": "true",  # 跳过时长校验
    }

    # 计算签名（基于 url_params）
    sig = generate_signature(API_SECRET, url_params)

    url = build_url("/v2/upload", url_params)
    headers = {
        "Content-Type": "application/octet-stream",
        "signature": sig,  # signature 放在请求头中
    }

    with open(file_path, "rb") as f:
        resp = requests.post(url, data=f, headers=headers, timeout=120)
    return resp.json()

def get_result(order_id, result_type="transfer"):
    """查询转写结果（轮询）"""
    now = datetime.now(timezone(timedelta(hours=8)))
    date_time = now.strftime("%Y-%m-%dT%H:%M:%S") + now.strftime("%z")[:3] + now.strftime("%z")[3:]
    signature_random = os.urandom(8).hex()

    url_params = {
        "accessKeyId": API_KEY,
        "dateTime": date_time,
        "signatureRandom": signature_random,
        "orderId": order_id,
        "resultType": result_type,
    }

    sig = generate_signature(API_SECRET, url_params)

    url = build_url("/v2/getResult", url_params)
    headers = {
        "Content-Type": "application/json",
        "signature": sig,  # signature 放在请求头中
    }

    resp = requests.post(url, json={}, headers=headers, timeout=60)
    return resp.json()

def poll_until_done(order_id, interval=5, max_attempts=120):
    """轮询直到转写完成"""
    for i in range(max_attempts):
        result = get_result(order_id)
        order_info = result.get("content", {}).get("orderInfo", {})
        status = order_info.get("status")
        if status == 4:
            return result
        if status == -1:
            raise RuntimeError(f"Transcription failed: {order_info}")
        print(f"[{i+1}] Processing... status={status}, estimated={result['content'].get('taskEstimateTime', 'N/A')}ms")
        time.sleep(interval)
    raise TimeoutError("Polling timeout")

def extract_text(result_json):
    """从结果中提取纯文本"""
    order_result = result_json.get("content", {}).get("orderResult", "")
    if not order_result:
        return ""
    data = json.loads(order_result)
    sentences = []
    for item in data.get("lattice", []):
        best = json.loads(item.get("json_1best", "{}"))
        st = best.get("st", {})
        words = []
        for ws in st.get("rt", [{}])[0].get("ws", []):
            for cw in ws.get("cw", []):
                words.append(cw.get("w", ""))
        text = "".join(words)
        bg = st.get("bg", "")
        ed = st.get("ed", "")
        sentences.append(f"[{bg}ms -> {ed}ms] {text}")
    return "\n".join(sentences)

# 使用示例
if __name__ == "__main__":
    file_path = "./recording.mp3"
    upload_resp = upload_audio(file_path)
    order_id = upload_resp["content"]["orderId"]
    print(f"Uploaded. OrderId: {order_id}")

    final = poll_until_done(order_id)
    text = extract_text(final)
    print(text)
```

## 常用参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `language` | string | 是 | `autodialect`（中英+202方言）或 `autominor`（37语种） |
| `pd` | string | 否 | 领域参数：`court`/`finance`/`medical`/`tech`/`edu` 等 |
| `roleType` | int | 否 | `0`=不分离，`1`=通用角色分离，`3`=声纹角色分离 |
| `roleNum` | int | 否 | 说话人数 `0-10`，默认 `0` 盲分 |
| `eng_smoothproc` | bool | 否 | 顺滑开关，默认 `true` |
| `eng_colloqproc` | bool | 否 | 口语规整开关，默认 `false` |
| `audioMode` | string | 否 | `fileStream`（默认）或 `urlLink` |
| `callbackUrl` | string | 否 | 异步回调地址 |

## 音频要求

- **采样率**: 16kHz 或 8kHz
- **位长**: 16bit
- **声道**: 单声道
- **格式**: mp3, wav, pcm, mp4, m4a, aac, opus, flac, ogg, amr 等
- **大小**: 不超过 500MB，时长不超过 5 小时

## 关键实现细节

### 1. signature 必须放在请求头中

**错误做法**：把 signature 拼接到 URL 查询参数中。
**正确做法**：signature 通过 `headers={"signature": sig}` 传递，URL 查询参数中不包含 signature。

```python
# 正确
headers = {"Content-Type": "application/octet-stream", "signature": sig}
requests.post(url, data=file, headers=headers)

# 错误
url = f"...?signature={sig}"  # 服务器会返回 "signature is empty"
```

### 2. durationCheckDisable 跳过时长校验

上传接口默认需要 `duration` 参数（音频时长，毫秒）。如果无法精确获取音频时长，可传入 `durationCheckDisable=true` 跳过校验：

```python
url_params = {
    # ... 其他参数 ...
    "durationCheckDisable": "true",
}
```

否则必须传入准确的 duration，否则会报错 `duration is empty`。

## 注意事项

1. **API 密钥安全**：始终通过环境变量注入密钥，不要硬编码到代码或提交到 git
2. **签名时间窗口**：请求时间戳与服务器时间偏差不能超过一定范围，确保系统时钟准确
3. **轮询策略**：建议间隔 3-10 秒轮询，转写时长约为音频时长的 20%-50%
4. **空请求体**：`getResult` 接口需要传递 `{}` 作为请求体，不可省略
