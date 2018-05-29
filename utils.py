from jinja2 import Template

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
    status, content = fetch(filename)
    return status, content

def fetch(filename):
    cache_content = fetch_cache(filename)
    if (cache_content):
        print('Fetched {} from cache'.format(filename)) 
        return '200 OK', cache_content
    server_content = fetch_server(filename)
    if (server_content):
        save_cache(filename, server_content)
        return '200 OK', server_content
    return '404 Not Found', server_content

def fetch_cache(filename):
    try:
        with open('./cache' + filename) as f:
            return f.read()
    except FileNotFoundError:
        return None

def fetch_server(filename):
    with open('./templates' + filename) as f:
        template = Template(f.read())
    rendered = template.render(username='Kasheem Lew')
    save_cache(filename, rendered)
    return rendered

def save_cache(filename, content):
    with open('./cache' + filename, 'w') as f:
        f.write(content)
    print('Save {} in cache'.format(filename))