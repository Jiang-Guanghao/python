#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pymysql
import re
import xml.dom.minidom as MND

OK = 0
BAD_ARGS = 1

def newwritexml(self, writer, indent= '', addindent= '', newl= ''):
    if len(self.childNodes)==1 and self.firstChild.nodeType==3:
        writer.write(indent)
        self.oldwritexml(writer) # cancel extra whitespace
        writer.write(newl)
    else:
        self.oldwritexml(writer, indent, addindent, newl)

def usage():
    print("Usage:")
    print("\tpython createddl.py tablename")

def main(argv):
    if len(argv) != 2:
        usage()
        return BAD_ARGS
    
    tabname=argv[1]
    print("Generate ddl file for "+tabname+" ...")
    typedict = {}
    with open("typedict.cfg") as f:
        lines = f.readlines()
    for line in lines:
        line = re.sub(r'\n', '' , line)
        items = re.split(r'\s+', line)
        typedict[items[0]] = items[1]
    
    tabcolsinfo=[]
    keycolsname=[]
    try:
        conn = pymysql.connect("127.0.0.1","cim","123456","cim" )
        cursor=conn.cursor()
        sql = 'SELECT COLUMN_NAME, DATA_TYPE, DATA_LENGTH, DATA_PRECISION, DATA_SCALE from USER_TAB_COLS \
               WHERE TABLE_NAME=%s ORDER BY COLUMN_ID' % (tabname)
        cursor.execute(sql)
        tabcolsinfo=cursor.fetchall()
        sql = 'SELECT cols.column_name FROM user_constraints cons, user_cons_columns cols \
               WHERE cols.table_name = UPPER(%s) AND cons.constraint_type = \'P\' \
                 AND cons.constraint_name = cols.constraint_name' % (tabname)
        cursor.execute(sql)
        keycolsname=cursor.fetchall()
    except Exception as e:
        print('Error:', e)
    finally:
        if conn:
            conn.close()
    
    doc = MND.Document()
    content = doc.createElement("transmit-content")
    doc.appendChild(content)
    file = doc.createElement('file')
    content.appendChild(file)
    
    fileinfos={'filename':tabname, 'fileversion':'V1.1', 'fieldcount':len(tabcolsinfo), 'isfixedlength':'0'}
    for k,v in fileinfos.items():
        element = doc.createElement( k )
        text = doc.createTextNode( str(v) )
        element.appendChild(text)
        file.appendChild(element)
    
    fielddescription = doc.createElement( "fielddescription" )
    for record in tabcolsinfo:
        columnname = record[0]
        datatype = record[1]
        datalength = record[2]
        precision = record[3]
        scale = record[4]
        element = doc.createElement( "fieldname" )
        text = doc.createTextNode( columnname )
        element.appendChild(text)
        fielddescription.appendChild(element)
        if datatype == 'NUMBER':
            if scale == 0:
                fieldtype = str(precision)+'n'
            else:
                fieldtype = str(precision+1)+'n'+'('+str(scale)+')'
        else:
            fieldtype = re.sub('#', str(datalength) , typedict[datatype])
        element = doc.createElement( "fieldtype" )
        text = doc.createTextNode( fieldtype )
        element.appendChild(text)
        fielddescription.appendChild(element)
    file.appendChild(fielddescription)
    
    keydescription = doc.createElement( "keydescription" )
    for record in keycolsname:
        columnname = record[0]
        element = doc.createElement( "keyname" )
        text = doc.createTextNode( columnname )
        element.appendChild(text)
        keydescription.appendChild(element)
    file.appendChild(keydescription)
    
    MND.Element.oldwritexml = MND.Element.writexml
    MND.Element.writexml = newwritexml
    f = open(tabname+'.ddl', 'wb')
    f.write( doc.toprettyxml(indent= '', newl= '\n', encoding="utf-8") )
    f.close()
    print("Generate ddl file for "+tabname+" end.")
    return OK

if __name__ == '__main__':
    sys.exit(main(sys.argv))
