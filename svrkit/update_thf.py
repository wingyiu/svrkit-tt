# -*- coding: utf-8 -*-

from svrkit.autogen import *

if __name__ == '__main__':
    # 从参数获取service_name
    service_name = sys.argv[1]
    #
    tpl_data = gen_tpl_data(service_name)
    # 编译thf
    compile_thf(service_name)
    #
    add_methods(service_name, tpl_data)
    # 生产client文件
    gen_client(service_name, tpl_data)
