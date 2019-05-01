
# bacadra docstyle

## General

Project bacadra have introduce their own docstyle. This is due to the very personalized use of the package, like units.

## Principles

The general docstyle is assumed at the below example.

~~~python
def test_function():
    '''
    There are difference between None and NotOccur

    ***** Parameters *****

    x: [type] (default value) {set of avaiable values} #letter
        type ex   : [letters via string] [str] [int] [numeric] [kN]
        default ex: (True), (15*kN)
        set ex    : {1, True, 'val'}
        lettter ex: #a, #c

    code: [str]
        the simplest description

    code: [unise:kN]
        the type must be input as unise:kN

    y: {...} ('r')
        parameter can gen one of value from set {..} and default 'r'

        y: {'execute', 'row', 'r'}
            Description of part of set

        y: {'execute2', 'row2', 'r2'}
            Description of part of set

    data: [...] (None)
        multitype can be inputed

        data: [tuple]
            what going on if data is tuple type

        data: [list]
            what going on if data is list type

    sql: [dict]
        example of nested dict description. * before and after key and val mean that the name is freely

        *key*: [str]
            here you can write key designation

        *val*: [dict]
            next one nested dict

            *key*: [str]
                will treat as column name, dont use square bracket [ ], it will be include automaticly.

            *val*: [dict]
                here is example of dict where keys are freezen, please remember about '' if string

                'sqltype': [str] (NotOccur)
                    it will be used to define type in sqlite database

                'pytype': [list of strings] (NotOccur)
                    it can be check if proper type inputed, please do not insert unise value into cell!

                'unise': [str] (NotOccur)
                    it will be check if value is input in proper unit, but also can be input without unit -> then treat is as this unit

                'description': [dict] (NotOccur)
                    description of column designing

                    *key: [str]
                        represent language shortname like en,pl

                    *val: [str]
                        description in proper language

            '*pri': [list of strings]
                list of ids of primary columns


    ***** Output *****

    if a > b: [auto]
        return a + b

    If function use yield insted returns then change

    if a > b: [auto]
        yield a + b

    ***** Erwin *****

    Please mark what kind of erwin will be raised (e), (w), (i)

    (e) BCDR_ERROR:

        BCDR_dbase_ERROR_Open_Database is called if divide by 0

    ***** Example *****

    Small example how to use this function. The bigger one should be placed at other repositories.

    ***** Notes ******

    Here you can plase link to website, book references etc.

    ***** See Also *****

    Here is the best place to write reference to other methods, atributes etc.

    '''
~~~
