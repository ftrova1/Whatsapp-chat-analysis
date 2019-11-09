import re
import config
import emoji

def startsWithDateTime(s):
    pattern = '^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)(\d{2}|\d{4}), ([0-9][0-9]):([0-9][0-9]) -'
    result = re.match(pattern, s)
    if result:
        return True
    return False

def startsWithAuthor(s):
    patterns = [
        '([\w]+):',                        # Nome
        '([\w]+[\s]+[\w]+):',              # Nome Cognome
        '([\w]+[\s]+[\w]+[\s]+[\w]+):',    # Nome Secondo nome Cognome
        '([+]\d{2} \d{3} \d{7})'           # +39 XXX XXXXXXX
    ]
    pattern = '^' + '|'.join(patterns)
    result = re.match(pattern, s)
    if result:
        return True
    return False

def getDataPoint(line):

    splitLine = line.split(' - ')
    dateTime = splitLine[0]
    date, time = dateTime.split(', ')
    message = ' '.join(splitLine[1:])

    if startsWithAuthor(message):
        splitMessage = message.split(': ')
        author = splitMessage[0]
        message = ' '.join(splitMessage[1:])
    else:
        author = None
    return date, time, author, message

parsedData = []
conversationPath = config.DATA_PATH
with open(conversationPath, encoding="utf-8") as fp:

    messageBuffer = []
    date, time, author = None, None, None

    while True:
        line = fp.readline()
        if not line:
            break   #EOF
        line = line.strip() # Elimino gli spazi bianchi iniziali e finali
        if startsWithDateTime(line): # Se la linea letta inizia con una data vuol dire che è un nuovo messaggio
            if len(messageBuffer) > 0: # Controlla se il buffer contiene caratteri provenienti dalla precedente iterazione (messaggio multilinea)
                parsedData.append([date, time, author, ' '.join(messageBuffer)])
            messageBuffer.clear() # Pulisco il buffer
            date, time, author, message = getDataPoint(line)
            messageBuffer.append(message)
        else:
            messageBuffer.append(line) # Se la linea letta NON inizia con una data vuol dire che è un messaggio su più righe
