prompt = """
[系统设定]
你是一个人工智能驱动的操作系统，你的目标是通过理解需求、编写代码、运行代码来实现用户的目标。

[资源列表]
你拥有一台完全权限的本地桌面环境，并且已经预装了python和node。

[工作流]
1.理解用户的需求
2.获取并分析当前工作目录中的结构和文件
3.根据需求创建或修改文件
4.通过 PowerShell 执行git命令将代码提交到github

[回答规范]
你的回答风格简洁概括的,除非用户要求详细输出.
当你打开一个文件时,你不需要向用户重复文件的内容,只需要大概描述一下即可.
当你写入文件时,你不需要向用户重复你写入的内容,只需要大概介绍一下即可.
当你读取文件时,读取的编码采用的是UTF-8.

"""

tools = [
    {
        "type": "function",
        "function": {
            "name": "write_to_file",
            "description": "Write data to a local file",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "The data to write to the file"
                    },
                    "filename": {
                        "type": "string",
                        "description": "The name of the file to write to",
                    },
                    "directory": {
                        "type": "string",
                        "description": "The directory where the file will be written. Defaults to the current directory",
                    }
                },
                "required": ["data", "filename","directory"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_from_file",
            "description": "Read data from a local file",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The name of the file to read from",
                    },
                    "directory": {
                        "type": "string",
                        "description": "The directory where the file is located. Defaults to the current directory",
                    }
                },
                "required": ["filename","directory"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_directory_structure",
            "description": "Get the directory structure of the specified directory, defaulting to the current directory",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "The directory to get the structure of. Defaults to the current directory",
                    }
                },
                "required": ["directory"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_powershell_command",
            "description": "Run a PowerShell command in the specified directory, defaulting to the current directory",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The PowerShell command to execute"
                    },
                    "directory": {
                        "type": "string",
                        "description": "The directory to run the command in. Defaults to the current directory",
                    }
                },
                "required": ["command","directory"]
            }
        }
    }
]
