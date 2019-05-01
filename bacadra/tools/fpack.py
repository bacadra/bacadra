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

import os.path

import shutil

import re

import textwrap

import numpy as np

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

def dprint(d, indent=0, style='1', to_print=True):
    '''
    Dictonary print
    '''

    if style=='1':

        code=''
        for key, value in d.items():
            if type(value)==str: value = "'"+value.replace('\n', '\\n')+"'"
            if type(key)==str: key = "'"+key+"'"
            code+=('\t' * indent + str(key)+':')
            if isinstance(value, dict):
                code+='\n'+dprint(value, indent+1, to_print=False)
            else:
                code+=(' '+str(value)+'\n')

    if to_print==True:
        print(code)
    else:
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

#$ ____ fancy item _________________________________________________________ #

#$$ ________ def bhead _____________________________________________________ #

def bhead(title, width=75, clr='m'):
    len1 = int((width - len(title) - 6 - 10)/2)
    len2 = (width - len(title) - 6- 10) - len1

    return color(len1*'-' + ' ' + '*'*5 + ' '*2 + title + ' '*2  + '*'*5 + ' '  + len2*'-', clr)

#$$ ________ def bend ______________________________________________________ #

def bend(width=75, clr='m'):
    return color(width*'-', clr)

#$$ ________ def bitem _____________________________________________________ #

def bitem(key, val, width):
    return '> {:{}s} = {}'.format(key,width,val)

#$$ ________ def btable ____________________________________________________ #

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

#$$ ________ def bstore ____________________________________________________ #

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

#$$ ________ def berwin ____________________________________________________ #

def berwin(mode, code, info, width=75, head=True, bott=True):

    if   code[0]=='e': clr = 'c'
    elif code[0]=='w': clr = 'y'
    elif code[0]=='i': clr = 'g'

    title = mode + ' : ' + code
    if head:
        pdata = [bhead(title, width, clr)]
    else:
        pdata = []

    info = str(info).split('\n')
    for i in range(len(info)):
        info[i] = textwrap.fill(str(info[i]), width=width)
    pdata += ['\n'.join(info)]

    if bott: pdata += [bend(width, clr)]

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




#

def letchk(driver, letters, mode='all'):
    '''
    Check if letters occur in driver string

    ***** Parameters *****

    driver: [str]

    letters: [str]

    mode: {...}

        mode: {'any'}
            reutrn True if any letters occur in driver, else False

        mode: {'all'}
            reutrn True if all letters occur in driver, else False

    '''

    if mode in ['all']:
        return all(i in driver for i in letters)

    elif mode in ['any']:
        return any(i in driver for i in letters)

    elif mode in ['valid']:

        if not all(i in driver for i in letters):

            # verrs can be loaded now
            from . import verrs

            verrs.BCDR_tools_ERROR_Letters_check(driver, letters)

            verrs.BCDR_tools_WARN_Letters_check(driver, letters)



#$ ____ class bpath ________________________________________________________ #

class bpath:

#$$ ________ def __init__ __________________________________________________ #

    def __init__(self, path=[], file='', ext=''):
        '''
        Atributes and properties, only to read!

        path: [list, str]
            list of the path's

        file: [str]
            name of the file without extension. ex. 'main'

        ext: [str]
            extension of the file, with pre dot, ex. '.py'
            file+ext give full name of the file, ex. 'main.py'
        '''

        self.path, self.file, self.ext = self._parse(path=path, file=file, ext=ext)

#$$ ________ def call ______________________________________________________ #

    def call(self, code='sjfe', relpath=None, path=None, file=None, ext=None):
        '''
        Return path converted to string or bpath.

        ***** Parameters *****

        code: [letters via string] (None)
            Set output options.
            If 'bp' will be use together, then only 'b' returned.
            If 'ar' will be use together, then only 'r' returned.

            'p' -- print output as string
            'b' -- return as bpatch
            's' -- return as string
            'j' -- joined path or name of the folder
                   can be ranged by followed start:stop
                   ex: '..j2'
                   ex: '..j-2'
                   ex: '..j1:-1'
                   ex: '..j:-1'
                   ex: '..j2:'
            'f' -- add file base name (without extension)
            'e' -- add extension after
            'a' -- convert to absolute path
            'r' -- convert to relative path, relpath must be given
            '/' -- convert backslash to slash. dont work together with 'b'

        relpath: [list, str, bpath] (None)
            Path input object. with code 'r' will return relative path.

        path: [list, str] (None)
            locally overwrite 'path' atributes. naturally have sense only together with 'b' or 's'

        file: [str] (None)
            locally overwrite 'file' atribute. it have sense only together with 'f'

        ext: [str] (None)
            locally overwrite 'ext' atribute. it have sense only with 'e'
        '''
        path, file, ext = self._parse(path, file, ext)

        if 'b' not in code and 's' not in code: code+='s'

        output = ''

        if 'j' in code:
            index = code.index('j')

            i=0
            while len(code)>index+1+i and code[index+1+i] in '-0123456789:':
                i+=1

            range_string = code[index+1:index+1+i]

            if range_string in ['',':']:
                output = '\\'.join(path)
                if output: output += '\\'

            elif ':' in range_string:
                start, stop = range_string.split(':')
                if start: start=eval(start)
                if stop: stop=eval(stop)
                # start, stop = eval(start), eval(stop)

                if start and stop:
                    output = '\\'.join(path[start:stop])
                elif start:
                    output = '\\'.join(path[start:])
                elif stop:
                    output = '\\'.join(path[:stop])

                if output: output += '\\'

            else:
                output = path[eval(range_string)]

        # add file with extension
        if 'b' in code:
            pass

        elif 'f' in code and 'e' in code:
            output = os.path.join(output,file+ext)

        # elif add file without extension
        elif 'f' in code:
            output =os.path.join(output,file)

        elif 'e' in code:
            output =os.path.join(output,ext)

        if 'r' in code and relpath!=None:

            if type(relpath) in [list, str]:
                relpath = bpath(relpath)

            output = os.path.relpath(output, relpath('sj'))

        # convert path to absolute path
        elif 'a' in code:
            output = os.path.abspath(output)

        # convert backslash to slash
        if '/' in code and 'b' not in code:
            output = output.replace('\\','/')

        if 'p' in code:
            print(output)

        if 'b' in code:

            if output[-1]=='\\': output=output[:-1]

            return bpath(
                path = output,
                file = (file if 'f' in code else ''),
                ext  = (ext  if 'e' in code else ''),
            )

        elif 's' in code:
            return output


#$$ ________ def __call__ __________________________________________________ #

    __call__ = call

#$$ ________ def __str__ ___________________________________________________ #

    __str__ = __call__

#$$ ________ def __format__ ________________________________________________ #

    def __format__(self, code=''):
        '''
        ***** Parameters *****

        code: [letters via string] ('sjfe')
        '''

        if code=='': code='sjfe'

        code.replace('b', 's')

        if 's' not in code: code += 's'

        return self(code=code)

#$$ ________ def __rshift__ ________________________________________________ #

    __rshift__ = __format__

#$$ ________ def __repr__ __________________________________________________ #

    def __repr__(self):
        return f"bpath(path={self.path}, file='{self.file}', ext='{self.ext}')"

#$$ ________ def __getitem__ _______________________________________________ #

    def __getitem__(self, item):
        return bpath(
            path = self.path[item],
            file = self.file,
            ext  = self.ext,
        )


#$$ ________ def __truediv__ _______________________________________________ #

    def __truediv__(self, other):
        return bpath(
            path = self.path + other.path,
            file = other.file,
            ext  = other.ext,
        )


#$$ ________ def chkdir ____________________________________________________ #

    def chkdir(src, path=None):
        '''
        Check if directory exists

        ***** Parameters *****

        src: [bpath, list of bpath]
            ex: 'a/b/c'

        path: [list, str] (None)


        '''
        if type(src)==list:
            return [one.chkdir(path=path) for one in src]

        return os.path.isdir(src('sj', path=path))



#$$ ________ def chkfile ___________________________________________________ #

    def chkfile(src, path=None, file=None, ext=None):
        '''
        Check if file exists

        ***** Parameters *****

        src: [bpath, list of bpath]

        path: [list, str] (None)

        file: [str] (None)

        ext: [str] (None)
        '''
        if type(src)==list:
            return [one.chkfile(path=path, file=file, ext=ext) for one in src]

        return os.path.isfile(src('sjfe', path=path, file=file, ext=ext))

#$$ ________ def mkdir _____________________________________________________ #

    def mkdir(src, exists=True, path=None):
        '''
        Create directory, can be nested.

        ***** Parameters *****

        src: [bpath, list of bpath]

        exist: [bool] (True)
            If False then if directory already exists then return OSError exception.
            If True then silenty skip making dir.

        path: [list, str] (None)

        ***** Notes *****

        Note makedirs() will become confused if the path elements to create include pardir (eg. “..” on UNIX systems). I have tested it and work ok...

        https://docs.python.org/3/library/os.html#os.makedirs

        '''
        if type(src)==list:
            [one.mkdir(exists=exists, path=path) for one in src]
            return

        os.makedirs(src('sj', path=path), exist_ok=exists)

#$$ ________ def mkfile ____________________________________________________ #

    def mkfile(src, write=None, separator='\n', close=True, exists=True, path=None, file=None, ext=None):
        '''
        Create text file, data can be wrriten.

        ***** Parameters *****

        src: [bpath, list of bpath]

        write: [str, list, tuple, np.ndarray] (None)

        separator: [str] ('\n')

        exists: [bool] (True)
            If False, then raise error if destination folder does not exists
            If True, then create destination folder

        path: [list, str] (None)

        file: [str] (None)

        ext: [str] (None)

        ***** Returns *****

        return FileObject
            if Close=False then object is not closed!

        '''
        if type(src)==list:
            [one.mkfile(write=write, separator=separator, path=path, file=file, ext=ext) for one in src]
            return

        fullpath = src('sjfe', path=path, file=file, ext=ext)

        if exists: src.mkdir(path=path)

        f = open(fullpath, 'w+')

        if type(write) in [list, tuple, np.ndarray]:
            f.writelines(separator.join(write))

        elif type(write) in [str]:
            f.writelines(write)

        if close: f.close()

        return f


#$$ ________ def rmdir _____________________________________________________ #

    def rmdir(src, exists=True, empty=True, path=None):
        '''
        Delete folder and intermetdie empty folders.

        ***** Parameters *****

        src: [bpath, list of bpath]

        exists: [bool] (True)
            if False then raise error if folder does not exists
            if True then silenty skip it

        empty: [bool] (True)
            if False then raise error if folder is not empty
            if True then delete folder with all files

        path: [list, str] (None)

        ***** Notes *****

        https://docs.python.org/3/library/os.html#os.removedirs
        '''
        if type(src)==list:
            [one.rmdir(exists=exists, empty=empty, path=path) for one in src]
            return

        if exists and not src.chkdir(path=path): return

        fullpath = src('sj', path=path)

        shutil.rmtree(fullpath, ignore_errors=empty)

#$$ ________ def rmfile ____________________________________________________ #

    def rmfile(src, exists=True, path=None, file=None, ext=None):
        '''
        Remove the file, extenstion can be set explicit.

        ***** Parameters *****

        src: [bpath, list of bpath]

        exists: [bool] (True)
            if False then raise error if file does not exists
            if True then silenty skip it

        path: [list, str] (None)

        file: [str] (None)

        ext: [str] (None)

        ***** Notes *****

        https://docs.python.org/3/library/os.html#os.remove
        '''
        if type(src)==list:
            [one.rmfile(exists=exists, path=path, file=file, ext=ext) for one in src]
            return

        if not exists and src.chkfile(path=path, file=file, ext=ext):
            return

        os.remove(src('sjfe', path=path, file=file, ext=ext))



#$$ ________ def cpfile ____________________________________________________ #

    def cpfile(src, dst,
        src_exists = True, dst_exists = True, dst_folder = True,
        src_path   = None, src_file   = None, src_ext    = None,
        dst_path   = None, dst_file   = None, dst_ext    = None):
        '''
        Copy file to destination folder.

        ***** Parameters *****

        src: [bpath, list of bpath]

        dst: [bpath, list of bpath]

        src_exists: [bool] (True)
            if True then skip if src_file does not exists
            if False then raise error

        dst_exists: [bool] (True)
            if True then skip if dst_file does not exists
            if False then raise error

        dst_folder: [bool] (True)
            if True, destination folder does not exists then create it
            if False, then raise error

        src_path: [list, str] (None)

        src_file: [str] (None)

        src_ext: [str] (None)

        dst_path: [list, str] (None)

        dst_file: [str] (None)

        dst_ext: [str] (None)
        '''
        if type(src)==list:
            [one.cpfile(
                src_exists = src_exists,
                dst_exists = dst_exists,
                dst_folder = dst_folder,
                src_path   = src_path,
                src_file   = src_file,
                src_ext    = src_ext,
                dst_path   = dst_path,
                dst_file   = dst_file,
                dst_ext    = dst_ext,
            ) for one,two in zip(src, dst)]
            return

        if not src_exists and not src.chkfile(
            path=src_path, file=src_file, ext=src_ext,
        ): return

        if not dst_exists and not dst.chkfile(
            path=dst_path, file=dst_file, ext=dst_ext,
        ): return

        if dst_folder: dst.mkdir()

        shutil.copyfile(
            src = src('sjfe', path=src_path, file=src_file, ext=src_ext),
            dst = dst('sjfe', path=dst_path, file=dst_file, ext=dst_ext),
            follow_symlinks=True,
        )


    def listdir(src, tree=False, max_deep=999, path=None):
        '''
        Create list of file and folders in given folder.

        tree: [bool] (False)
            if True then return full tree list
            if False then return only files in given directory
        '''

        if type(src)==list:
            return [one.listdir(path=path) for one in src]

        if tree==False:
            return os.listdir(src('sj', path=path))

        deep, tree = -1, {}

        def create_tree(tree, path):

            nonlocal deep

            deep+= 1

            if deep >= max_deep:
                deep-= 1
                return tree

            # create continer for files
            tree['*'] = []

            for obj in os.listdir(path):

                fullpath = os.path.join(path, obj)

                # if it is dir
                if os.path.isdir(fullpath):

                    # create subdir
                    tree[obj] = {}

                    # call recursive
                    create_tree(tree[obj], fullpath)

                # if it is file
                elif os.path.isfile(fullpath):

                    # add file
                    tree['*'].append(obj)

            deep-= 1

        create_tree(tree, src('sj', path=path))

        return tree






#$$ ________ def _parse ____________________________________________________ #

    def _parse(src, path=None, file=None, ext=None):
        '''
        Parse input parameters
        '''
        if path==None:
            path = src.path
        elif type(path)==str:
                path = path.replace('/','\\')
                path = path.split('\\')

        if '.' in path[-1] and file in ['', None] and ext in ['', None]:
            print('flag2')
            index = path[-1].rfind('.')
            file, ext = path[-1][:index], path[-1][index:]
            path = path[:-1]

        if file==None: file=src.file
        if ext==None: ext=src.ext




        if ext and ext[0]!='.': ext='.'+ext
        return path, file, ext





#$ ######################################################################### #
