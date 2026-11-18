#模块一：导入区
import os
import json
from pathlib import Path
from datetime import datetime
from getpass import getpass
#上面都是官方库，无需下载
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv

load_dotenv()   #读取.env里的配置

#模块二：常量区
MODEL = "deepseek-flash"

SYSTEM_PROMPT = (
    "你是一个面向编程初学者的 AI 教学助手。"
    "使用自然、准确的中文回答问题。"
    "解释技术概念时尽量提供简单示例。"
    "不编造不存在的技术信息。"
)

#模块三：类定义 
class RunoobChatBot:    #定义机器人蓝图

    def __init__(self):  #初始化 

        api_key = os.environ.get("DEEPSEEK_API_KEY")

        if not api_key:
            api_key = getpass("请输入 DeepSeek API Key：").strip()

        if not api_key:
            raise ValueError("没有提供 API Key")

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com",
            max_retries=2,
            timeout=60.0
        )

        self.messages = []

        self.input_tokens = 0
        self.output_tokens = 0

    def chat(self, question):   #发请求

        # 保留最近 6 轮完整对话
        recent_history = self.messages[-20:]

        request_messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ] + recent_history + [
            {
                "role": "user",
                "content": question
            }
        ]

        response = self.client.chat.completions.create(
            model=MODEL,
            messages=request_messages,
            extra_body={"thinking": {"type": "disabled"}},
        )

        answer = response.choices[0].message.content or ""

        # 成功后才保存本轮对话
        self.messages.append({
            "role": "user",
            "content": question
        })

        self.messages.append({
            "role": "assistant",
            "content": answer
        })

        if response.usage:
            self.input_tokens += response.usage.prompt_tokens
            self.output_tokens += response.usage.completion_tokens

        return answer #调用这个函数chat(I)后输出AI答复中用户需要的文本内容O

    def show_stats(self):   #查看统计数据

        print("\n=== 当前会话统计 ===")
        print("模型：", MODEL)
        print("对话轮数：", len(self.messages) // 2)
        print("输入 Token：", self.input_tokens)
        print("输出 Token：", self.output_tokens)
        print(
            "总 Token：",
            self.input_tokens + self.output_tokens
        )
        print("费用请以平台实际账单为准。\n")

    def save_history(self):     #保存聊天记录

        output_dir = Path("conversations")
        output_dir.mkdir(exist_ok=True)

        filename = (
            "chat-"
            + datetime.now().strftime("%Y%m%d-%H%M%S-%f")   #文件名精确到微秒，确保不会重名
            + ".json"
        )

        filepath = output_dir / filename

        data = {
            "model": MODEL,
            "saved_at": datetime.now().isoformat(),
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "messages": self.messages
        }

        filepath.write_text(
            json.dumps(
                data,
                ensure_ascii=False,  #中文原样输出
                indent=2    #indent缩进，界面更美观
            ),
            encoding="utf-8"
        )

        print("已保存到：", filepath)

    def clear(self):    #清空聊天记录

        self.messages.clear()

        self.input_tokens = 0
        self.output_tokens = 0

        print("当前会话已清空。")

#模块四：辅助函数
def print_help():   #为用户打印操作说明

    print("""
可用命令：

/help   查看帮助
/stats  查看 Token 用量
/save   保存当前聊天记录
/clear  清空当前会话
/quit,q 退出程序

直接输入文字即可与 AI 对话。
""")

#模块五：主流程（函数）
def main():     #流程逻辑

    print("AI-chat命令行聊天工具")

    bot = RunoobChatBot()   #按类定义的蓝图造一个实例机器人(bot)

    print_help()

    while True:

        try:
            question = input("我们：").strip()

            if not question:
                continue

            if question == "/quit":
                print("再见！")
                break

            if question == "q":
                print("再见！")
                break

            if question == "/help":
                print_help()
                continue

            if question == "/stats":
                bot.show_stats()
                continue

            if question == "/save":
                bot.save_history()
                continue

            if question == "/clear":
                bot.clear()
                continue

            if question == "/good":
                print('感谢支持，一键三连')
                continue

            print("AI思考中：", end="", flush=True)

            answer = bot.chat(question) #这里真正调用了聊天函数，并将返回值赋给同名变量

            print(answer)
            print()
#try里的执行出错了，直接跳到except，而不是直接崩溃
        except (KeyboardInterrupt, EOFError):
            print("\n程序已退出。")
            break

        except OpenAIError as error:
            print(
                "\nAPI 调用失败：",
                type(error).__name__
            )

        except Exception as error:
            raise

#模块六：入口守卫
if __name__ == "__main__":  #真正启动这个流程
    main()

#这等于说："只有在被直接运行时，才执行 main()
# 直接运行：  打印帮助、进入对话循环 
# 被 import： 什么都不会发生，只提供类和函数