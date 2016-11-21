#!/usr/bin/python 
#coding:utf-8

from api import app
import utils
import db

config = utils.get_config('api')
#print config

#将自定义的配置文件全部加载到全局的大字典app.config中，可以在任意地方调用
app.config.update(config)

#实例化数据库类，并将实例化的对象导入配置
app.config['db'] = db.Cursor(config)
print app.config

utils.write_log('web').info("just a test")
utils.write_log('api').error("have a error")

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=int(app.config['port']),debug=False)
