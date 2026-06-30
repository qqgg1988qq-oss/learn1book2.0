# Audio2Text 使用模板

## 调用模板

用户请求格式：

```
/audio2text {音频文件路径} [--参数名 参数值]...
```

## 参数配置模板

```yaml
# 每次调用时根据需求填入
audio_file: "./path/to/audio.mp3"
language: "autodialect"          # autodialect | autominor
pd: ""                           # 领域: court/finance/medical/tech/edu...
roleType: 0                      # 0 | 1 | 3
roleNum: 0                       # 0-10
eng_smoothproc: true             # true | false
eng_colloqproc: false            # true | false
audioMode: "fileStream"          # fileStream | urlLink
callbackUrl: ""                  # 可选回调地址
output_format: "text"            # text | json | srt
```

## 输出格式模板

### text 格式

```
[0ms -> 1680ms] 喂你好。
[2390ms -> 3640ms] 请问是王先生吗？
[5130ms -> 7200ms] 是的，请问有什么事情？
...
```

### json 格式

```json
{
  "sentences": [
    {
      "text": "喂你好。",
      "begin": 0,
      "end": 1680,
      "role": 1
    }
  ],
  "duration": 11240,
  "orderId": "..."
}
```

### srt 格式（字幕）

```srt
1
00:00:00,000 --> 00:00:01,680
喂你好。

2
00:00:02,390 --> 00:00:03,640
请问是王先生吗？
```

## 错误处理检查清单

- [ ] 环境变量 `XF_APPID`、`XF_API_KEY`、`XF_API_SECRET` 已设置
- [ ] 音频文件存在且格式支持
- [ ] 系统时钟准确（签名时间戳校验）
- [ ] 轮询未超时（长音频可能需要更长时间）
- [ ] orderId 正确传递到了 getResult 接口
