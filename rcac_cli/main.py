import sys
import argparse
from rcac_cli.client.api import chat
from rcac_cli.config import set_api_key, ensure_api_key
from rcac_cli.tool_schemas import TOOLS_SCHEMA, execute_tool
import json

def print_stream(generator):
    """Print streaming tokens from the API response and collect tool calls."""
    collected_content = ""
    tool_calls = {}
    
    for chunk in generator:
        try:
            delta = chunk.get('choices', [{}])[0].get('delta', {})
            content = delta.get('content', '')
            if content:
                sys.stdout.write(content)
                sys.stdout.flush()
                collected_content += content
                
            if 'tool_calls' in delta:
                for tc in delta['tool_calls']:
                    idx = tc['index']
                    if idx not in tool_calls:
                        tool_calls[idx] = {"id": tc.get("id"), "type": "function", "function": {"name": tc["function"].get("name", ""), "arguments": ""}}
                    if "function" in tc and "arguments" in tc["function"]:
                        tool_calls[idx]["function"]["arguments"] += tc["function"]["arguments"]
        except Exception:
            continue
    print()  # final newline
    
    msg = {"role": "assistant"}
    if collected_content:
        msg["content"] = collected_content
    else:
        msg["content"] = ""
    if tool_calls:
        msg["tool_calls"] = [tool_calls[i] for i in sorted(tool_calls.keys())]
    return msg

SYSTEM_PROMPT = {
    "role": "system", 
    "content": """You are a powerful autonomous agentic coding assistant running directly in the user's terminal. 
You have access to local tools to explore the filesystem, read/write code, and run shell commands.

CRITICAL INSTRUCTIONS:
1. Do NOT just print tutorials, instructions, or markdown blocks of code for the user to copy-paste.
2. You MUST take action on behalf of the user. If they ask you to create a project, write a file, or run a command, use your `write_file` and `run_command` tools to do it for them autonomously.
3. Your `run_command` tool runs in a non-interactive environment. You MUST use non-interactive flags (e.g. -y, --yes) for commands like npm, apt, pip, etc. Never run commands that block waiting for user input, or the system will hang."""
}

def chat_interactive():
    ensure_api_key()
    print("Welcome to RCAD Qwen CLI. Type 'exit' or 'quit' to leave.")
    history = [SYSTEM_PROMPT]
    while True:
        try:
            user_input = input('rcac> ')
        except (EOFError, KeyboardInterrupt):
            print('\nExiting.')
            break
        if user_input.strip().lower() in {'exit', 'quit'}:
            print('Goodbye!')
            break
        if not user_input.strip():
            continue
        history.append({"role": "user", "content": user_input})
        
        while True:
            try:
                response_gen = chat(history, stream=True, tools=TOOLS_SCHEMA)
                msg = print_stream(response_gen)
                history.append(msg)
                
                if "tool_calls" in msg and msg["tool_calls"]:
                    for tc in msg["tool_calls"]:
                        func_name = tc["function"]["name"]
                        try:
                            args = json.loads(tc["function"]["arguments"])
                        except json.JSONDecodeError:
                            args = {}
                        
                        print(f"\n[Tool Calling] Executing: {func_name}")
                        result = execute_tool(func_name, args)
                        
                        history.append({
                            "role": "tool",
                            "tool_call_id": tc["id"],
                            "content": result
                        })
                    # loop again to send tool results to the model
                    continue
                else:
                    break # no tools called, wait for next user input
            except Exception as e:
                print(f"Error: {e}")
                break

def run_repl():
    """Start the REPL loop directly."""
    chat_interactive()


def _handle_cli_args():
    parser = argparse.ArgumentParser(prog='rcac', description='RCAC Qwen CLI')
    subparsers = parser.add_subparsers(dest='subcommand')

    # repl subcommand
    repl_parser = subparsers.add_parser('repl', help='Start the interactive REPL')
    repl_parser.add_argument('--no-confirm', action='store_true', help='Skip confirmation prompts (useful for automation)')

    # set-key subcommand
    setkey_parser = subparsers.add_parser('set-key', help='Set API key')
    setkey_parser.add_argument('value', help='API key value')

    args = parser.parse_args()
    if args.subcommand == 'set-key':
        set_api_key(args.value)
        print('API key saved to config.json')
        sys.exit(0)
    elif args.subcommand == 'repl':
        # Pass flag to REPL if needed (future extension)
        run_repl()
    else:
        # default to REPL when no subcommand provided
        run_repl()

if __name__ == '__main__':
    _handle_cli_args()
