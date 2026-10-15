"""Call the installed Codex app's compile_latex_document through its MCP bridge.

Uses the same built-in compiler tool as the editor, never a terminal TeX engine.
Only the app pipe metadata is copied; credentials and app settings are untouched.
"""
from pathlib import Path
import json, os, select, subprocess, time, uuid

ROOT = Path(__file__).resolve().parents[2]
SERVER = Path(os.environ.get('CODEX_APP_TOOLS_SERVER',
    str(Path.home() / '.codex/plugins/cache/openai-bundled/codex-app-tools/0.1.5/server.mjs')))

def app_environment():
    env = os.environ.copy()
    if not env.get('CODEX_APP_TOOLS_PIPE_PATH'):
        raise RuntimeError('Set CODEX_APP_TOOLS_PIPE_PATH explicitly; use make pdf for a portable build')
    if not SERVER.is_file():
        raise RuntimeError('Set CODEX_APP_TOOLS_SERVER to the installed application bridge')
    return env


def main():
    env = app_environment()
    thread = env.get('CODEX_THREAD_ID')
    if not thread:
        raise RuntimeError('Missing current thread context')
    process = subprocess.Popen(['node', str(SERVER)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True, env=env)
    def request(item, timeout=30):
        process.stdin.write(json.dumps(item) + '\n')
        process.stdin.flush()
        end = time.monotonic() + timeout
        while time.monotonic() < end:
            if not select.select([process.stdout], [], [], 1)[0]:
                continue
            line = process.stdout.readline()
            if not line:
                raise RuntimeError('Native MCP bridge closed')
            result = json.loads(line)
            if result.get('id') == item['id']:
                return result
        raise TimeoutError('Native compilation response timed out')
    try:
        init = request({'jsonrpc':'2.0', 'id':1, 'method':'initialize', 'params':{
            'protocolVersion':'2024-11-05','capabilities':{},
            'clientInfo':{'name':'manuscript-native-compiler','version':'1'}}})
        if 'error' in init:
            raise RuntimeError(init['error'])
        process.stdin.write(json.dumps({'jsonrpc':'2.0','method':'notifications/initialized'}) + '\n')
        process.stdin.flush()
        catalog = request({'jsonrpc':'2.0','id':2,'method':'tools/list','params':{}})
        available = catalog.get('result', {}).get('tools', [])
        if not any(x['name'] == 'compile_latex_document' for x in available):
            raise RuntimeError('The native compile tool is not available')
        result = request({'jsonrpc':'2.0','id':3,'method':'tools/call','params':{
            'name':'compile_latex_document','arguments':{'path':str(ROOT / 'china-capital-2026.tex')},
            '_meta':{'openai/threadId':thread,'openai/toolCallId':'manuscript-' + str(uuid.uuid4())}}}, 300)
        (ROOT / 'research/native_compile_result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
        for item in result.get('result', {}).get('content', []):
            if item.get('type') == 'text':
                try:
                    data = json.loads(item['text'])
                except ValueError:
                    print(item['text'][:4000], flush=True)
                    continue
                print(json.dumps({k:v for k,v in data.items() if k != 'diagnostics'}, ensure_ascii=False), flush=True)
                diagnostics = data.get('diagnostics', {})
                if diagnostics:
                    print(str(diagnostics)[-4000:], flush=True)
        if 'error' in result:
            print(json.dumps(result['error'], ensure_ascii=False), flush=True)
    finally:
        process.terminate()

if __name__ == '__main__':
    main()
