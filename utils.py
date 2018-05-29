def resolve_req(req):
    headers_list = [x for x in req.split('\n') if x.strip() != '']
    headers_dict = dict()
    for header in headers_list:
        try:
            colon_index = header.index(':')
            headers_dict[header[:colon_index].strip()] = header[colon_index+1:].strip()
        except ValueError:
            headers_dict['REQ'] = header
    return headers_dict

def route(path):
    filename = path.split()[1]
    if (filename == '/'):
        filename = '/index.html'
    with open('./templates' + filename) as f:
        content = f.read()
    return content