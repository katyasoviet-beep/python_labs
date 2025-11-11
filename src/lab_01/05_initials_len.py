FIO = input('ФИО: ')
FIO=FIO.strip()
WORDS = FIO.split()
INITIALS = ''
LEN_FIO = len(FIO)
COUNT_SPACE = FIO.count(' ')
for word in WORDS:
    INITIALS += word[0].upper()+'.'
print('Инициалы:', INITIALS)
print('Длина (символов):', LEN_FIO-COUNT_SPACE+2)
