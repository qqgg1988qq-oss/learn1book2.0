#!/usr/bin/env python3
"""
批量生成梵高视频场景图片
- 输入: van_gogh_visual_prompts.json
- 模式: unlimited（不消耗积分）
- 输出: 每个场景独立目录，已生成的跳过
"""
import json
import os
import sys
import time

# 加载 LovartClient
SKILL_DIR = "/Users/chouchou/.claude/skills/lovart-image/scripts"
sys.path.insert(0, SKILL_DIR)
from generate import LovartClient, AgentSkillError

# 生成模式：fast=用积分快速 / thinking=用积分深度推理 / unlimited=排队不消耗积分
MODE = os.environ.get("LOVART_MODE", "fast")
AUTO_CONFIRM = os.environ.get("LOVART_AUTO_CONFIRM", "1") == "1"

# 路径
PROMPTS_JSON = "/Users/chouchou/Documents/Obsidian Vault/成长计划/博客/van_gogh_visual_prompts.json"
OUTPUT_ROOT = "/Users/chouchou/Documents/Obsidian Vault/成长计划/博客/van_gogh_images"
STATE_FILE = os.path.join(OUTPUT_ROOT, "_progress.json")

os.makedirs(OUTPUT_ROOT, exist_ok=True)


def load_state():
    if os.path.exists(STATE_FILE):
        try:
            return json.load(open(STATE_FILE, "r", encoding="utf-8"))
        except Exception:
            pass
    return {"project_id": "", "completed": {}, "failed": {}}


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def main():
    data = json.load(open(PROMPTS_JSON, "r", encoding="utf-8"))
    global_style = data["meta"].get("global_style_prompt", "")
    scenes = data["prompts"]

    state = load_state()
    client = LovartClient(timeout=600, poll_interval=5)

    # 复用或创建 project
    project_id = state.get("project_id")
    if not project_id:
        project_id = client.create_project()
        state["project_id"] = project_id
        save_state(state)
        print(f"[INFO] 创建 project: {project_id}")
        try:
            client.rename_project(project_id, "梵高嫂子-视频分镜")
        except Exception:
            pass
    else:
        print(f"[INFO] 复用 project: {project_id}")

    total = len(scenes)
    for idx, scene in enumerate(scenes, 1):
        sid = scene["scene_id"]
        title = scene["title"]
        scene_dir = os.path.join(OUTPUT_ROOT, f"scene_{sid:02d}")
        key = str(sid)

        # 跳过已完成的场景
        if key in state.get("completed", {}):
            existing = state["completed"][key].get("files", [])
            if existing and all(os.path.exists(p) for p in existing):
                print(f"[SKIP] 场景 {sid:02d} ({title}) 已完成，跳过")
                continue

        # 跳过已经有图片文件存在的场景
        if os.path.isdir(scene_dir):
            existing_imgs = [
                f for f in os.listdir(scene_dir)
                if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
            ]
            if existing_imgs:
                files = [os.path.join(scene_dir, f) for f in existing_imgs]
                state.setdefault("completed", {})[key] = {
                    "title": title, "files": files
                }
                save_state(state)
                print(f"[SKIP] 场景 {sid:02d} 已有图片 ({len(existing_imgs)} 张)，跳过")
                continue

        # 组合 prompt：静态化指令 + 全局风格 + 场景描述
        STATIC_PREFIX = (
            "请生成一张【静态图片】（PNG，1张），不要生成视频，不要使用视频工具或动画工具。"
            "下面的'镜头推近''缓慢移动''逐渐浮现'等只是构图意图参考，最终输出必须是单帧静态图。"
            "请使用图像生成工具（如 GPT Image / Midjourney / Flux），不要使用 generate_media 视频工具。"
        )
        full_prompt = f"{STATIC_PREFIX}\n\n{global_style}。{scene['prompt']}"

        print(f"\n{'='*60}")
        print(f"[{idx}/{total}] 生成场景 {sid:02d}: {title}")
        print(f"[INFO] 输出目录: {scene_dir}")
        print(f"{'='*60}")

        try:
            result = client.generate(
                prompt=full_prompt,
                project_id=project_id,
                mode=MODE,
                timeout=900,
                output_dir=scene_dir,
                auto_create_project=False,
            )

            # 自动确认 pending_confirmation —— 仅限图片工具，视频/媒体类拒绝
            if result.get("status") == "pending_confirmation":
                tid = result.get("thread_id")
                pc = result.get("pending_confirmation", {})
                tool_name = (pc.get("tool_name") or "").lower()
                cost = pc.get("estimated_cost", 0)

                # 黑名单：视频 / 媒体 / 音频
                BLOCKED = ["video", "media", "audio", "music", "voice", "sound"]
                is_blocked = any(b in tool_name for b in BLOCKED)
                # 仅允许明确的图片工具或低成本 (<10 积分)
                is_image = "image" in tool_name or "img" in tool_name or "picture" in tool_name

                if is_blocked or (not is_image and cost > 10):
                    print(f"[REJECT] 拒绝 {tool_name} (cost={cost})，跳过该场景")
                    state.setdefault("failed", {})[key] = {
                        "title": title,
                        "status": "rejected_non_image_tool",
                        "warning": f"拒绝非图片工具 {tool_name} (cost={cost})",
                        "thread_id": tid,
                    }
                    save_state(state)
                    time.sleep(3)
                    continue

                print(f"[CONFIRM] 自动确认图片工具 {tool_name} (cost={cost}): {tid}")
                try:
                    client.confirm(tid)
                except Exception as e:
                    print(f"[CONFIRM-ERR] {e}")
                status = client.poll(tid, timeout=900, verbose=True)
                print(f"[CONFIRM-DONE] status={status}")
                if status == "done":
                    result2 = client.get_result(tid)
                    result2["thread_id"] = tid
                    result2["project_id"] = project_id
                    result2["status"] = status
                    has_artifact = any(
                        (it.get("artifacts") or [])
                        for it in (result2.get("items") or [])
                    )
                    result2["generation_succeeded"] = has_artifact
                    if has_artifact:
                        result2["downloaded"] = client.download_artifacts(result2, output_dir=scene_dir)
                    else:
                        result2["downloaded"] = []
                    result = result2
        except AgentSkillError as e:
            print(f"[ERROR] 场景 {sid:02d} 失败: {e.message} (code={e.code})")
            state.setdefault("failed", {})[key] = {
                "title": title, "error": e.message
            }
            save_state(state)
            time.sleep(10)
            continue
        except Exception as e:
            print(f"[ERROR] 场景 {sid:02d} 异常: {e}")
            state.setdefault("failed", {})[key] = {
                "title": title, "error": str(e)
            }
            save_state(state)
            time.sleep(10)
            continue

        downloaded = result.get("downloaded", [])
        files = [d["local_path"] for d in downloaded if d.get("local_path")]
        status = result.get("status", "unknown")
        success = result.get("generation_succeeded", bool(files))

        if success and files:
            state.setdefault("completed", {})[key] = {
                "title": title,
                "files": files,
                "thread_id": result.get("thread_id"),
            }
            # 移除 failed 记录
            state.get("failed", {}).pop(key, None)
            print(f"[OK] 场景 {sid:02d} 完成，{len(files)} 张图：")
            for fp in files:
                print(f"  → {fp}")
        else:
            warning = result.get("warning") or status
            state.setdefault("failed", {})[key] = {
                "title": title,
                "status": status,
                "warning": warning,
                "agent_message": result.get("agent_message", ""),
                "thread_id": result.get("thread_id"),
            }
            print(f"[WARN] 场景 {sid:02d} 无产出: {warning}")

        save_state(state)

        # 场景间稍作停顿，避免触发限流
        time.sleep(5)

    # 汇总
    print(f"\n{'='*60}")
    print("批量生成完毕")
    print(f"  ✓ 完成: {len(state.get('completed', {}))} / {total}")
    print(f"  ✗ 失败: {len(state.get('failed', {}))}")
    print(f"  状态文件: {STATE_FILE}")


if __name__ == "__main__":
    main()
