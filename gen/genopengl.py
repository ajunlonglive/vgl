import os

import requests
from lxml import etree


class Group():
    def __init__(self, name, enums):
        self.name = name
        self.enums = enums

    def __repr__(self):
        return self.name


class Enum():
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return self.name


class Registry():
    def __init__(self, url):
        self.url = url
        self.filename = url.rsplit('/', 1)[-1]
        self.groups = []
        self.enums = []

    def download(self):
        if os.path.exists(self.filename):
            return

        with open(self.filename, 'wb') as f:
            r = requests.get(self.url)
            f.write(r.content)

    def parse(self):
        with open(self.filename) as f:
            xml = f.read()
        root = etree.fromstring(xml.encode('utf-8'))

        for c in root.xpath('//comment()'):
            c.getparent().remove(c)
        for u in root.xpath('//unused'):
            u.getparent().remove(u)

        for element in root.getchildren():
            if element.tag == 'groups':
                for group in element.getchildren():
                    self.groups.append(Group(
                        group.attrib['name'],
                        [enum.attrib['name'] for enum in group.getchildren()]
                    ))

            if element.tag == 'enums':
                for enum in element.getchildren():
                    self.enums.append(Enum(enum.attrib['name'], enum.attrib['value']))


if __name__ == '__main__':
    registry = Registry('https://raw.githubusercontent.com/KhronosGroup/OpenGL-Registry/master/xml/gl.xml')
    registry.download()
    registry.parse()
