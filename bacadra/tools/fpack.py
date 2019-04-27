'''
------------------------------------------------------------------------------
***** general use (f)unction (pack) *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

#$ ######################################################################### #

#$ ____ import _____________________________________________________________ #

import re
import textwrap

#$ ____ def translate _______________________________________________________ #

def translate(text, ndict):
    '''
    Replace string by dict.
    '''

    # loop over keys in dict
    for key in ndict:
        # replace text
        text = text.replace(key, str(ndict[key]))

    # return modyfied text
    return text


#$ ____ def dprint _________________________________________________________ #

def dprint(d, indent=0, style='1'):
    '''
    Dictonary print
    '''

    if style=='1':

        code=''
        for key, value in d.items():
            if type(value)==str: value = "'"+value+"'"
            if type(key)==str: key = "'"+key+"'"
            code+=('\t' * indent + str(key)+':')
            if isinstance(value, dict):
                code+='\n'+dprint(value, indent+1)
            else:
                code+=(' '+str(value)+'\n')
        return code


#$ ____ def nprec __________________________________________________________ #

def nprec(value, notation='f', trail=False, significant=None, decimal=None, exp_width=None):

    # convert to string
    value = list('{:f}'.format(value))

    sign = ''
    if value[0]=='-':
        value.pop(0)
        sign = '-'

    # find dot
    if '.' not in value: value.append('.')
    posdot = value.index('.')

    # move dot
    if notation in ['sci', 'scientific', 'e', 'tex10', 'texe', '10']:

        # if dot in number
        if posdot<len(value):
            value.pop(posdot)

        i=0
        if posdot==1 and value[0]=='0':
            for i in range(len(value)):
                if value[i]!='0':
                    break
            value = value[i:]

        # save expontential
        fexp = posdot-1-i

        # insert new one at 2st position
        value.insert(1,'.')

        # change posdto position
        posdot=1

    # if user want to convert decimal
    if type(decimal)==int:
        j = 0
        for i in range(len(value)-posdot-decimal-1):
            if value[-j-1]!='.':
                value[-j-1] = '0'
                j+=1
            else:
                value[-j-2] = '0'
                j+=2

    if type(significant)==int:
        kzi = 0
        for kz in range(len(value)):
            if value[kz] in ['0']:
                kzi+=1
            elif value[kz] in ['.']:
                continue
            else:
                break

        j = 0
        for i in range(len(value)-significant-1-kzi):
            if value[-j-1]!='.':
                value[-j-1] = '0'
                j+=1
            else:
                value[-j-2] = '0'
                j+=2

    if trail==False:
        for i in range(len(value)):
            if value[-i-1]!='0':
                break
            else:
                value[-i-1]=''

    elif trail=='d' and type(decimal)==int:
        run = len(value)-(posdot+decimal)-1
        if run > 0:
            for i in range(run):
                if value[-i-1]=='.':
                    break
                else:
                    value[-i-1]=''
        elif run < 0:
            for i in range(-run):
                value.append('0')

    elif trail=='s' and type(significant)==int:
        i = 0
        dotflag = False
        while True:
            if value[i] in ['0']:
                i+=1
                continue
            elif value[i] in ['.']:
                i+=1
                dotflag = True
                continue
            else:
                i-=1
                break

        run = len(value)-i-(significant)-dotflag
        if run > 0:
            for i in range(run):
                if value[-i-1]=='.':
                    break
                else:
                    value[-i-1]=''
        elif run < 0:
            for i in range(-run):
                value.append('0')



    if notation in ['std', 'standard', 'f']:

        value = ''.join(value)
        if value[-1]=='.': value=value[:-1]

        return sign+value

    elif notation in ['sci', 'scientific', 'e', 'tex10', 'texe']:

        if notation in ['sci', 'scientific', 'e']:
            value.append('e')
        elif notation in ['10']:
            value.append('*10**(')
        elif notation in ['tex10']:
            value.append('*10^{')
        elif notation in ['texe']:
            value.append(r' \mathrm{e}{')
        fexp = str(fexp)

        if type(exp_width)==int:
            if len(fexp) < exp_width:
                if fexp[0]=='-':
                    fexp=fexp[1:]
                    madd='-'
                else:
                    madd=''
                fexp = madd+'0'*(exp_width-len(fexp)-len(madd)) + fexp

        value.append(fexp)

        value = ''.join(value)
        if notation in ['sci', 'scientific', 'e']:
            if value[2]=='e': value=value[0:1] + value[2:]
        elif notation in ['10']:
            value = value+')'
        elif notation in ['tex10','texe']:
            value = value+'}'

        return sign+value



#$ ____ color text _________________________________________________________ #

#$$ ________ def print_format_table ________________________________________ #

def print_format_table():
    """
    prints table of formatted text format options
    """
    for style in range(8):
        for fg in range(30,38):
            s1 = ''
            for bg in range(40,48):
                format = ';'.join([str(style), str(fg), str(bg)])
                s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
            print(s1)
        print('\n')

#$$ ________ def color _____________________________________________________ #

def color(fmt, fg=None, bg=None, st=None, inherit=True):
    """
    Colour-printer.
        cprint( 'Hello!' )                                  # normal
        cprint( 'Hello!', fg='g' )                          # green
        cprint( 'Hello!', fg='r', bg='w', st='bx' )      # bold red blinking on white
    List of colours (for fg and bg):
        k   black
        r   red
        g   green
        y   yellow
        b   blue
        m   magenta
        c   cyan
        w   white
    List of styles:
        b   bold
        i   italic
        u   underline
        s   strikethrough
        x   blinking
        r   reverse
        y   fast blinking
        f   faint
        h   hide
    """

    COLCODE = {
        'k': 0, # black
        'r': 1, # red
        'g': 2, # green
        'y': 3, # yellow
        'b': 4, # blue
        'm': 5, # magenta
        'c': 6, # cyan
        'w': 7  # white
    }

    FMTCODE = {
        'b': 1, # bold
        'f': 2, # faint
        'i': 3, # italic
        'u': 4, # underline
        'x': 5, # blinking
        'y': 6, # fast blinking
        'r': 7, # reverse
        'h': 8, # hide
        's': 9, # strikethrough
    }

    # properties
    props = []
    if isinstance(st,str):
        props = [ FMTCODE[s] for s in st ]
    if isinstance(fg,str):
        props.append( 30 + COLCODE[fg] )
    if isinstance(bg,str):
        props.append( 40 + COLCODE[bg] )

    # display
    props = ';'.join([ str(x) for x in props ])

    if inherit:
        if props:
            return '\x1b[%sm%s\x1b[0m' % (props, fmt)
        else:
            return fmt

    else:
        if props:
            print( '\x1b[%sm%s\x1b[0m' % (props, fmt) )
        else:
            print( fmt )

#$$ ________ def cprint ____________________________________________________ #

def cprint(*args, **kwargs):
    print(color(*args, **kwargs))



#$ ____ def is_canonical ___________________________________________________ #

def is_canonical(version):
    return re.match(r'^v([1-9]\d*!)?(0|[1-9]\d*)(\.(0|[1-9]\d*))*((a|b|rc)(0|[1-9]\d*))?(\.post(0|[1-9]\d*))?(\.dev(0|[1-9]\d*))?$', version) is not None

# is_canonical('v0.1')
# is_canonical('v0.2.dev1')
# is_canonical('v0.2a1')


#$ ____ def bhead __________________________________________________________ #

def bhead(title, width=75, clr='m'):
    len1 = int((width - len(title) - 6 - 10)/2)
    len2 = (width - len(title) - 6- 10) - len1

    return color(len1*'-' + ' ' + '*'*5 + ' '*2 + title + ' '*2  + '*'*5 + ' '  + len2*'-', clr)


def bend(width=75, clr='m'):
    return color(width*'-', clr)

def bitem(key, val, width):
    return '> {:{}s} = {}'.format(key,width,val)

def btable(title, data, width=75, iwdith=True):
    if iwdith==True:
        iwdith = 0
        for key in data.keys():
            if len(key)>iwdith: iwdith=len(key)

    if title:
        pdata = [bhead(title, width)]
    else:
        pdata = [bend(width)]

    for key,val in data.items():
        if type(val) is str: val = "'" + str(val) + "'"
        # elif type(val) is unise: val = val(style='pretty')
        pdata.append('> {:{}s} = {}'.format(key,iwdith,str(val)))

    if len(pdata)==1:
        pdata+=['There are no atributes.']

    pdata += [bend(width)]
    return '\n'.join(pdata)

def bstore(title, data, width=75, iwdith=True):
    if iwdith==True:
        iwdith = 0
        for key in data.keys():
            if len(key)>iwdith: iwdith=len(key)

    if title:
        pdata = [bhead(title, width)]
    else:
        pdata = [bend(width)]

    for key,val in data.items():

        if 'd' in val: pdata.append('* '+val['d'])

        if 'v' in val:

            if type(val['v']) is str: val['v'] = "'" + str(val['v']) + "'"
            pdata.append('> {:{}s} = {}'.format(key,iwdith,str(val['v'])))

    if len(pdata)==1:
        pdata+=['There are no atributes.']

    pdata += [bend(width)]
    return '\n'.join(pdata)




def berwin(mode, code, info, width=75):

    if   code[0]=='e': clr = 'c'
    elif code[0]=='w': clr = 'y'
    elif code[0]=='i': clr = 'g'

    title = mode + ' : ' + code
    pdata = [bhead(title, width, clr)]

    info = str(info).split('\n')
    for i in range(len(info)):
        info[i] = textwrap.fill(str(info[i]), width=width)
    pdata += ['\n'.join(info)]

    pdata += [bend(width, clr)]

    return '\n'.join(pdata)

#$ ____ class mdata ________________________________________________________ #

class mdata:

    def __init__(self, obj=None, **kwargs):
        if obj==None: obj={}
        if kwargs:    obj.update(kwargs)
        for key,val in obj.items():
            setattr(self, key, val)

    def __call__(self):
        print(btable(
            title='bacadra mapped object',
            data={key:getattr(self, key) for key in self.__dict__},
        ))





#$ ######################################################################### #
