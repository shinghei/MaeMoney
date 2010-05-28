from Util import *
import urllib2
import urllib
from Properties import Properties

class StockMatchGoogleFinance:
    BUFFER_SIZE = 1024
    NEWLINE_RE = urllib2.re.compile('\n')
    JSON_RE = urllib2.re.compile('\{[\s]*\"matches\"[\s]*:[\s]*[[\s]*\{.*\}[\s]*\].*\}')



    def __init__(self):
        self.prop = Properties.instance()

    def getMatchesFromGFinance(self, queryString):
        encodedQueryString = urllib.quote(str(queryString))

        gUrl = self.prop.getGoogleUrl()
        url = "http://%s/finance/match?q=%s" % (gUrl, encodedQueryString)
        connection = urllib2.urlopen(url)
        buffer = []
        while True:
            partialData = connection.read(self.BUFFER_SIZE)
            if not partialData:
                break
            buffer.append(partialData)
        connection.close()
        fromGoogle = "".join(buffer)

        enc = self.prop.getEncoding()
        fromGoogle = fromGoogle.decode(enc).encode('utf-8')

        return fromGoogle

    def cleanUpDataFromGoogle(self, rawBuffer):
        cleaned = Util.removeNewLine(rawBuffer)
        cleaned = Util.convertTrueFalseCasing(cleaned)
        cleaned = Util.replaceHtmlCode(cleaned)
        return cleaned

    def convertToJson(self, cleaned):
        matchObject = self.JSON_RE.search(cleaned)
        if matchObject is not None:
            jsonString = matchObject.group(0)
            jsonMatches =  Util.evalJson(jsonString, False)
            return jsonMatches
        else:
            return None

    def match(self, queryString):
        try:
            rawBuffer = self.getMatchesFromGFinance(queryString)
            cleaned = self.cleanUpDataFromGoogle(rawBuffer)
            jsonMatches = self.convertToJson(cleaned)

            if jsonMatches is not None:
                matches = jsonMatches['matches']
                return matches
            else:
                return None
                
        except urllib2.HTTPError:
            qWarning("Cannot open url for " + queryString)
            return None
        except ValueError:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                                      file=sys.stdout)
            qWarning("Value Error\n" + rawBuffer)
            return None
