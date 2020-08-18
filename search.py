from enum import Enum, auto

def searchScrum (s_name, s_tag, s_type):

    class id_tags(Enum):
        _148 = 'backlog'
        _141 = 'development team'
        _144 = 'daily scrum'
        _149 = 'definition of done'
        _153 = 'leadership'
        _140 = 'product owner'
        _156 = 'refinement'
        _150 = 'scaling'
        _139 = 'scrum master'
        _151 = 'scrum values'
        _155 = 'scrum with devops'
        _152 = 'scrum with kanban'
        _154 = 'sprint goal'
        _143 = 'sprint planning'
        _146 = 'sprint retrospective'
        _145 = 'sprint review'
        _202 = 'user experience'

    class id_types(Enum):
        _98 = 'blog'
        _86 = 'book'
        _69 = 'case study'
        _70 = 'datasheet'
        _91 = 'glossary'
        _90 = 'guide'
        _87 = 'infographic'
        _115 = 'podcast'
        _88 = 'poster'
        _100 = 'publication'
        _128 = 'slides'
        _101 = 'video'
        _129 = 'web page'
        _116 = 'web cast'
        _71 = 'whitepaper'

    #busca no site
    search = ''

    search_name = s_name.lower()
    search_tag = s_tag.lower()
    search_type = s_type.lower()

    if search_name.strip() != '':
        search = f'search={search_name}&'

    for i in id_tags:
        if i.value == search_tag.strip():
            id_tag = i.name.replace('_', '') 
            search += f'field_resource_tags_target_id={id_tag}&'
            break

    for i in id_types:
        if i.value == search_type.strip():
            id_type = i.name.replace('_', '') 
            search += f'type={id_type}&'
            break
    
    return search

