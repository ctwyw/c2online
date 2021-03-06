#/bin/env python
#-*-coding:utf-8-*-
import web
from conf import config
import json
import time
from modules import dbHelp
from modules import valids
import math

urls = (
		'', 'ReServers',
        '/',  'Servers',
		'/create/', 'Create',
		'/change/', 'Change',
		'/update/', 'Update',
		'/shortlist/(\d*)', 'ShortList',
		'/history/(\d*)/(\d*)', 'History',
)

#def onload(handler):
#	try:
#		web.ctx.session.uName is None
#	except:
#		if 'HTTP_X_REQUESTED_WITH' in web.ctx.environ and web.ctx.environ['HTTP_X_REQUESTED_WITH'] == 'XMLHttpRequest':
#			return json.dumps({'res' : 'error', 'msg' : '您已经退出登录，请<a href="/index?login">重新登录</a>'})
#		else:
#			web.seeother('/index?login', True)
#
#	return handler()

render = config.render
appServers = web.application(urls, globals())
#appServers.add_processor(onload)

class ReServers(object):
	def GET(self): raise web.redirect('/')

class Servers(object):
	def GET(self):
		try:
			dbase = dbHelp.DbHelp()
			db = dbase.database()
			slist = db.select('c2_server', order='s_status, s_cdateline desc')
			if len(slist) == 0:
				slist = ''
			#return render.servers(slist = slist, ac = 3, logUserInfo = web.ctx.session)
			return render.servers(slist = slist, ac = 3)
		except:
			#return render.servers(ac = 3, logUserInfo = web.ctx.session)
			return render.servers(ac = 3)

class Create(object):
	def POST(self):
		inputs = web.input()
		pId = inputs['pid'].strip()
		sname = inputs['sname'].strip()
		pdir = inputs['pdir'].strip()
		bdir = inputs['bdir'].strip()
		spath = inputs['spath'].strip()
		suser = inputs['suser'].strip()
		spass = inputs['spass'].strip()
		v = valids.Valids()

		if v.isEmpty(pId) or \
			v.isEmpty(sname) or \
			v.isEmpty(pdir) or \
			v.isEmpty(bdir) or \
			v.isEmpty(spath) or \
			v.isEmpty(suser) or \
			v.isEmpty(spass):
			return json.dumps({'res' : 0, 'msg' : '带*不能为空'})

		#入库操作
		try:
			dbase = dbHelp.DbHelp()
			db = dbase.database()
			#查看pid是否真实存在
			res = db.select('c2_project', what = 'p_name', where = 'p_id = $pId', limit = 1, vars = locals())
			if len(res) < 1:
				return json.dumps({'res' : 0, 'msg' : '对应项目不存在'})

			pname = res[0].p_name
			#查看是否重名
			rs = db.select('c2_server', what = 's_id', where = 's_name = $sname', limit = 1, vars = locals())
			if len(rs) > 0:
				return json.dumps({'res' : 0, 'msg' : '该服务器名称已经存在'})

			pData = {'p_id' : pId, 
					's_name' : sname, 
					's_host' : spath, 
					's_user' : suser, 
					's_pass' : spass, 
					's_pdir' : pdir, 
					's_bdir' : bdir, 
					's_cdateline' : time.time(), 
					's_status' : 1,
					'p_name' : pname}
			if 'svpn' in inputs:
				pData['s_vpn'] = inputs['svpn'].strip()

			if 'svpnname' in inputs:
				pData['s_vpnuser'] = inputs['svpnname'].strip()

			if 'svpnpass' in inputs:
				pData['s_vpnpass'] = inputs['svpnpass'].strip()

			res = db.insert('c2_server', **pData)

			return json.dumps({'res' : 1})
		except:
			return json.dumps({'res' : 0, 'msg' : '系统错误'})

class Change(object):
	def POST(self):
		inputs = web.input()
		status = 1
		if len(inputs['checkboxs']) == 0:
			return json.dumps({'res' : 0, 'msg' : '请至少选择一项'})

		if len(inputs['status']) > 0:
			status = inputs['status'].strip()

		#修改数据库
		try:
			ids = inputs['checkboxs'].strip().split('|')
			dbase = dbHelp.DbHelp()
			db = dbase.database()
			db.update('c2_server', s_status = status, where = 's_id IN $ids', vars=locals())
			return json.dumps({'res' : 1})
		except:
			return json.dumps({'res' : 0, 'msg' : '系统错误'})

class Update(object):
	def POST(self):
		inputs = web.input()
		name = inputs['name'].strip()
		id = inputs['id'].strip()
		val = inputs['val'].strip()
		v = valids.Valids()

		if (v.isEmpty(name) or \
			v.isEmpty(id) or \
			v.isEmpty(val)) and name.find('vpn') == -1:
			return json.dumps({'res' : 0, 'msg' : '数据不合法'})

		#修改数据
		try:
			if name == 'pdir':
				dVal = {'s_pdir' : val}
			elif name == 'bdir':
				dVal = {'s_bdir' : val}
			elif name == 'host':
				dVal = {'s_host': val}
			elif name == 'user':
				dVal = {'s_user': val}
			elif name == 'pass':
				dVal = {'s_pass': val}
			elif name == 'vpn':
				dVal = {'s_vpn': val}
			elif name == 'vpnuser':
				dVal = {'s_vpnuser': val}
			elif name == 'vpnpass':
				dVal = {'s_vpnpass': val}
			else:
				return json.dumps({'res' : 0, 'msg' : '数据不合法'})

			dbase = dbHelp.DbHelp()
			db = dbase.database()
			db.update('c2_server', where = 's_id = $id', vars = locals(), **dVal)
			return json.dumps({'res' : 1})
		except:
			return json.dumps({'res' : 0, 'msg' : '系统错误'})

class ShortList(object):
	def GET(self, pId):
		'''取数据库服务器列表信息'''
		v = valids.Valids()
		pId = pId.strip()
		if v.isEmpty(pId):
			return json.dumps({'res' : 0, 'msg' : '参数不合法'})

		try:
			dbase = dbHelp.DbHelp()
			db = dbase.database()
			plist = db.select('c2_server', what = 's_id, s_name', where = 's_status = 1 AND p_id = $pId', order='s_cdateline desc', vars = locals())
			if len(plist) == 0:
				return json.dumps({'res' : 0, 'msg' : '暂无服务器列表，请先创建服务器'})

			return json.dumps({'res' : 1, 'list' : [l for l in plist]})
		except:
			return json.dumps({'res' : 0, 'msg' : '服务器列表读取失败'})

class History:
	def GET(self, sId, page = None):
		'''取数据库发布列表信息'''
		v = valids.Valids()
		sId = sId.strip()
		if v.isEmpty(sId):
			return json.dumps({'res' : 0, 'msg' : '参数不合法'})

		if page == '':
			page = 1

		page = int(page)

		eachPage = 10

		try:
			dbase = dbHelp.DbHelp()
			db = dbase.database()
			#查看发布总数
			ct = db.select('c2_log', what = 'COUNT(*) AS c', where = 's_id = $sId', vars = locals())
			allNums = ct[0].c
			if allNums <= 0: 
				return json.dumps({'res' : 0, 'msg' : '暂无发布历史'})

			#最大页数
			maxPage = int(math.ceil(float(allNums)/eachPage))
			if page > maxPage:
				page = maxPage

			slist = db.select('c2_log', what = '*', where = 's_id = $sId', limit = '%d, %d' % ((page-1)*eachPage, eachPage),  order='r_dateline desc', vars = locals())
			if len(slist) == 0:
				return json.dumps({'res' : 0, 'msg' : '暂无发布历史'})

			return json.dumps({'res' : 1, 'list' : [l for l in slist], 'maxPage' : maxPage})
		except:
			return json.dumps({'res' : 0, 'msg' : '发布历史列表读取失败'})
