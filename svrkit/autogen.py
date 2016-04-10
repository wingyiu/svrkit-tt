# -*- coding: utf-8 -*-
import subprocess
import os
import sys
import importlib

from jinja2 import Environment, FileSystemLoader

if __name__ == '__main__':
    # 从参数获取service_name
    service_name = sys.argv[1]
    #
    thf_out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')
    thf_out_dir = os.path.realpath(thf_out_dir)
    cmd = 'thrift -r -out {0} --gen py:tornado app/{1}/{1}.thrift'.format(thf_out_dir, service_name)
    print('gen thrift files: %s' % cmd)
    os.system(cmd)
    # 根据service_name生产各种路径等
    client_out_fp = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../app/' + service_name + '/client.py')
    client_out_fp = os.path.realpath(client_out_fp)
    client_cls_name = service_name.title() + 'Client'
    service_cls_name = service_name.title() + 'Service'
    service_mod_name = 'app.{}.thf.{}'.format(service_name, service_cls_name)
    service_mod = importlib.import_module(service_mod_name)
    # print(service_mod)

    client_tpl_data = {'client_cls_name': client_cls_name,
                        'service_name': service_name,
                       'service_cls_name': service_cls_name,
                       'methods': []
                       }
    iface = getattr(service_mod, 'Iface')
    # print(iface.__dict__)
    for attr_n in iface.__dict__:
        attr = iface.__dict__[attr_n]
        if callable(attr):
            method = {}
            method['doc'] = attr.__doc__.replace('    ', '        ')
            method['name'] = attr.__name__
            method['args'] = attr.func_code.co_varnames
            client_tpl_data['methods'].append(method)

    # client模板
    tpl_dir = os.path.dirname(os.path.abspath(__file__))
    # print(tpl_dir)
    jinja2 = Environment(loader=FileSystemLoader(tpl_dir), trim_blocks=True)
    client_template = jinja2.get_template('client.tpl')
    client_file_content = client_template.render(client_tpl_data)
    # print(client_file_content)
    print('output client: %s' % client_out_fp)
    # 写
    with open(client_out_fp, 'w+') as f:
        f.write(client_file_content)