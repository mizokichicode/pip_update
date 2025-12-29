"""pip update
"""
import platform
from subprocess import run, PIPE
import sys
sys.dont_write_bytecode = True

def _get_python_exe(python_version):
    """pythonランタイムのファイル名取得
    """
    if platform.system() == 'windows':
        return f'py -{python_version}'
    return f'python{python_version}'


def _update(python_exe_name):
    """更新パッケージ情報取得
    
    Parameters
    ----------
    python_exe_name : str
        Pythonランタイムファイル名
    
    Returns
    -------
    list
        更新パッケージ情報リスト
    """
    # コマンドライン作成
    arg = f'{python_exe_name} -m pip list -o'.split()

    # コマンド実行
    ret = run(arg, stdout=PIPE, stderr=PIPE, check=False)
    if ret and ret.returncode == 0:
        # 標準出力の情報取得
        rows = [row for row in ret.stdout.decode().split('\n') if row]

        # 更新パッケージ情報取得
        if rows:
            return [row.split()[0] for row in rows[2:]]
    return []


def _upgrade(python_exe_name, pkgs):
    """更新パッケージのインストール
    
    Parameters
    ----------
    python_exe_name : str
        Pythonランタイムのファイル名
    pkgs : list
        更新パッケージリスト
    """
    for i, name in enumerate(pkgs, start=1):
        print(f'{i:3d}: {name:<32} ... ', end='', flush=True)

        # コマンドライン作成
        arg = f'{python_exe_name} -m pip install -U {name}'.split()

        # コマンド実行
        ret = run(arg, stdout=PIPE, stderr=PIPE, check=False)

        # 結果表示
        if ret and ret.returncode == 0:
            print('OK')
        else:
            print('NG')
    print()


def main():
    """メインメソッド
    """
    # 初期化
    python_versions = ['3.14', '3.13']

    # パッケージ更新
    for python_version in python_versions:
        print(f'Ver.{python_version:<10} ', end='', flush=True)

        # Pythonランタイムファイル名取得
        python_exe_name = _get_python_exe(python_version)

        # 更新パッケージ情報取得
        pkgs = _update(python_exe_name)

        # 更新パッケージ数表示
        print(f'(更新: {len(pkgs)})')

        # 更新パッケージのインストール
        if pkgs:
            _upgrade(python_exe_name, pkgs)


if __name__ == '__main__':
    main()
