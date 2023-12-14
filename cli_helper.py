from base_chat import BaseChat
from path_structure import get_tree
import os
import json
import subprocess

os_name = 'linux' if os.name == 'posix' else 'windows'


class CliHelper(BaseChat):
    def __init__(self):
        super().__init__()
        self.main_path = os.getcwd()

    def chat(self, message):
        wrap_message = {
            "role": "user",
            "content": f"当前的项目结构是这样：{self.project_structure}\n" + message
        }
        self.history.append(wrap_message)

        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=self.history,
            response_format={"type": "json_object"}
        )

        response = json.loads(completion.choices[0].json())["message"]['content']
        self.history.append({"role": "assistant", "content": response})
        return response

    @property
    def project_structure(self):
        return get_tree(self.main_path)

    def execute(self, command):
        if command.startswith('echo'):
            command = command.replace('\n', '^r^n')
            command = command.replace('^r^n', '\r\n')
        if command == 'ls':
            return self.project_structure
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
            return f"成功！结果是{output}" if output else "成功！"
        except subprocess.CalledProcessError as e:
            return f"运行{command}时出错：{e.output}"


if __name__ == '__main__':
    helper = CliHelper()


    while True:
        message = input(">>> ")
        response = helper.chat(message)
        # print(response)
        try:
            print(json.loads(response)[os_name])
        except:
            print("模型输出格式错误，尝试重新回答问题。")
            wrong_handler = "你没有按照指定格式输出，请重新回答问题，不要说多余的话，按照json格式返回答案。" + message
            response = helper.chat(wrong_handler)
        execute_permission = input("是否执行？(y/n)")
        if execute_permission == 'y':
            print(helper.execute(json.loads(response)[os_name]))


