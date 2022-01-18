# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
import pymysql
import datetime
import smtplib
from email.mime.text import MIMEText

def sendEmail(mail_host,mail_user,mail_pass,sender,receiver,send_text):
    #设置email信息

    #邮件内容设置
    message = MIMEText(send_text,'html','utf-8')
    #邮件主题
    message['Subject'] = send_text
    #发送方信息
    message['From'] = sender
    #接受方信息
    #receivers_str=';'.join(receivers)
    message['To'] = receiver

    #登录并发送邮件
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host,465)
        #连接到服务器
        #smtpObj.connect()
        #登录到服务器
        smtpObj.login(mail_user,mail_pass)
        #发送
        smtpObj.sendmail(
            sender,receiver,message.as_string())
        #退出
        smtpObj.quit()
        print('send email successfully')
    except smtplib.SMTPException as e:
        print('error',e) #打印错误

# 表单
def search_form(request):
    return render(request, 'search_form.html')

def deepsearch_form(request):
    return render(request,'deep_search_form.html')

dic_qxname={"HP":"黄浦","XH":"徐汇","CN":"长宁","JA":"静安","PT":"普陀","HK":"虹口","YP":"杨浦","MH":"闵行","BS":"宝山","JD":"嘉定","PD":"浦东","JS":"金山","SJ":"松江","QP":"青浦","FX":"奉贤","CM":"崇明","KQ":"跨区"}
cand_catename={"gczcb_html":"工程总承包","sgcb_html":"施工承包","kcsjhbzb_html":"勘察设计合并","sjzb_html":"设计招标",\
               "jlzb_html":"监理招标","kczb_html":"勘察招标","sgzgj_html":"暂估价工程",\
               "sg_pdf":"施工承包","jl_pdf":"监理招标","sgzgj_pdf":"暂估价工程"}
# 接收请求数据
def search(request):
    request.encoding = 'utf-8'
    if 'projName' in request.GET and request.GET['projName']:
        projName_key=request.GET['projName']
        # 打开数据库连接
        db = pymysql.connect(host="localhost", user="usr_bidinfo", password="20201203", database="db_bidinfo")
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        ret_cont=''
        if projName_key!="今日":
            keywords = projName_key.split(' ')
            kw_str = "%"
            for kw in keywords:
                kw_str += kw + "%"

            sql_bidinfo = 'select constructno,projname,bidcate,projinvestment,bidconsprice,infodate,originurl,bidsectionno from tb_bidinfo where projname like "' + kw_str + '"'
            sql_bidplan = 'select zbxmmc,ztz,jaf,nkszbsj,timeflag,xmssqx,id from tb_bidplan where zbxmmc like "'+kw_str+'"'


            try:
                #查询tb_bidinfo表中数据
                ret_cont="<h2>招标信息</h2>"
                cursor.execute(sql_bidinfo)
                results_info = cursor.fetchall()
                if not results_info:
                    ret_cont = ret_cont+"无招标公示数据"
                else:
                    recordNum=len(results_info)
                    ret_cont=ret_cont + "<p>共有<font color='blue'><u>"+str(recordNum)+"</u></font>条记录</p><table boder='1'><tr><th>序号</th><th>报建编号</th><th>项目名称</th><th>招标类型</th><th>工程总投资</th><th>建安费用</th><th>发布日期</th><th>网页链接</th><th>中标候选</th><th>中标结果</th></tr>"
                    xuhao = 1
                    for row in results_info:
                        bidresult_url=""
                        constructno,bidsectionno=row[0],row[7]
                        sql_result="select originurl from tb_bidresult where constructno='"+constructno+"' and bidsectionno='"+bidsectionno+"'"
                        sql_bidcand="select originurl from tb_bidcand where constructno='"+constructno+"' and bidsectionno='"+bidsectionno+"'"
                        cursor.execute(sql_bidcand)
                        bidcand_res=cursor.fetchall()
                        cursor.execute(sql_result)
                        bidresults = cursor.fetchall()
                        #print(sql_result)
                        bidcand_url="无"
                        bidresult_url="无"
                        if not bidcand_res and not bidresults:
                            ret_cont = ret_cont + "<tr><td>" + str(xuhao) + "</td><td>" + row[0] + "</td><td>" + row[1] \
                                       + "</td><td>" + row[2] + "</td><td>" + row[3] + "</td><td>" + row[4] + "</td><td>" \
                                       + str(row[5]) + "</td><td><a href='" + row[6] + "'>招标网页</td><td>无</td><td>无</td></tr>"
                        elif not bidcand_res and bidresults:
                            bidresult_url=bidresults[0][0]
                            ret_cont = ret_cont + "<tr><td>"+str(xuhao)+"</td><td>"  + row[0] + "</td><td>" + row[1] \
                                       + "</td><td>" + row[2] + "</td><td>" + row[3] +"</td><td>" + row[4] +"</td><td>" \
                                       + str(row[5]) +"</td><td><a href='" + row[6] + "'>招标网页</td><td>无</td><td><a href='" \
                                       + bidresult_url + "'>中标结果</td></tr>"
                        elif bidcand_res and not bidresults:
                            bidcand_url=bidcand_res[0][0]
                            ret_cont = ret_cont + "<tr><td>"+str(xuhao)+"</td><td>"  + row[0] + "</td><td>" + row[1] \
                                       + "</td><td>" + row[2] + "</td><td>" + row[3] +"</td><td>" + row[4] +"</td><td>" \
                                       + str(row[5]) +"</td><td><a href='" + row[6] + "'>招标网页</td><td><a href='" \
                                       + bidcand_url + "'>中标候选</td><td>无</td></tr>"
                        else:
                            bidcand_url = bidcand_res[0][0]
                            bidresult_url = bidresults[0][0]
                            ret_cont = ret_cont + "<tr><td>" + str(xuhao) + "</td><td>" + row[0] + "</td><td>" + row[1] \
                                       + "</td><td>" + row[2] + "</td><td>" + row[3] + "</td><td>" + row[4] + "</td><td>" \
                                       + str(row[5]) + "</td><td><a href='" + row[6] + "'>招标网页</td><td><a href='" \
                                       + bidcand_url + "'>中标候选</td><td><a href='"+ bidresult_url + "'>中标结果</td></tr>"
                        xuhao+=1
                    ret_cont=ret_cont+"</table>"
                #查询tb_bidplan表中数据
                cursor.execute(sql_bidplan)
                ret_cont = ret_cont+"<h2>招标计划</h2>"
                results_plan=cursor.fetchall()
                if not results_plan:
                    ret_cont=ret_cont+"无招标计划数据"
                else:
                    planNum=len(results_plan)
                    ret_cont = ret_cont + "<p>共有<font color='blue'><u>" + str(planNum) + "</u></font>条记录</p><table boder='1'><tr><th>序号</th><th>项目名称</th><th>总投资</th><th>建安费</th><th>拟开始招标日期</th><th>计划发布日期</th><th>项目区县</th><th>网页链接</th></tr>"
                    xuhao=1
                    for row in results_plan:
                        link_str="https://ciac.zjw.sh.gov.cn/XMJYPTInterWeb/Zbjh/GlyhZbjhQuery?id="+row[6]+"&lcd=1"
                        if row[5] in dic_qxname.keys():
                            qxname_str=dic_qxname[row[5]]
                        else:
                            qxname_str=row[5]
                        ret_cont = ret_cont + "<tr><td>"+str(xuhao)+"</td><td>"  + row[0] + "</td><td>" + row[1] + "万</td><td>" \
                                   + row[2] + "万</td><td>" + row[3] +"</td><td>" + row[4] +"</td><td>" \
                                   + qxname_str +"</td><td><a href='" + link_str + "'>网页链接</td></tr>"
                        xuhao+=1
                    ret_cont=ret_cont+"</table>"
                cursor.close()
            except pymysql.Error as e:
                ret_cont = str(e.args[0]) + str(e.args[1])
            db.close()
        else:
            d = datetime.date.today()
            today_str = d.isoformat()
            #招标公示
            sql_bidinfo = 'select constructno,projname,bidcate,projinvestment,bidconsprice,infodate,originurl from tb_bidinfo where infodate="' + today_str + '"'

            cursor.execute(sql_bidinfo)
            results_info=cursor.fetchall()
            ret_cont = "<h2>招标信息</h2>"
            if not results_info:
                ret_cont = ret_cont + "无招标公示数据"
            else:
                recordNum = len(results_info)
                ret_cont = ret_cont + "<p>共有<font color='blue'><u>" + str(recordNum) + \
                           "</u></font>条记录</p><table boder='1'><tr><th>序号</th><th>报建编号</th><th>项目名称</th>\
                           <th>招标类型</th><th>工程总投资</th><th>建安费用</th><th>发布日期</th><th>网页链接</th></tr>"
                xuhao = 1
                for row in results_info:
                    ret_cont = ret_cont + "<tr><td>" + str(xuhao) + "</td><td>" + row[0] + "</td><td>" + row[1] \
                               + "</td><td>" + row[2] + "</td><td>" + row[3] + "</td><td>" + row[4] + "</td><td>" \
                               + str(row[5]) + "</td><td><a href='" + row[6] + "'>招标网页</td></tr>"
                    xuhao += 1
                ret_cont = ret_cont + "</table>"
            #中标候选信息
            sql_bidcand = 'select constructno,projname,bidcate,no1cand,no1price,no2cand,no2price,originurl from tb_bidcand where infodate="' + today_str + '"'
            cursor.execute(sql_bidcand)
            results_cand=cursor.fetchall()
            ret_cont = ret_cont+"<h2>中标候选信息</h2>"
            if not results_cand:
                ret_cont=ret_cont+"无中标候选信息"
            else:
                recordNum = len(results_cand)
                ret_cont = ret_cont + "<p>共有<font color='blue'><u>" + str(recordNum) + \
                           "</u></font>条记录</p><table boder='1'><tr><th>序号</th><th>报建编号</th><th>项目名称</th>\
                           <th>招标类型</th><th>第一中标候选人</th><th>第一候选投标价</th><th>第二中标候选人</th><th>第二候选投标价</th><th>网页链接</th></tr>"
                xuhao = 1
                for row in results_cand:
                    try:
                        catename=cand_catename[row[2]]
                    except KeyError:
                        catename=row[2]
                        errorText='新中标候选 招标类型信息'+row[2]
                        sendEmail("smtp.yeah.net", "bidinfo", "FTFXMKFXVSQBMJSM", "bidinfo@yeah.net",
                                  "3233964153@qq.com", errorText)
                    if row[5] and row[6]:
                        ret_cont = ret_cont + "<tr><td>" + str(xuhao) + "</td><td>" + row[0] + "</td><td>" + row[1] \
                               + "</td><td>" + catename + "</td><td>" + row[3] + "</td><td>" + row[4] + "万元</td><td>" \
                               + row[5] + "</td><td>"+ row[6] + "万元</td><td><a href='" + row[7] + "'>网页链接</td></tr>"
                    else:
                        ret_cont = ret_cont + "<tr><td>" + str(xuhao) + "</td><td>" + row[0] + "</td><td>" + row[1] \
                                   + "</td><td>" + catename + "</td><td>" + row[3] + "</td><td>" + row[4] + "万元</td><td>无</td><td>无</td>"\
                                   +"<td><a href='" + row[7] + "'>网页链接</td></tr>"
                    xuhao += 1
                ret_cont = ret_cont + "</table>"
            #中标结果信息
            d = datetime.date.today()
            today_str_res = d.strftime("%Y年%m月%d日")
            sql_bidresult = 'select constructno,projname,bidcate,winner,winprice,originurl from tb_bidresult where windate="' + today_str_res + '"'
            cursor.execute(sql_bidresult)
            results_bidresult = cursor.fetchall()
            ret_cont = ret_cont + "<h2>中标结果</h2>"
            if not results_bidresult:
                ret_cont = ret_cont + "无中标结果信息"
            else:
                recordNum = len(results_bidresult)
                ret_cont = ret_cont + "<p>共有<font color='blue'><u>" + str(recordNum) + \
                           "</u></font>条记录</p><table boder='1'><tr><th>序号</th><th>报建编号</th><th>项目名称</th>\
                           <th>招标类型</th><th>中标人</th><th>中标价</th><th>网页链接</th></tr>"
                xuhao = 1
                for row in results_bidresult:
                    ret_cont = ret_cont + "<tr><td>" + str(xuhao) + "</td><td>" + row[0] + "</td><td>" + row[1] \
                               + "</td><td>" + row[2] + "</td><td>" + row[3] + "</td><td>" + row[4] + \
                               "</td><td><a href='" + row[5] + "'>网页链接</td></tr>"
                    xuhao += 1
                ret_cont = ret_cont + "</table>"
            #招标计划
            sql_bidplan = 'select zbxmmc,ztz,jaf,nkszbsj,timeflag,xmssqx,id from tb_bidplan where timeflag ="' + today_str + '"'
            cursor.execute(sql_bidplan)
            results_bidplan = cursor.fetchall()
            ret_cont = ret_cont + "<h2>招标计划</h2>"
            if not results_bidplan:
                ret_cont = ret_cont + "招标计划"
            else:
                recordNum = len(results_bidplan)
                ret_cont = ret_cont + "<p>共有<font color='blue'><u>" + str(recordNum) + "</u></font>条记录</p><table boder='1'><tr><th>序号</th><th>项目名称</th><th>总投资</th><th>建安费</th><th>拟开始招标日期</th><th>计划发布日期</th><th>项目区县</th><th>网页链接</th></tr>"
                xuhao=1
                for row in results_bidplan:
                    link_str = "https://ciac.zjw.sh.gov.cn/XMJYPTInterWeb/Zbjh/GlyhZbjhQuery?id=" + row[6] + "&lcd=1"
                    if row[5] in dic_qxname.keys():
                        try:
                            qxname_str = dic_qxname[row[5]]
                        except KeyError:
                            qxname_str = row[5]
                            errorText = '招标计划 区县简写' + row[5]
                            sendEmail("smtp.yeah.net", "bidinfo", "FTFXMKFXVSQBMJSM", "bidinfo@yeah.net",
                                      "3233964153@qq.com", errorText)
                    else:
                        qxname_str = row[5]
                    ret_cont = ret_cont + "<tr><td>" + str(xuhao) + "</td><td>" + row[0] + "</td><td>" + row[1] + "万</td><td>" \
                               + row[2] + "万</td><td>" + row[3] + "</td><td>" + row[4] + "</td><td>" \
                               + qxname_str + "</td><td><a href='" + link_str + "'>网页链接</td></tr>"
                    xuhao += 1
                ret_cont = ret_cont + "</table>"
    else:
        ret_cont = '未填写搜索信息，请重试'
    return HttpResponse(ret_cont)

def deepsearch(request):
    """
    深度搜索方法，利用项目名称、招标人、代理名称、中标候选人、中标公司等关键字，搜索tb_bidinfo、tb_bidcands、tb_bidresult三张表
    :param request:
    :return:
    """
    request.encoding = 'utf-8'
    info_conditions_lst=[]
    cand_conditions_lst=[]
    result_conditions_lst=[]
    cand_conditions_lst_res=[]

    involveBidInfo=False
    involveBidCands=False
    involveBidResult=False

    if 'projName' in request.GET and request.GET['projName']:
        tmp_str=request.GET['projName'].replace(' ','')
        if tmp_str:
            involveBidInfo = True
        projName_key=request.GET['projName'].strip()
        keywords = projName_key.split(' ')
        kw_str = "%"
        for kw in keywords:
            kw_str += kw + "%"
        info_str_tmp='projname like "'+kw_str+'"'
        cand_str_tmp='a.projname like "'+kw_str+'"'
        info_conditions_lst.append(info_str_tmp)
        cand_conditions_lst.append(cand_str_tmp)
        result_conditions_lst.append(cand_str_tmp)

    if 'bidCompanyName' in request.GET and request.GET['bidCompanyName']:
        tmp_str = request.GET['bidCompanyName'].replace(' ', '')
        if tmp_str:
            involveBidInfo = True
        bidcompName_key = request.GET['bidCompanyName'].strip()
        keywords = bidcompName_key.split(' ')
        kw_str = "%"
        for kw in keywords:
            kw_str += kw + "%"
        info_str_tmp = 'bidcompany like "' + kw_str + '"'
        cand_str_tmp='a.bidcompany like "'+kw_str+'"'
        info_conditions_lst.append(info_str_tmp)
        cand_conditions_lst.append(cand_str_tmp)
        result_conditions_lst.append(cand_str_tmp)

    if 'bidAgent' in request.GET and request.GET['bidAgent']:
        tmp_str = request.GET['bidAgent'].replace(' ', '')
        if tmp_str:
            involveBidInfo = True
        agentName_key = request.GET['bidAgent'].strip()
        keywords = agentName_key.split(' ')
        kw_str = "%"
        for kw in keywords:
            kw_str += kw + "%"
        info_str_tmp = 'bidagent like "' + kw_str + '"'
        cand_str_tmp='a.bidagent like "'+kw_str+'"'
        info_conditions_lst.append(info_str_tmp)
        cand_conditions_lst.append(cand_str_tmp)
        result_conditions_lst.append(cand_str_tmp)

    if 'bidCandName' in request.GET and request.GET['bidCandName']:
        tmp_str = request.GET['bidCandName'].replace(' ', '')
        if tmp_str:
            involveBidCands=True
        bidCand_key=request.GET['bidCandName'].strip()
        keywords = bidCand_key.split(' ')
        kw_str = "%"
        for kw in keywords:
            kw_str += kw + "%"
        cand_condition_str = 'no1cand like "' + kw_str + '"'
        cand_conditions_lst.append('b.no1cand like "'+kw_str+'"')
        cand_conditions_lst_res.append('a.no1cand like "'+kw_str+'"')

    if 'winnerName' in request.GET and request.GET['winnerName']:
        tmp_str = request.GET['winnerName'].replace(' ', '')
        if tmp_str:
            involveBidResult=True
        winnerName_key=request.GET['winnerName'].strip()
        keywords = winnerName_key.split(' ')
        kw_str = "%"
        for kw in keywords:
            kw_str += kw + "%"
        result_condition_str = 'winner like "' + kw_str + '"'
        result_conditions_lst.append('b.winner like "'+kw_str+'"')
        cand_conditions_lst_res.append('b.winner like "'+kw_str+'"')

    info_sql_conditions_str=' and '.join(info_conditions_lst)
    #only招标信息
    if involveBidInfo and not involveBidCands and not involveBidResult:
        sql_bidinfo = 'select constructno,projname,bidcompany,projinvestment,bidagent,infodate,originurl,bidsectionno ' \
                      'from tb_bidinfo where '+info_sql_conditions_str
        ret_cont='nothing'
        # 打开数据库连接
        db = pymysql.connect(host="localhost", user="usr_bidinfo", password="20201203", database="db_bidinfo")
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        try:
            # 查询tb_bidinfo表中数据
            ret_cont = "<h2>招标中标信息</h2>"
            cursor.execute(sql_bidinfo)
            results_info = cursor.fetchall()
            print(results_info)
            if not results_info:
                ret_cont = ret_cont + "无相关招标中标信息"
            else:
                recordNum = len(results_info)
                ret_cont = ret_cont + "<p>共有<font color='blue'><u>" + str(
                    recordNum) + "</u></font>条记录</p><table boder='1'><tr><th>序号</th><th>报建编号</th><th>项目名称</th>" \
                                 "<th>招标人</th><th>工程总投资</th><th>代理机构</th><th>发布日期</th><th>网页链接</th>" \
                                 "<th>中标候选</th><th>中标结果</th></tr>"
                xuhao = 1
                for row in results_info:
                    bidresult_url = ""
                    constructno, bidsectionno = row[0], row[7]
                    sql_result = "select originurl from tb_bidresult where constructno='" + constructno + \
                                 "' and bidsectionno='" + bidsectionno + "'"
                    sql_bidcand = "select originurl from tb_bidcand where constructno='" + constructno + \
                                  "' and bidsectionno='" + bidsectionno + "'"
                    cursor.execute(sql_bidcand)
                    bidcand_res = cursor.fetchall()
                    cursor.execute(sql_result)
                    bidresults = cursor.fetchall()
                    # print(sql_result)
                    bidcand_url = "无"
                    bidresult_url = "无"
                    if not bidcand_res and not bidresults:
                        ret_cont = ret_cont + "<tr><td>" + str(xuhao) + "</td><td>" + row[0] + "</td><td>" + row[1] \
                                   + "</td><td>" + row[2] + "</td><td>" + row[3] + "</td><td>" + row[4] + "</td><td>" \
                                   + str(row[5]) + "</td><td><a href='" + row[6] + "'>招标网页</td><td>无</td><td>无</td></tr>"
                    elif not bidcand_res and bidresults:
                        bidresult_url = bidresults[0][0]
                        ret_cont = ret_cont + "<tr><td>" + str(xuhao) + "</td><td>" + row[0] + "</td><td>" + row[1] \
                                   + "</td><td>" + row[2] + "</td><td>" + row[3] + "</td><td>" + row[4] + "</td><td>" \
                                   + str(row[5]) + "</td><td><a href='" + row[6] + "'>招标网页</td><td>无</td><td><a href='" \
                                   + bidresult_url + "'>中标结果</td></tr>"
                    elif bidcand_res and not bidresults:
                        bidcand_url = bidcand_res[0][0]
                        ret_cont = ret_cont + "<tr><td>" + str(xuhao) + "</td><td>" + row[0] + "</td><td>" + row[1] \
                                   + "</td><td>" + row[2] + "</td><td>" + row[3] + "</td><td>" + row[4] + "</td><td>" \
                                   + str(row[5]) + "</td><td><a href='" + row[6] + "'>招标网页</td><td><a href='" \
                                   + bidcand_url + "'>中标候选</td><td>无</td></tr>"
                    else:
                        bidcand_url = bidcand_res[0][0]
                        bidresult_url = bidresults[0][0]
                        ret_cont = ret_cont + "<tr><td>" + str(xuhao) + "</td><td>" + row[0] + "</td><td>" + row[1] \
                                   + "</td><td>" + row[2] + "</td><td>" + row[3] + "</td><td>" + row[4] + "</td><td>" \
                                   + str(row[5]) + "</td><td><a href='" + row[6] + "'>招标网页</td><td><a href='" \
                                   + bidcand_url + "'>中标候选</td><td><a href='" + bidresult_url + "'>中标结果</td></tr>"
                    xuhao += 1
                ret_cont = ret_cont + "</table>"
            cursor.close()
        except pymysql.Error as e:
            ret_cont = str(e.args[0]) + str(e.args[1])
        db.close()

    #only中标候选
    elif involveBidCands and not involveBidInfo and not involveBidResult:
        sql_str='select constructno,bidsectionno,projname,no1cand,no1price,originurl,infodate from tb_bidcand where '+cand_condition_str
        ret_cont = 'nothing'
        # 打开数据库连接
        db = pymysql.connect(host="localhost", user="usr_bidinfo", password="20201203", database="db_bidinfo")
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        try:
            # 查询tb_bidinfo表中数据
            ret_cont = "<h2>招标中标信息</h2>"
            cursor.execute(sql_str)
            results_info = cursor.fetchall()
            print(results_info)
            if not results_info:
                ret_cont = ret_cont + "无相关招标中标信息"
            else:
                recordNum = len(results_info)
                ret_cont = ret_cont + "<p>共有<font color='blue'><u>" + str(recordNum) + "</u></font>条记录</p>"\
                           +"<table boder='1'><tr><th>序号</th><th>报建编号</th><th>项目名称</th><th>中标候选人</th><th>中标报价</th><th>招标采购人</th><th>代理机构</th><th>发布日期</th><th>招标网页</th><th>中标候选</th><th>中标结果</th></tr>"
                xuhao = 1
                for row in results_info:
                    bidresult_url = ""
                    constructno, bidsectionno,projname,no1cand,no1price,cand_originurl,infodate = \
                        row[0], row[1],row[2],row[3],row[4]+"万元",row[5],row[6]
                    sql_info = "select bidcompany,bidagent,originurl from tb_bidinfo where constructno='" + constructno + "' and bidsectionno='" + bidsectionno + "'"
                    sql_bidresult = "select originurl from tb_bidresult where constructno='" + constructno + "' and bidsectionno='" + bidsectionno + "'"
                    cursor.execute(sql_info)
                    bidinfo_res = cursor.fetchall()
                    cursor.execute(sql_bidresult)
                    bidresult_res = cursor.fetchall()
                    # print(sql_result)
                    bidcand_url = "无"
                    bidresult_url = "无"
                    if not bidresult_res and not bidinfo_res:
                        ret_cont = ret_cont + "<tr><td>" + str(xuhao) + "</td><td>" + constructno + "</td><td>" + projname \
                                   + "</td><td>" + no1cand + "</td><td>" + no1price + "万元</td><td>无</td><td>无</td><td>" \
                                   + str(infodate) + "</td><td>无</td><td><a href='"+cand_originurl+">中标候选</td><td>无</td></tr>"

                    elif not bidresult_res and bidinfo_res:
                        bidcompany=bidinfo_res[0][0]
                        bidagent=bidinfo_res[0][1]
                        bidinfo_url = bidinfo_res[0][2]
                        ret_cont = ret_cont + "<tr><td>" + str(xuhao) + "</td><td>" + constructno + "</td><td>" + projname \
                                   + "</td><td>" + no1cand + "</td><td>" + no1price + "万元</td><td>"+bidcompany+"</td><td>"+bidagent+"</td><td>" \
                                   + str(infodate) + "</td><td><a href='"+bidinfo_url+"'>招标网页</td><td><a href='"+cand_originurl+\
                                   "'>中标候选</td><td>无</td></tr>"

                    elif bidresult_res and not bidinfo_res:
                        bidresult_url = bidresult_res[0][0]
                        ret_cont = ret_cont + "<tr><td>" + str(xuhao) + "</td><td>" + constructno + "</td><td>" + projname \
                                   + "</td><td>" + no1cand + "</td><td>" + no1price + "</td><td>无</td><td>无</td><td>" \
                                   + str(infodate) + "</td><td>无</td><td><a href='"+cand_originurl+\
                                   "'>中标候选</td><td><a href='"+bidresult_url+"'>中标结果</td></tr>"
                    else:
                        bidcompany = bidinfo_res[0][0]
                        bidagent = bidinfo_res[0][1]
                        bidinfo_url = bidinfo_res[0][2]
                        bidresult_url = bidresult_res[0][0]
                        ret_cont = ret_cont + "<tr><td>" + str(xuhao) + "</td><td>" + constructno + "</td><td>" + projname \
                                   + "</td><td>" + no1cand + "</td><td>" + no1price + "</td><td>"+bidcompany+"</td><td>"+bidagent+"</td><td>" \
                                   + str(infodate) + "</td><td><a href='"+bidinfo_url+"'>招标网页</td><td><a href='"+cand_originurl+\
                                   "'>中标候选</td><td><a href='"+bidresult_url+"'>中标结果</td></tr>"
                    xuhao += 1
                ret_cont = ret_cont + "</table>"
            cursor.close()
        except pymysql.Error as e:
            ret_cont = str(e.args[0]) + str(e.args[1])
        db.close()

    #招标信息+中标候选
    elif involveBidInfo and involveBidCands and not involveBidResult:
        sql_conditions_str=' and '.join(cand_conditions_lst)
        sql_str='select a.constructno,a.bidsectionno,a.projname,a.bidcompany,a.bidagent,b.no1cand,b.no1price,a.originurl,b.originurl ' \
                'from tb_bidinfo a join tb_bidcand b on a.constructno=b.constructno and a.bidsectionno=b.bidsectionno ' \
                'where '+sql_conditions_str
        ret_cont = 'nothing'
        # 打开数据库连接
        db = pymysql.connect(host="localhost", user="usr_bidinfo", password="20201203", database="db_bidinfo")
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        try:
            # 查询tb_bidinfo表中数据
            ret_cont = "<h2>招标中标信息</h2>"
            cursor.execute(sql_str)
            results_info = cursor.fetchall()
            #print(results_info)
            if not results_info:
                ret_cont = ret_cont + "无相关招标中标信息"
            else:
                recordNum = len(results_info)
                ret_cont = ret_cont + "<p>共有<font color='blue'><u>" + str(recordNum) + "</u></font>条记录</p>" \
                           + "<table boder='1'><tr><th>序号</th><th>报建编号</th><th>项目名称</th><th>招标采购人</th>" \
                             "<th>招标代理</th><th>中标候选人</th><th>中标报价</th><th>招标网页</th>" \
                             "<th>中标候选</th><th>中标结果</th></tr>"
                xuhao = 1
                for row in results_info:
                    bidresult_url = ""
                    constructno, bidsectionno, projname, bidcompany,bidagent,no1cand, no1price, info_originurl,cand_originurl =\
                        row[0], row[1], row[2], row[3], row[4], row[5], row[6]+"万元",row[7],row[8]
                    #sql_info = "select bidcompany,bidagent,originurl from tb_bidinfo where constructno='" + constructno + "' and bidsectionno='" + bidsectionno + "'"
                    sql_bidresult = "select originurl from tb_bidresult where constructno='" + constructno + \
                                    "' and bidsectionno='" + bidsectionno + "'"
                    #cursor.execute(sql_info)
                    #bidinfo_res = cursor.fetchall()
                    cursor.execute(sql_bidresult)
                    bidresult_res = cursor.fetchall()
                    # print(sql_result)
                    bidcand_url = "无"
                    bidresult_url = "无"
                    if not bidresult_res:
                        ret_cont = ret_cont + "<tr><td>" + str(xuhao) + "</td><td>" + constructno + "</td><td>" + projname + \
                                   "</td><td>" + bidcompany + "</td><td>" + bidagent + "</td><td>"+\
                                   no1cand+"</td><td>"+no1price+"</td><td><a href='" + info_originurl +\
                                   "'>招标信息</td><td><a href='" + cand_originurl + "'>中标候选</td><td>无</td></tr>"
                    else:
                        ret_cont = ret_cont + "<tr><td>" + str(xuhao) + "</td><td>" + constructno + "</td><td>" + projname + \
                                   "</td><td>" + bidcompany + "</td><td>" + bidagent + "</td><td>" + \
                                   no1cand + "</td><td>" + no1price + "</td><td><a href='" + info_originurl + \
                                   "'>招标信息</td><td><a href='" + cand_originurl + "'>中标候选</td><td><a href='"+bidresult_res[0][0]\
                                   +"'>中标结果</td></tr>"
                    xuhao += 1
                ret_cont = ret_cont + "</table>"
            cursor.close()
        except pymysql.Error as e:
            ret_cont = str(e.args[0]) + str(e.args[1])
        db.close()

    #only中标结果
    elif not involveBidInfo and not involveBidCands and involveBidResult:
        sql_conditions_str=result_condition_str
        sql_str='select constructno,bidsectionno,projname,winner,winprice,bidcompany,bidagent,originurl,windate from tb_bidresult where '\
                +sql_conditions_str
        ret_cont = 'nothing'
        # 打开数据库连接
        db = pymysql.connect(host="localhost", user="usr_bidinfo", password="20201203", database="db_bidinfo")
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        try:
            # 查询tb_bidinfo表中数据
            ret_cont = "<h2>招标中标信息</h2>"
            cursor.execute(sql_str)
            results_info = cursor.fetchall()
            #print(results_info)
            if not results_info:
                ret_cont = ret_cont + "无相关招标中标信息"
            else:
                recordNum = len(results_info)
                ret_cont = ret_cont + "<p>共有<font color='blue'><u>" + str(recordNum) + "</u></font>条记录</p>" \
                           + "<table boder='1'><tr><th>序号</th><th>报建编号</th><th>项目名称</th><th>中标人</th>" \
                             "<th>中标价格</th><th>招标采购人</th><th>招标代理</th><th>中标结果</th><th>中标日期</th>" \
                             "<th>招标信息</th><th>中标候选</th></tr>"
                xuhao = 1
                for row in results_info:
                    bidresult_url = ""
                    constructno, bidsectionno, projname, winner, winprice, bidcompany, bidagent, res_originurl, windate = \
                    row[0], row[1], row[2], row[3], row[4]+"万元", row[5], row[6], row[7], row[8]
                    # sql_info = "select bidcompany,bidagent,originurl from tb_bidinfo where constructno='" + constructno + "' and bidsectionno='" + bidsectionno + "'"
                    sql_bidinfo = "select originurl from tb_bidinfo where constructno='" + constructno + "' and bidsectionno='" + bidsectionno + "'"
                    sql_bidcand="select originurl from tb_bidcand where constructno='" + constructno + "' and bidsectionno='" + bidsectionno + "'"
                    cursor.execute(sql_bidinfo)
                    bidinfo_res = cursor.fetchall()
                    cursor.execute(sql_bidcand)
                    bidcand_res = cursor.fetchall()
                    if not bidinfo_res and not bidcand_res:
                        ret_cont = ret_cont + "<tr><td>" + str(xuhao) + "</td><td>" + constructno + "</td><td>" + projname + \
                                   "</td><td>" + winner + "</td><td>" + winprice + "</td><td>" + \
                                   bidcompany + "</td><td>" + bidagent + "</td><td><a href='" + res_originurl + \
                                   "'>中标结果</td><td>"+str(windate)+"</td><td>无</td><td>无</td></tr>"
                    elif bidinfo_res and not bidcand_res:
                        info_originurl=bidinfo_res[0][0]
                        ret_cont = ret_cont + "<tr><td>" + str(xuhao) + "</td><td>" + constructno + "</td><td>" + projname + \
                                   "</td><td>" + winner + "</td><td>" + winprice + "</td><td>" + \
                                   bidcompany + "</td><td>" + bidagent + "</td><td><a href='" + res_originurl + \
                                   "'>中标结果</td><td>" + str(windate) + "</td><td><a href='"+info_originurl+"'>招标信息</td><td>无</td></tr>"
                    elif not bidinfo_res and bidcand_res:
                        cand_originurl=bidcand_res[0][0]
                        ret_cont = ret_cont + "<tr><td>" + str(xuhao) + "</td><td>" + constructno + "</td><td>" + projname + \
                                   "</td><td>" + winner + "</td><td>" + winprice + "</td><td>" + \
                                   bidcompany + "</td><td>" + bidagent + "</td><td><a href='" + res_originurl + \
                                   "'>中标结果</td><td>" + str(windate) + "</td><td>无</td><td><a href='"+cand_originurl+"'>中标候选</td></tr>"
                    else:
                        info_originurl=bidinfo_res[0][0]
                        cand_originurl=bidcand_res[0][0]
                        ret_cont = ret_cont + "<tr><td>" + str(xuhao) + "</td><td>" + constructno + "</td><td>" + projname + \
                                   "</td><td>" + winner + "</td><td>" + winprice + "</td><td>" + \
                                   bidcompany + "</td><td>" + bidagent + "</td><td><a href='" + res_originurl + \
                                   "'>中标结果</td><td>" + str(windate) + "</td><td><a href='"+info_originurl+"'>招标信息</td><td><a href='" \
                                   + cand_originurl + "'>中标候选</td></tr>"
                    xuhao += 1
                ret_cont = ret_cont + "</table>"
            cursor.close()
        except pymysql.Error as e:
            ret_cont = str(e.args[0]) + str(e.args[1])
        db.close()

    #招标信息+中标结果
    elif involveBidInfo and not involveBidCands and involveBidResult:
        sql_condition_str=' and '.join(result_conditions_lst)
        sql_str='select a.constructno,a.bidsectionno,a.projname,b.winner,b.winprice,a.bidcompany,' \
                'a.bidagent,b.originurl,b.windate,a.originurl from tb_bidinfo a join tb_bidresult b ' \
                'on a.constructno=b.constructno and a.bidsectionno=b.bidsectionno where '+sql_condition_str
        ret_cont = 'nothing'
        # 打开数据库连接
        db = pymysql.connect(host="localhost", user="usr_bidinfo", password="20201203", database="db_bidinfo")
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        try:
            # 查询tb_bidinfo表中数据
            ret_cont = "<h2>招标中标信息</h2>"
            cursor.execute(sql_str)
            results_info = cursor.fetchall()
            # print(results_info)
            if not results_info:
                ret_cont = ret_cont + "无相关招标中标信息"
            else:
                recordNum = len(results_info)
                ret_cont = ret_cont + "<p>共有<font color='blue'><u>" + str(recordNum) + "</u></font>条记录</p>" \
                           + "<table boder='1'><tr><th>序号</th><th>报建编号</th><th>项目名称</th><th>中标人</th>" \
                             "<th>中标价格</th><th>招标采购人</th><th>招标代理</th><th>中标结果</th><th>中标日期</th>" \
                             "<th>招标信息</th><th>中标候选</th></tr>"
                xuhao = 1
                for row in results_info:
                    bidresult_url = ""
                    constructno, bidsectionno, projname, winner, winprice, bidcompany, bidagent, res_originurl, windate,info_originurl = \
                        row[0], row[1], row[2], row[3], row[4] + "万元", row[5], row[6], row[7], row[8],row[9]
                    sql_bidcand = "select originurl from tb_bidcand where constructno='" + constructno + "' and bidsectionno='" + bidsectionno + "'"
                    cursor.execute(sql_bidcand)
                    bidcand_res = cursor.fetchall()
                    if not bidcand_res:
                        ret_cont = ret_cont + "<tr><td>" + str(xuhao) + "</td><td>" + constructno + "</td><td>" + projname + \
                                   "</td><td>" + winner + "</td><td>" + winprice + "</td><td>" + \
                                   bidcompany + "</td><td>" + bidagent + "</td><td><a href='" + res_originurl + \
                                   "'>中标结果</td><td>" + str(windate) + "</td><td><a href='"+info_originurl+"'>招标信息</td><td>无</td></tr>"
                    else:
                        ret_cont = ret_cont + "<tr><td>" + str(xuhao) + "</td><td>" + constructno + "</td><td>" + projname + \
                                    "</td><td>" + winner + "</td><td>" + winprice + "</td><td>" + \
                                    bidcompany + "</td><td>" + bidagent + "</td><td><a href='" + res_originurl + \
                                    "'>中标结果</td><td>" + str(windate) + "</td><td><a href='" + info_originurl + \
                                   "'>招标信息</td><td><a href='"+bidcand_res[0][0]+"'>中标候选</td></tr>"
                xuhao += 1
            ret_cont = ret_cont + "</table>"
            cursor.close()
        except pymysql.Error as e:
            ret_cont = str(e.args[0]) + str(e.args[1])
        db.close()

    #中标候选+中标结果
    elif not involveBidInfo and involveBidCands and involveBidResult:
        sql_conditions_str=' and '.join(cand_conditions_lst_res)
        sql_str='select a.constructno,a.bidsectionno,a.projname,a.no1cand,a.no1price,a.infodate,a.originurl,' \
                'b.winner,b.winprice,b.windate,b.originurl from tb_bidcand a join tb_bidresult b ' \
                'on a.constructno=b.constructno and a.bidsectionno=b.bidsectionno where '+sql_conditions_str
        ret_cont = 'nothing'
        # 打开数据库连接
        db = pymysql.connect(host="localhost", user="usr_bidinfo", password="20201203", database="db_bidinfo")
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        try:
            # 查询tb_bidinfo表中数据
            ret_cont = "<h2>招标中标信息</h2>"
            cursor.execute(sql_str)
            results_info = cursor.fetchall()
            # print(results_info)
            if not results_info:
                ret_cont = ret_cont + "无相关招标中标信息"
            else:
                recordNum = len(results_info)
                ret_cont = ret_cont + "<p>共有<font color='blue'><u>" + str(recordNum) + "</u></font>条记录</p>" \
                           + "<table boder='1'><tr><th>序号</th><th>报建编号</th><th>项目名称</th><th>中标候选人</th>" \
                             "<th>候选价格</th><th>候选日期</th><th>中标候选</th><th>中标人</th><th>中标价格</th>" \
                             "<th>中标价格</th><th>中标日期</th><th>中标信息</th><th>招标信息</th></tr>"
                xuhao = 1
                for row in results_info:
                    bidresult_url = ""
                    constructno, bidsectionno, projname, no1cand,no1price,canddate,cand_originurl,winner, winprice, windate, res_originurl= \
                        row[0], row[1], row[2], row[3], row[4] + "万元", row[5], row[6], row[7], row[8]+"万元", row[9],row[10]
                    sql_bidinfo = "select originurl from tb_bidinfo where constructno='" + constructno + "' and bidsectionno='" + bidsectionno + "'"
                    cursor.execute(sql_bidinfo)
                    bidinfo_res = cursor.fetchall()
                    if not bidinfo_res:
                        ret_cont = ret_cont + "<tr><td>" + str(xuhao) + "</td><td>" + constructno + "</td><td>" + projname + \
                                   "</td><td>" + no1cand + "</td><td>" + no1price + "</td><td>" + \
                                   str(canddate) + "</td><td><a href='" + cand_originurl + "'>中标候选</td><td>"+winner+"</td><td>" + \
                                   winprice+ "</td><td>"+str(windate)+"</td><td><a href='"+res_originurl+"'>中标结果</td><td>无</td></tr>"
                    else:
                        ret_cont = ret_cont + "<tr><td>" + str(xuhao) + "</td><td>" + constructno + "</td><td>" + projname + \
                                   "</td><td>" + no1cand + "</td><td>" + no1price + "</td><td>" + \
                                   str(canddate) + "</td><td><a href='" + cand_originurl + "'>中标候选</td><td>" + winner + "</td><td>" + \
                                   winprice + "</td><td>" + str(windate) + "</td><td><a href='" + res_originurl + "'>中标结果</td><td><a href='"+\
                                   bidinfo_res[0][0]+"'>招标信息</td></tr>"
                xuhao += 1
            ret_cont = ret_cont + "</table>"
            cursor.close()
        except pymysql.Error as e:
            ret_cont = str(e.args[0]) + str(e.args[1])
        db.close()

    #招标信息+中标候选+中标结果
    elif involveBidInfo and involveBidCands and involveBidResult:
        info_sql_conditions_str=' and '.join(info_conditions_lst)
        sql_info_str='select constructno,bidsectionno,projname,bidcompany,bidagent,bidconsprice,originurl ' \
                     'from tb_bidinfo where '+info_sql_conditions_str
        ret_cont = 'nothing'
        # 打开数据库连接
        db = pymysql.connect(host="localhost", user="usr_bidinfo", password="20201203", database="db_bidinfo")
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        try:
            # 查询tb_bidinfo表中数据
            ret_cont_1 = "<h2>招标中标信息</h2>"
            ret_cont_2=''
            cursor.execute(sql_info_str)
            results_info = cursor.fetchall()
            hasmatchdata=False
            if results_info:
                recordNum = len(results_info)
                ret_cont_2 = "<p>共有<font color='blue'><u>" + str(recordNum) + "</u></font>条记录</p>" \
                           + "<table boder='1'><tr><th>序号</th><th>报建编号</th><th>项目名称</th><th>招标采购人</th>" \
                             "<th>招标代理</th><th>招标限价</th><th>招标网页</th><th>中标候选人</th><th>中标候选价</th>" \
                             "<th>中标候选</th><th>中标人</th><th>中标价格</th><th>中标结果</th></tr>"
                xuhao = 1
                for row in results_info:
                    constructno, bidsectionno, projname, bidcompany, bidagent, bidconsprice, info_originurl = \
                        row[0], row[1], row[2], row[3], row[4] + "万元", row[5], row[6]
                    sql_bidcand = "select no1cand,no1price,originurl from tb_bidcand where constructno='" + constructno \
                                  + "' and bidsectionno='" + bidsectionno + "' and "+cand_condition_str
                    cursor.execute(sql_bidcand)
                    bidcand_res = cursor.fetchall()
                    if bidcand_res:
                        cand_row=bidcand_res[0]
                        no1cand,no1price,cand_originurl=cand_row[0],cand_row[1]+"万元",cand_row[2]
                        sql_bidres="select winner,winprice,originurl from tb_bidresult where constructno='"+ constructno \
                                   + "' and bidsectionno='" + bidsectionno + "' and "+result_condition_str
                        cursor.execute(sql_bidres)
                        bidres_res=cursor.fetchall()
                        if bidres_res:
                            hasmatchdata=True
                            res_row=bidres_res[0]
                            winner,winprice,res_originurl=res_row[0],res_row[1]+"万元",res_row[2]
                            ret_cont_2 = ret_cont_2 + "<tr><td>" + str(xuhao) + "</td><td>" + constructno + "</td><td>" + projname + \
                                       "</td><td>" + bidcompany + "</td><td>" + bidagent + "</td><td>" + \
                                       bidconsprice + "</td><td><a href='" + info_originurl + "'>招标信息</td><td>" +no1cand+\
                                         "</td><td>"+no1price+"</td><td><a href='"+cand_originurl+"'>中标候选</td><td>"+winner+\
                                         "</td><td>"+winprice+"</td><td><a href='"+res_originurl+"'>中标结果</td></tr>"
                        else:
                            continue
                    else:
                        continue
            if not hasmatchdata:
                ret_cont_2='无相关招标中标信息'
            ret_cont=ret_cont_1+ret_cont_2

        except pymysql.Error as e:
            ret_cont = str(e.args[0]) + str(e.args[1])
        db.close()


    return HttpResponse(ret_cont)
