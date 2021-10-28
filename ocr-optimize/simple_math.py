import re

def strB2Q(ustring):
    rstring = ''
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 0x3000:
            inside_code = 0x0020
        else:
            inside_code -= 0xfee0
        if not (0x0021 <= inside_code and inside_code <= 0x7e):
            rstring += uchar
            continue
        rstring += chr(inside_code)
    return rstring

def mathStyleText(latex):
    transmap = {
        'min': '\\textrm{min}',
        'cm': '\\textrm{cm}',
        'm/s': '\\textrm{m/s}',
        'Rt': '\\textrm{Rt}',
    }
    for k, v in transmap.items():
        latex = latex.replace(k, v)
    return latex

def fullstopBySci(ustring):
    return ustring.replace('。', '．')

def clearCR(ustring):
    return ustring.replace('\n', '')

def repairPunctMark(ustring):
    # 引号修复：修复 “ " 型的右侧引号问题
    ustring = re.sub(
        r"\“([^”]{1,20})\"",
        lambda m: '“' + m.group(1) + '”',
    ustring)
    return ustring

def buildCR(ustring):
    # 构造换行：当有小题序列号时，换行
    ustring = re.sub(
        r"\([1-6]\)",
        lambda m: '\n' + m.group(0) + ' ',
    ustring)
    # 构造换行：当有小题序列号时，换行
    ustring = re.sub(
        r"[A-D]\.",
        lambda m: '\n' + m.group(0) + ' ',
    ustring)
    return ustring

def buildMath(ustring):
    def _build(matched):
        result = ''
        # if matched.group(0).strip() in ('.', '(', ')', '()', 'A.', 'B.', 'C.', 'D.') or not re.match('[a-zA-Z0-9]',matched.group(0)):
        if matched.group(0).strip() in ('.', '(', ')', '()', ':' 'A.', 'B.', 'C.', 'D.'):
            result = matched.group(0)
        else:
            result = ' $' + mathStyleText(matched.group(0)).strip() + '$ '
        return result
    ustring = re.sub(
        r"[a-zA-Z\ \\\u0028-\u002b\u002d-\u003e]{1,50}", _build, ustring)
    return ustring

def mathChar2TeX(ustring):
    transmap = {
        '△': '\\triangle',
        '∠': '\\angle',
        '°': '\\degree',
        '≌': '\\cong',
        '⊥': '\\perp'
    }
    for k, v in transmap.items():
        ustring = ustring.replace(k, v + ' ')
    return ustring

def repairPunctSpace(ustring):
    # 修复逗号、顿号为全角字符并将多余的空格删去，所以应当最后处理
    transmap = {
        ' , ': '，',
        ', ': '，',
        ' ,': '，',
        ',': '，',
        ' 、 ': '、',
        ' 、': '、',
        '、 ': '、',
    }
    for k, v in transmap.items():
        ustring = ustring.replace(k, v)
    return ustring

def repairErrorChinese(ustring):
    return ustring.replace('- -', '一')


if __name__ == '__main__':
    # a = strB2Q("你好ｐｙｔｈｏｎａｂｄａｌｄｕｉｚｘｃｖｂｎｍ")
    text = """
[2021江苏无锡期中,偏难]两套完全相同(如图甲所示)
的加热装置,两套装置的试管中分别装有少量的相等体
积的M固体和N固体,它们的温度随加热时间变化的曲
线如图乙所示,在35 min内M物质从固体熔化成了液体，
N物质始终是固体,则下列说法正确的是
"""
    print(repairPunctSpace( buildMath(buildCR(repairPunctMark(repairErrorChinese( mathChar2TeX( strB2Q(clearCR(text)) ) )))) ))
