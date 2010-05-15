from Util import *
import urllib2
import urllib

class StockMatchGoogleFinance:
    BUFFER_SIZE = 1024
    BASE_GFINANCE_URL = "http://www.google.com.hk/finance/match?q=%s"
    NEWLINE_RE = urllib2.re.compile('\n')
    JSON_RE = urllib2.re.compile('\{[\s]*\"matches\"[\s]*:[\s]*[[\s]*\{.*\}[\s]*\].*\}')

    BIG5HK_ENCODING = "big5hkscs"
    DEFAULT_ENCODING = BIG5HK_ENCODING

    def __init__(self, encoding=DEFAULT_ENCODING):
        self.encoding = encoding

    def getMatchesFromGFinance(self, queryString):
        encodedQueryString = urllib.quote(str(queryString))
        url = self.BASE_GFINANCE_URL % (encodedQueryString)
        connection = urllib2.urlopen(url)
        buffer = []
        while True:
            partialData = connection.read(self.BUFFER_SIZE)
            if not partialData:
                break
            buffer.append(partialData)
        connection.close()
        fromGoogle = "".join(buffer)

        fromGoogle = fromGoogle.decode(self.encoding).encode('utf-8')

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
            print "Cannot open url for " + queryString
            return None
        except ValueError:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                                      file=sys.stdout)
            print "Value Error\n" + rawBuffer
            return None
