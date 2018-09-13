import os

import requests
import config
from lxml import html


def get_all_solved_problems():
    no_login_session = requests.session()
    page = no_login_session.get(config.infoarena_user_url + config.username_url, params={
        'action': 'stats'
    })
    tree = html.fromstring(page.content)
    problems = tree.xpath('//*[@id="main"]/div[2]/*[text() = \'Probleme rezolvate\']/following-sibling::h3[text() = '
                          '\'Probleme incercate\']/preceding-sibling::span[preceding-sibling::span]/a/text()')
    return problems


def get_last_solved_source_id(problem_name):
    return get_solved_source_id(problem_name)[0]


def get_solved_source_id(problem_name):
    no_login_session = requests.session()
    page = no_login_session.get(config.infoarena_monitor_url, params={
        'task': problem_name,
        'user': config.username
    })

    tree = html.fromstring(page.content)
    sources = tree.xpath('//*[@id="monitor-table"]/table/tbody/tr/td[7]/a/span[text() = \'Evaluare completa: 100 '
                         'puncte\']/parent::a/parent::td/parent::tr/td[1]/a/text()')
    int_sources = []
    for i in sources:
        int_sources.append(int(i[1:]))
    return int_sources


def get_source_code(source_id):
    no_login_session = requests.session()
    page = no_login_session.post('https://www.infoarena.ro/job_detail/' + str(source_id), config.no_login_data, params={
        'action': 'view-source'
    })
    tree = html.fromstring(page.content)
    source_code = tree.xpath('/html/body/div[1]/div[3]/div[2]/div[2]/textarea/text()')
    return source_code[0]


def get_source_code_language(source_id):
    no_login_session = requests.session()
    page = no_login_session.post('https://www.infoarena.ro/job_detail/' + str(source_id), config.no_login_data, params={
        'action': 'view-source'
    })
    tree = html.fromstring(page.content)
    source_code = tree.xpath('//td[@class=\'compiler-id\']/text()')
    return source_code[0]


def save_source_code(source_id, problem_name):
    # if path to sources does not exist, create one
    if not os.path.exists(config.sources_directory):
        os.makedirs(config.sources_directory)
    # if path of problem does not exist, create one
    if not os.path.exists(config.sources_directory + '/' + problem_name):
        os.makedirs(config.sources_directory + '/' + problem_name)
    file_director = config.sources_directory + '/' + problem_name + '/'
    file_name = problem_name + '.' + get_source_code_language(source_id)
    with open(file_director + file_name, "w") as file:
        file.write(get_source_code(source_id))
    pass


def check_if_already_downloaded(problem_name):
    file_director = config.sources_directory + '/' + problem_name + '/'
    file_path = file_director + problem_name
    exists = (os.path.exists(file_path + '.cpp') and os.stat(file_path + '.cpp').st_size != 0) or \
        (os.path.exists(file_path + '.c') and os.stat(file_path + '.c').st_size != 0) or \
        (os.path.exists(file_path + '.pas') and os.stat(file_path + '.pas').st_size != 0) or \
        (os.path.exists(file_path + '.java') and os.stat(file_path + '.java').st_size != 0)
    return exists


def main():
    solved_problems = get_all_solved_problems()
    print('Gasit %d probleme rezolvate pe contul %s' % (len(solved_problems), config.username))
    for i in solved_problems:
        print('%-25s' % config.Colors.bold(i), end=' ')
        if check_if_already_downloaded(i):
            if not config.overwrite_flag:
                print(config.Colors.warning(u'\u2713'), end=' ')
                print(config.Colors.ok_blue('     exista deja'))
                continue
        source_id = get_last_solved_source_id(i)
        save_source_code(source_id, i)
        print(config.Colors.ok_green(u'\u2713'), end=' ')
        print('%25s' % config.Colors.ok_blue(source_id))
    pass


if __name__ == '__main__':
    main()
    # print(save_source_code(2240199, 'adunare'))
