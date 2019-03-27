from jira import JIRA
import pandas as pd
from dateutil.parser import *
'''
라이블러리 설치 
pip install jira
pip install padas 
pip install openpyxl
pip install python-dateutil
'''

# jira 설정 정보
jira_server = 'https://igloosecjira.atlassian.net'
jira_id = 'sptm@igloosec.com'
jira_passwd = '****'


# jira 설정 정보 적용
jira = JIRA(server=jira_server, basic_auth=(jira_id, jira_passwd))

'''
# 필드 정보 # 
priority : priority
issuetype : issuetype
담당 엔지니어 :customfield_10028
완료 요청 일자 : customfield_10043
담당 개발자(TM) : customfield_10049
고객사 : customfield_10027[0].value
description : description
'''

value_list = []

# Summaries of my last 50 reported issues
for issue in jira.search_issues('project in (SPTM31, SPTM40, SPTM50) AND status not in (Closed, Done, Resolved) AND "담당 개발자(TM)" = 양학승 ORDER BY key DESC', maxResults=50):
    key = issue.key                                     #이슈 Key
    summary = issue.fields.summary                      #이슈 Summary
    assignee = issue.fields.assignee                    #이슈 할당자
    reporter = issue.fields.reporter                    #이슈 보고자
    status = issue.fields.status                        #이슈 상태
    created = ''
    if issue.fields.created is not None:
        created = parse(issue.fields.created).strftime("%Y.%m.%d %H:%M:%S")                     #이슈 생성일
    updated = ''
    if issue.fields.updated is not None:
        updated = parse(issue.fields.updated).strftime("%Y.%m.%d %H:%M:%S")                    #이슈 업데이트일
    duedate = ''
    if issue.fields.duedate is not None:
        duedate = parse(issue.fields.duedate).strftime("%Y.%m.%d %H:%M:%S")                       #이슈 완료일
    developer = issue.fields.customfield_10049          #이슈 담당 개발자(TM)
    customer =''
    if len(issue.fields.customfield_10027) > 0:
        customer = issue.fields.customfield_10027[0].value  #이슈 고객사
    engineer = issue.fields.customfield_10028           # 이슈 담당 엔지니어

    value_list.append([key, summary, assignee, reporter, status, created, updated, duedate, developer, customer, engineer])

cols = ['Key', 'Summary', 'Assignee', 'Reporter', 'Status', 'Created', 'Updated', 'Due', '담당 개발자(TM)', '고객사','담당 엔지니어']
df = pd.DataFrame(value_list, columns=cols)
df.tail()

#엑셀 파일 저장
df.to_excel('result.xlsx', sheet_name='Sheet1')
