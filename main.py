"""pip update (main)"""

import platform
import sys
from subprocess import run, PIPE

sys.dont_write_bytecode = True


def _get_python_exe(python_version):
    """pythonランタイムのファイル名取得"""
    if platform.system() == 'windows':
        return f'py -{python_version}'
    return f'python{python_version}'


def _update(python_exe):
    """更新パッケージ情報取得

    Parameters
    ----------
    python_exe : str
        Pythonランタイムファイル名

    Returns
    -------
    list
        更新パッケージ情報リスト
    """
    # コマンドライン作成
    arg = f'{python_exe} -m pip list -o'.split()

    # コマンド実行
    ret = run(arg, stdout=PIPE, stderr=PIPE, check=False)
    if ret and ret.returncode == 0:
        # 標準出力の情報取得
        rows = [row for row in ret.stdout.decode().split('\n') if row]

        # 更新パッケージ情報取得
        if rows:
            return [tuple(row.split()) for row in rows[2:]]
    return []


def _upgrade(python_exe, pkgs):
    """更新パッケージのインストール

    Parameters
    ----------
    python_exe : str
        Pythonランタイムのファイル名
    pkgs : list
        更新パッケージ情報リスト
    """
    total = len(pkgs)
    for num, info in enumerate(pkgs, start=1):
        print(f'{num:3d}/{total}: {info[0]:<32} ... ', end='', flush=True)

        # コマンドライン作成
        arg = f'{python_exe} -m pip install -U {info[0]}'.split()

        # コマンド実行
        ret = run(arg, stdout=PIPE, stderr=PIPE, check=False)

        # 結果表示
        if ret and ret.returncode == 0:
            print(f'OK ({info[1]} → {info[2]})')
        else:
            print('NG')


def main():
    """メインメソッド"""
    # 初期化
    python_versions = ['3.14']

    # パッケージ更新
    for python_version in python_versions:
        print(f'Ver.{python_version}')

        # pythonランタイムファイル名取得
        python_exe = _get_python_exe(python_version)

        # 更新パッケージ情報取得
        pkgs = _update(python_exe)

        if pkgs:
            # 更新パッケージのインストール
            _upgrade(python_exe, pkgs)
        else:
            print('  更新パッケージなし')
        print()


if __name__ == '__main__':
    main()
