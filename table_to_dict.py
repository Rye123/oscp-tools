# table_to_dict.py: Converts a table into an array of dictionaries
# Useful for converting a dumped database that's too wide for your terminal into
# Python dictionary objects that can be introspected.
# 
# Usage:
# Use as part of the Python REPL.
# >>> from table_to_dict import table_to_dict as ttd
# >>> delimiter="|"
# >>> titletext="      id     | name      | password       "
# >>> contentstext="""01       | john            | 1234        
# ... 02       | andy            | password        
# ... 03       | betty            | word        
# ... 04       | charlie            | rockyou        
# ... 05       | denise            | correcthorsebatterystaple        
# ... 06       | eunice            | five        
# ... 07       | frank            | anotherpassword        
# ... 08       | grant            | password1234        
# ... 09       | harry            | 1234asdf        
# ... 010       | irene            | qwerty        
# ... 011       | jack            | jackspassword        """
# >>> arr = ttd(delimiter,titletext,contentstext)
# >>> arr
# [{'id': '01', 'name': 'john', 'password': '1234'}, {'id': '02', 'name': 'andy', 'password': 'password'}, {'id': '03', 'name': 'betty', 'password': 'word'}, {'id': '04', 'name': 'charlie', 'password': 'rockyou'}, {'id': '05', 'name': 'denise', 'password': 'correcthorsebatterystaple'}, {'id': '06', 'name': 'eunice', 'password': 'five'}, {'id': '07', 'name': 'frank', 'password': 'anotherpassword'}, {'id': '08', 'name': 'grant', 'password': 'password1234'}, {'id': '09', 'name': 'harry', 'password': '1234asdf'}, {'id': '010', 'name': 'irene', 'password': 'qwerty'}, {'id': '011', 'name': 'jack', 'password': 'jackspassword'}]
# >>> arr[0]
# {'id': '01', 'name': 'john', 'password': '1234'}
# >>> [print(rec["name"] + ':' + rec["password"]) for rec in arr]
# john:1234
# andy:password
# betty:word
# charlie:rockyou
# denise:correcthorsebatterystaple
# eunice:five
# frank:anotherpassword
# grant:password1234
# harry:1234asdf
# irene:qwerty
# jack:jackspassword
# [None, None, None, None, None, None, None, None, None, None, None]


from typing import Dict, List

def table_to_dict(delimiter: str, titletext: str, contentstext: str) -> List[Dict[str, str]]:
    objs = []
    titles = titletext.split(delimiter)
    lines = contentstext.splitlines()
    for line in lines:
        contents = line.split(delimiter)
        if len(contents) != len(titles):
            print("Warning: Invalid record: " + line)
            continue

        obj = {}
        for i in range(len(titles)):
            obj[titles[i].strip()] = contents[i].strip()

        objs.append(obj)
    return objs
