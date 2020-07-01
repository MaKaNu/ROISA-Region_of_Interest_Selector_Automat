from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from libs.utils import *
from libs.resources import *
from libs.stringBundle import StringBundle
from libs.toolBar import ToolBar
from libs.canvas import Canvas
from libs.errors import *


class WindowMixin(object):

    def menu(self, title, actions=None):
        menu = self.menuBar().addMenu(title)
        if actions:
            addActions(menu, actions)
        return menu

    def toolbar(self, title, actions=None):
        toolbar = ToolBar(title)
        toolbar.setObjectName(u'%sToolBar' % title)
        # toolbar.setOrientation(Qt.Vertical)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        if actions:
            addActions(toolbar, actions)
        self.addToolBar(Qt.LeftToolBarArea, toolbar)
        return toolbar


class StartWindow(QMainWindow, WindowMixin):
    def __init__(self, appname='defaultName', defaultFilename=None):
        super().__init__()
        self.setWindowTitle(appname)

        # Standard QT Parameter
        self.title = 'ROISA - Region of Interest Selector Automat'
        self.__left = 1
        self.__top = 30
        self.__width = 640
        self.__height = 480

        # Application state.
        self.__image = QImage()
        self.__filePath = defaultFilename

        # Load string bundle for i18n
        self.__stringBundle = StringBundle.getBundle()

        def getStr(strId):
            return self.__stringBundle.getString(strId)

        # Create Canvas Widget
        self.__canvas = Canvas(parent=self)

        # Load Actions
        quit = self.get_quit()
        open = self.get_open()

        # Store actions for further handling.
        self.__actions = struct(
            open=open,
            fileMenuActions=(
                open,
                quit),
            beginner=(),
            advanced=(),
            editMenu=(),
            beginnerContext=(),
            advancedContext=(),
            onLoadActive=(),
            onShapesPresent=()
            )

        # Create Menus
        self.__menus = struct(
            file=self.menu('&File'),
            edit=self.menu('&Edit'),
            view=self.menu('&View'),
            help=self.menu('&Help'),
            recentFiles=QMenu('Open &Recent')
            )

        # Fill Menus
        addActions(self.__menus.file, (
            open,
            quit,
            )
            )
        # addActions(self.menus.help, (help, showInfo))
        # addActions(self.menus.view, (
        #     self.autoSaving,
        #     self.singleClassMode,
        #     self.displayLabelOption,
        #     labels, advancedMode, None,
        #     hideAll, showAll, None,
        #     zoomIn, zoomOut, zoomOrg, None,
        #     fitWindow, fitWidth))

        # Create Toolbars
        self.__tools = self.toolbar('Tools')
        self.__actions.beginner = (
            open, None, quit
            )

        addActions(self.__tools, self.__actions.beginner)

        self.statusBar().showMessage('%s started.' % appname)
        self.statusBar().show()

    from ._actions import get_open, get_quit
    from ._filehandler import openFile, loadFile
