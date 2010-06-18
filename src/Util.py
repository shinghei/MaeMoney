import re
import sys
from PyQt4.QtCore import qWarning, QUrl
import traceback

class Util:

    ASCII_PATTERN = re.compile('\\\\x[0-7][0-9a-fA-F]')
    HTMLCODE_PATTERN = re.compile('&#[0-9][0-9][0-9][0-9][0-9];')
    TRUE_FALSE_PATTERN = re.compile('(true)|(false)')
    NEWLINE_RE_PATTERN = re.compile('\n')

    @staticmethod
    def removeNewLine(str):
        str = Util.NEWLINE_RE_PATTERN.sub('', str)
        return str

    @staticmethod
    def fixXescape(str):
        unicoded = Util.ASCII_PATTERN.sub(lambda s: unicode(s.group(0)) (str), str)
        return unicoded

    @staticmethod
    def evalJson(str, withQuotes=True):
        try:
            if withQuotes:
                fixed = eval('\'%s\'' %(str))
            else:
                fixed = eval(str)
        except SyntaxError:
            fixed = ""
            qWarning("Syntax error")
            qWarning(str)
            traceback.print_stack()

        return fixed

    @staticmethod
    def replaceTrueFalseCasing(matchedStr):
        true = matchedStr.group(1)
        false = matchedStr.group(2)

        if true is not None:
            return "True"
        elif false is not None:
            return "False"
        else:
            raise Exception('This is impossible.')

    @staticmethod
    def convertTrueFalseCasing(str):
        converted = Util.TRUE_FALSE_PATTERN.sub(Util.replaceTrueFalseCasing, str)
        return converted

    @staticmethod
    def htmlCodeReplace(matchedStr):
        '''
        @param string matchedStr - &#dddd;
        @see Util.HTMLCODE_PATTERN
        '''
        try:
            htmlCoded = matchedStr.group(0)
            intCode = int(htmlCoded[2:7])
            return unichr(intCode)
        except:
            traceback.print_exc()
            qWarning(htmlCoded)
            return htmlCoded
        
    @staticmethod
    def replaceHtmlCode(str):
        decoded = str.decode('utf-8')
        unicoded = Util.HTMLCODE_PATTERN.sub(Util.htmlCodeReplace, decoded)
        return unicoded

    @staticmethod
    def loadsJsonString(rawData, encoding):
        if sys.version.startswith("2.6") or sys.version.startswith("3"):
            import json
            decodedStocks = json.loads(rawData, encoding)
        else:
            import simplejson
            decodedStocks = simplejson.loads(rawData, encoding)
        return decodedStocks

    @staticmethod
    def openUrl(url):
        import os

        if os.name == 'posix':
            os.system('dbus-send --type=method_call --dest=com.nokia.osso_browser \
                       /com/nokia/osso_browser/request \
                       com.nokia.osso_browser.open_new_window \
                       string:%s' % (url))
        else:
            from PyQt4.Qt import QDesktopServices

            url = QUrl(url, QUrl.TolerantMode)
            QDesktopServices.openUrl(url)
