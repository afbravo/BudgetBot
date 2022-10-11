from bs4 import BeautifulSoup as bs4

def main():
    filename = 'bg0.html'

    with open(filename, 'r') as f:
        html = f.read()

    text = getHTMLText(html)
    print(text)
    print(getMoney(text))


def getMoney(text):
    for i in text:
        if i[0] == '$':
            return i[1:]


def getHTMLText(html):
    soup = bs4(html, 'html.parser')
    #find the money amount
    text = soup.get_text()
    text = text.replace('\\r', '').replace('\\n', '').replace('\\t', '').replace(' ', ',')
    text = text.split(',')
    text = [x for x in text if x != '']
    return text


if __name__ == '__main__':
    main()