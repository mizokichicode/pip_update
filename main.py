"""pip update (main)"""

import platform
import sys
from subprocess import PIPE, CalledProcessError, run

sys.dont_write_bytecode = True


def _get_python_exe(python_version):
    """pythonランタイムのファイル名取得
    Returns
    -------
    (bool, str) : tuple
        bool : プラットフォーム判定結果
            True : macOS, Windows
            False: その他
        str : Pythonランタイムファイル名
    """
    match platform.system():
        case 'Windows':
            return (True, f'py -{python_version}')
        case 'Darwin':
            return (True, f'python{python_version}')
        case _:
            return (False, '')


def _update(python_exe):
    """更新パッケージ情報取得

    Parameters
    ----------
    python_exe : str
        Pythonランタイムファイル名

    Returns
    -------
    (result, pkgs) : tuple
        更新パッケージ情報リスト
    """
    try:
        # コマンドライン作成
        arg = f'{python_exe} -m pip list -o'.split()

        # コマンド実行
        ret = run(arg, stdout=PIPE, stderr=PIPE, check=True)

        # 標準出力の情報取得
        pkgs = [row for row in ret.stdout.decode().split('\n') if row]

        # 更新パッケージ情報取得
        if pkgs:
            pkgs = [tuple(row.split()) for row in pkgs[2:]]
        return (True, pkgs)
    except (
        FileNotFoundError,
        CalledProcessError,
    ):
        return (False, [])


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

        try:
            # コマンド実行
            _ = run(arg, stdout=PIPE, stderr=PIPE, check=True)
            print(f'OK ({info[1]} → {info[2]})')
        except CalledProcessError:
            print('NG')


def main():
    """メインメソッド"""
    # 初期化
    python_versions = [
        '3.15',  # End of support: 2031-10
        '3.14',  # End of support: 2030-10
        '3.13',  # End of support: 2029-10
        '3.12',  # End of support: 2028-10
        '3.11',  # End of support: 2027-10
    ]

    # パッケージ更新
    for python_version in python_versions:
        # pythonランタイムファイル名取得
        ret, python_exe = _get_python_exe(python_version)

        if not ret:
            print('macOS、またはWindowsで実行してください')
            break

        # 更新パッケージ情報取得
        ret, pkgs = _update(python_exe)

        if not ret:
            continue

        # 更新パッケージのインストール
        print(f'Ver.{python_version}')

        if pkgs:
            # パッケージの更新
            _upgrade(python_exe, pkgs)
        else:
            print('  更新パッケージなし')
        print()


if __name__ == '__main__':
    main()
