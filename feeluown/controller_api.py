# -*- coding:utf8 -*-

import platform
import subprocess

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication


class ControllerApi(object):
    """暴露给plugin或者其他外部模块的接口和数据
    """
    notify_widget = None
    lyric_widget = None
    desktop_mini = None
    current_playlist_widget = None
    player = None
    network_manager = None
    api = None

    state = {"is_login": False,
             "current_mid": 0,
             "current_pid": 0,
             "platform": "",
             "other_mode": False}

    @classmethod
    def set_login(cls):
        cls.state['is_login'] = True
        cls.view.ui.LOVE_SONG_BTN.show()
        cls.view.ui.LOGIN_BTN.hide()

    @classmethod
    def play_mv_by_mvid(cls, mvid):
        mv_model = ControllerApi.api.get_mv_detail(mvid)
        if not ControllerApi.api.is_response_ok(mv_model):
            return

        url_high = mv_model['url_high']
        clipboard = QApplication.clipboard()
        clipboard.setText(url_high)

        if platform.system() == "Linux":
            ControllerApi.player.pause()
            ControllerApi.notify_widget.show_message("通知", "正在尝试调用VLC视频播放器播放MV")
            try:
                subprocess.Popen(['vlc', url_high, '--play-and-exit', '-f'])
            except FileNotFoundError:
                ControllerApi.notify_widget.show_message("Error", "VLC视频播放器未安装")
        elif platform.system().lower() == 'Darwin'.lower():
            ControllerApi.player.pause()
            cls.view.ui.STATUS_BAR.showMessage(u"准备调用 QuickTime Player 播放mv", 4000)
            try:
                subprocess.Popen(['open', '-a', 'QuickTime Player', url_high])
            except FileNotFoundError:
                ControllerApi.notify_widget.show_message("Error", "QuickTime Player未安装")
        else:
            cls.view.ui.STATUS_BAR.showMessage(u"程序已经将视频的播放地址复制到剪切板", 5000)

    @classmethod
    def toggle_lyric_widget(cls):
        if ControllerApi.lyric_widget.isVisible():
            ControllerApi.lyric_widget.close()
        else:
            ControllerApi.lyric_widget.show()

    @classmethod
    def toggle_desktop_mini(cls):
        if ControllerApi.desktop_mini.isVisible():
            ControllerApi.desktop_mini.close()
        else:
            ControllerApi.desktop_mini.show()
            ControllerApi.notify_widget.show_message("Tips", "按ESC可以退出mini模式哦 ~")

    @classmethod
    @pyqtSlot(int)
    def seek(cls, seconds):
        cls.player.setPosition(seconds * 1000)

    @classmethod
    def play_specific_song_by_mid(cls, mid):
        song = ControllerApi.api.get_song_detail(mid)
        if not ControllerApi.api.is_response_ok(song):
            return False

        ControllerApi.player.play(song)
        return True
