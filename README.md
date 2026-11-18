# AI-chat 命令行聊天工具

一个基于 DeepSeek API 的命令行 AI 聊天工具，支持多轮对话、Token 用量统计和聊天记录保存。

## 功能

- 多轮对话（自动携带最近 10 轮上下文）
- Token 用量实时统计与累加
- 聊天记录保存为 JSON 文件
- API 异常保护（网络错误不中断会话）
- 支持 `/help` `/stats` `/save` `/clear` `/quit` 命令

## 环境要求

- Python 3.10 或更高版本
- 一个 DeepSeek API Key（[获取地址](https://platform.deepseek.com/api_keys)，需账户有余额）

## 安装

```bash
# 1. 克隆仓库
git clone https://github.com/你的用户名/你的仓库名.git
cd 你的仓库名

# 2. 创建并激活虚拟环境
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt
```

## 配置 API Key

复制示例配置文件：

```bash
cp .env.example .env          # macOS / Linux
copy .env.example .env        # Windows
```

编辑 `.env`，填入你自己的 Key：

```
DEEPSEEK_API_KEY=sk-你的真实密钥
```

也可以不建 `.env`，运行时程序会提示你输入（输入内容不回显）。

## 运行

```bash
python AI_chat.py
```

## 可用命令

| 命令     | 作用                                           |
| -------- | ---------------------------------------------- |
| `/help`  | 查看帮助                                       |
| `/stats` | 查看本次会话 Token 用量                        |
| `/save`  | 把当前聊天记录存为 `conversations/chat-*.json` |
| `/clear` | 清空当前会话                                   |
| `/quit`  | 退出程序 直接按q也可以                         |

## 项目结构

```
.
├── AI-chat.py            # 主程序
├── .env.example          # 环境变量示例（不含真实密钥）
├── requirements.txt      # 依赖清单
├── conversations/        # 保存的聊天记录（自动创建，不提交）
└── README.md
```

## 费用说明

调用 DeepSeek API 按 Token 计费，本工具不提供免费额度。使用前请查看
[DeepSeek 官方定价](https://api-docs.deepseek.com/quick_start/pricing/)。

## 许可证

MIT License，详见 [LICENSE](LICENSE)。
