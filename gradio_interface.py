import gradio as gr
from cli_helper import CliHelper
import json
import os

os_name = 'linux' if os.name == 'posix' else 'windows'
helper = CliHelper()

def update_file_tree():
    return helper.project_structure

def chat(message):
    response = helper.chat(message)
    command = json.loads(response).get(os_name, "")
    return command, command, response

def execute(command):
    if command:
        result = helper.execute(command)
    else:
        result = "命令未执行。"
    file_tree = update_file_tree()
    return result, file_tree

def init():
    return update_file_tree()

with gr.Blocks() as app:
    gr.Markdown("### 命令行助手")
    gr.Markdown("在下面的框中输入命令，获取执行命令。再确认是否执行。")
    with gr.Row():
        message_input = gr.Textbox(label="输入您的命令", lines=2, placeholder="比如：请删除这个文件夹")
        chat_button = gr.Button("获取命令")
    chat_response_output = gr.Text(label="模型响应")
    command_output = gr.Text(label="解析后的命令")
    
    with gr.Row():
        execute_input = gr.Textbox(label="要执行的命令")
        execute_button = gr.Button("执行命令")
    with gr.Row():
        file_tree_output = gr.Textbox(label="当前目录结构", interactive=True, lines=20, readonly=True, value=init())
        execute_output = gr.Text(label="执行结果")

    chat_button.click(
        fn=chat,
        inputs=message_input,
        outputs=[command_output, execute_input, chat_response_output]
    )

    execute_button.click(
        fn=execute,
        inputs=[execute_input],
        outputs=[execute_output, file_tree_output]
    )

app.launch()
