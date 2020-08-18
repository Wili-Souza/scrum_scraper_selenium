def pageNumber(link):
    link_splited = link.split('page=')
    page = link_splited[1]
    return int(page)