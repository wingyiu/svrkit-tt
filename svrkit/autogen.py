# -*- coding: utf-8 -*-
import os
import sys
import importlib
from jinja2 import Environment, FileSystemLoader


def gen_dir(service_name):
    service_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../app/' + service_name)
    if os.path.exists(service_dir):
        return
    # 创建
    os.makedirs(service_dir)
    print('create dir %s' % service_dir)


def gen_thf(service_name, tpl_data):
    thf_out_fp = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              '../app/' + service_name + '/' + service_name + '.thrift')
    thf_out_fp = os.path.realpath(thf_out_fp)
    #
    tpl_dir = os.path.dirname(os.path.abspath(__file__))
    jinja2 = Environment(loader=FileSystemLoader(tpl_dir), trim_blocks=True)
    thf_template = jinja2.get_template('thrift.tpl')
    thf_file_content = thf_template.render(tpl_data)
    print('output thf: %s' % thf_out_fp)
    # 写
    with open(thf_out_fp, 'w+') as f:
        f.write(thf_file_content)


def compile_thf(service_name):
    thf_out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')
    thf_out_dir = os.path.realpath(thf_out_dir)
    cmd = 'thrift -r -out {0} --gen py:tornado app/{1}/{1}.thrift'.format(thf_out_dir, service_name)
    print('gen thrift files: %s' % cmd)
    os.system(cmd)


def gen_tpl_data(service_name):
    #
    service_cls_name = service_name.title() + 'Service'
    client_cls_name = service_name.title() + 'Client'
    handler_cls_name = service_name.title() + 'Handler'
    tpl_data = {
        'service_name': service_name,
        'service_cls_name': service_cls_name,
        'client_cls_name': client_cls_name,
        'handler_cls_name': handler_cls_name,
        'methods': []
    }
    return tpl_data


def add_methods(service_name, tpl_data):
    service_mod_name = 'app.{}.thf.{}'.format(service_name, tpl_data['service_cls_name'])
    service_mod = importlib.import_module(service_mod_name)
    iface = getattr(service_mod, 'Iface')
    for attr_n in iface.__dict__:
        attr = iface.__dict__[attr_n]
        if callable(attr):
            method = {}
            method['doc'] = attr.__doc__.replace('    ', '        ')
            method['name'] = attr.__name__
            method['args'] = attr.func_code.co_varnames
            tpl_data['methods'].append(method)


def gen_client(service_name, tpl_data):
    # client模板
    client_out_fp = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../app/' + service_name + '/client.py')
    client_out_fp = os.path.realpath(client_out_fp)
    #
    tpl_dir = os.path.dirname(os.path.abspath(__file__))
    jinja2 = Environment(loader=FileSystemLoader(tpl_dir), trim_blocks=True)
    client_template = jinja2.get_template('client.tpl')
    client_file_content = client_template.render(tpl_data)
    print('output client: %s' % client_out_fp)
    # 写
    with open(client_out_fp, 'w+') as f:
        f.write(client_file_content)


def gen_handler(service_name, tpl_data):
    #
    handler_out_fp = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../app/' + service_name + '/handler.py')
    handler_out_fp = os.path.realpath(handler_out_fp)
    #
    tpl_dir = os.path.dirname(os.path.abspath(__file__))
    jinja2 = Environment(loader=FileSystemLoader(tpl_dir), trim_blocks=True)
    handler_template = jinja2.get_template('handler.tpl')
    handler_file_content = handler_template.render(tpl_data)
    print('output handler: %s' % handler_out_fp)
    # 写
    with open(handler_out_fp, 'w+') as f:
        f.write(handler_file_content)


if __name__ == '__main__':
    # 从参数获取service_name
    service_name = sys.argv[1]
    #
    tpl_data = gen_tpl_data(service_name)
    # 生产文件夹
    gen_dir(service_name)
    #
    gen_thf(service_name, tpl_data)
    # 编译thf
    compile_thf(service_name)
    #
    add_methods(service_name, tpl_data)
    # 生产client文件
    gen_client(service_name, tpl_data)
    # 生产handler文件
    gen_handler(service_name, tpl_data)
