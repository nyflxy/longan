#coding=utf-8

import datetime
import elasticsearch

es = elasticsearch.Elasticsearch()

if __name__ == "__main__":

    # 创建
    es.index("newbie","link",{"name":"lxy","age":27,"create_date":datetime.datetime.now()},)

    print es.search(index="my-index",doc_type="test-type")
    print es.count("newbie","link",{
        "query":{
            "bool":{
                "must":{"match":{"company.name":"qingdun"}},
                # "must_not":{"match":{"name":"niyoufa"}},
            }
        }
    })
    es.delete("newbie","link",1)
    es.delete_by_query("newbie",)
    result = es.search("newbie","user",{
        "query":{
            "term":{
                "age":25,
            }
        }
    })
    result = es.search("newbie", "user", {
        "query": {
            "terms": {
                "age": [20,25,30],
            }
        }
    })
    result = es.search("newbie", "user", {
        "query": {
            "range": {
                "age": {
                    "gte":25,
                    "lte":2
                },
            }
        }
    })
    result = es.search("newbie", "user", {
        "query": {
            "exists": {
                "field":"age"
            }
        }
    })
    result = es.search("newbie", "user", {
        "query": {
            "bool":{
                "must":{"term":{"age":25}},
                "must_not":{"term":{"name":"niyoufa"}},
                "should":[
                    {"term":{"name":"lxy1"}},
                ]
            }
        }
    })
    result = es.search("newbie", "user", {
        "query": {
            "match_all":{}
        }
    })
    result = es.search("newbie", "user", {
        "query": {
            "match": {"name":"niyoufa"}
        }
    })
    result = es.search("newbie", "user", {
        "query": {
            "multi_match": {
                "query":"full text search",
                "fields":["name","age"]
            }
        }
    })

    filter
    result = es.search("newbie","link",{
        "query":{
            "filtered": {
                "query": {"match": {"name": "niyoufa"}},
                "filter": {"term": {"age": 25}},
            },
        }
    })

    sort
    result = es.search("newbie", "link", {
        "query": {
            "exists":{
                "field":"age",
            }
        },
        "sort":{"age":{"order":"desc"}}
    })

    result = es.search("newbie", "link", {
        "query": {
            "match": {"name":"niyoufa"}
        }
    })

    print result.get("hits").get("hits")
    print len(result.get("hits").get("hits"))

# coding=utf-8
import  datetime, time, json, pdb
from  es_settings  import *
import cPickle as pickle
import logging
from xieli.models import * 
from xieli.util.types import * 
from django.conf import settings 

import pyes 
from pyes import *
from pyes.filters import GeoBoundingBoxFilter, GeoDistanceFilter, GeoPolygonFilter
from pyes.query import FilteredQuery, MatchAllQuery , Search
from pyes.sort import SortFactory, SortOrder, GeoSortOrder, ScriptSortOrder
from pyes.queryset import generate_model

ES_PATH = settings.ES_PATH
#ES_PATH = "http://dev.xielicheng.com:9200"
#ES_PATH ="http://192.168.1.113:9200"
#ES_PATH = "http://www.xieliapp.com:9200"

es_logger = logging.getLogger("utils")

# 连接es服务器
CONN_ES = pyes.ES(ES_PATH, timeout=200.0) 

#连接es服务器
def _connect_index():
    conn = pyes.ES(ES_PATH, timeout=200.0)
    return conn

#创建index索引表
def create_index(name,index_type,FIELD_MAPPING):
    try : 
        conn = _connect_index()
        conn.indices.create_index(name)
        conn.indices.put_mapping(index_type, {'properties':FIELD_MAPPING}, [name])
        print "创建%s索引和%s表"%(name,index_type)
    except Exception,e : 
        print "创建%s索引和%s表失败"%(name,index_type)
        es_logger.error(str(e))

#删除index索引表
def delete_index(name):
    try : 
        conn = pyes.ES(ES_PATH, timeout=200.0)
        conn.indices.delete_index(name)
        print "索引%s被删除"%name
    except Exception,e: 
        print "删除索引%s失败"%name
        es_logger.error(str(e))

#向es插入数据
def insert_into_es(params,index_name,index_type):
    try : 
        CONN_ES.index(params,index_name,index_type)
        try:
            CONN_ES.indices.refresh(index_name)
        except Exception, e:
            pass
        # print "插入数据:\n" 
        # print params
    except Exception ,e : 
        # print "%s插入数据失败"%e
        es_logger.error(str(e))

#获取es数据，形成类似django model对象
def get_index_model(index_name,index_type) :
    from pyes.queryset import generate_model
    return generate_model(index_name, index_type,es_url=ES_PATH)

#获取所有相关的记录
def march_query_alltag(field,query) :
    #b = MatchQuery('interest_tag','美国')
    b = MatchQuery(field,query)
    return [i for i in CONN_ES.search(query =b)]

#must + should
def march_query_tag(field,query,sub_type):
    must = pyes.TermQuery("sub_type",sub_type)
    should = pyes.MatchQuery(field,query)
    query = pyes.BoolQuery(must = must ,should = should)
    return [i for i in CONN_ES.search(query =query)]

#搜索指定index，指定字段
def  search_term(field,query,index_name,index_type):
    q = TermQuery(field, query)
    results = CONN_ES.search(query = q,indices=index_name,doc_types=index_type)
    return [i for i in results]

#搜索多个字段
def search_more_term(field1,query1,field2,query2,index_name,index_type,kw=None,*arg):
    must1 = pyes.TermQuery(field1,query1)
    must2 = pyes.TermQuery(field2,query2)
    must= [must1,must2]
    if arg:
        must3 = pyes.TermQuery(arg[0],arg[1])
        must.append(must3)
    query = pyes.BoolQuery(must = must)

    if kw:
        search = search_add_sort(query,kw["sort_field"],kw["sort_type"])
        
        return [i for i in CONN_ES.search(search,indices=[index_name])]

    return [i for i in CONN_ES.search(query =query,indices=index_name,doc_types=index_type) ]

#倒序 desc 
def search_add_sort(query,sort_field,sort_type):
    search = Search(query)
    sort_order = SortOrder(sort_field, sort_type)
    search.sort.add(sort_order)
    return search

#按时间范围查询
def search_range_time(field,start_date,date_range,index_name,index_type):
    if type(date_range) == type(-1) and date_range != -1:
        #start_da = datetime.datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%SZ").date()
        start_da = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = (start_da + datetime.timedelta(days=date_range)).strftime('%Y-%m-%d')
        must = pyes.RangeQuery(pyes.ESRange(field, from_value=start_date, to_value=end_date))
        query = pyes.BoolQuery(must = must)
        dd = [i for i in CONN_ES.search(query =query,indices=index_name,doc_types=index_type) ]
        return dd
    else:
        raise

def get_data_id(data):
    return data.get_id()

#此处id为es默认id
def delete_data(index_name,index_type,id):
    CONN_ES.delete(index = index_name,doc_type = index_type,id = id)

#根据es对象删除数据
def delete_data_from_esobj(es_obj):
    id = get_data_id(es_obj)
    es_meta = es_obj.get_meta()
    index_name = es_meta['index']
    index_type = es_meta["type"]
    CONN_ES.delete(index = index_name,doc_type = index_type,id = id)

def create_all_about_xieli_es_index():
    try:
        #create_index("messageglobalindex","MessageGlobal",GLOBAL_MESSAGE_FIELD_MAPPING)
        #create_index("commentglobalindex","CommentGlobal",GLOBAL_COMMENT_FIELD_MAPPING)
        #create_index("fileglobalindex","FileGlobal",GLOBAL_FILEIMAGE_FIELD_MAPPING)
        #create_index("usernavigationglobalindex","UsernavigationgGlobal",GLOBAL_USERNAVIGATION_FIELD_MAPPING)
        #create_index("participationglobalindex","ParticipationGlobal",GLOBAL_PARTICIPATION_FIELD_MAPPING)
        delete_index("teamup")
        create_index("teamup","CommonObject",ES_FIELD_MAPPING)
    except Exception, e:
        es_logger.error(str(e))

def delete_all_index():
    delete_index("messageglobalindex")
    delete_index("commentglobalindex")
    delete_index("fileglobalindex")
    delete_index("usernavigationglobalindex")
    delete_index("participationglobalindex")
    delete_index("teamup")

# author nyf 

#根据条件获取从ES获取指定个数数据
#index_name : 索引名称
#index_type : 索引表名称
#query_params : 查询条件
#ordering : 排序字段
# start , end 数据标记
def get_document_from_es(index_name,index_type,query_params={},ordering="",start=0,end=1) : 
    try : 
        model = get_index_model(index_name,index_type)
    except Exception ,e : 
        print e 
        return False 
    if ordering : 
        return model.objects.filter(**query_params).order_by(ordering)[start:end]
    else : 
        return model.objects.filter(**query_params)[start:end]

#根据条件从ES中删除文档
#index_name : 索引名称
#index_type : 索引表名称
#query_params : 查询条件
def delete_document_from_es(index_name,index_type,query_params={}) : 
    try : 
        model = get_index_model(index_name,index_type)
    except Exception ,e : 
        print e 
        return False 
    results = model.objects.filter(**query_params).all()
    try : 
        for result in results : 
            result.delete()
    except Exception ,e : 
        print e 
        return False 
    return True 

#coding=utf8
#author = yxp
"""
    配置elasticsearchp2.2
    jdk1.8
    本配置文件以 路径，loging为主
"""

from django.conf import settings 
ES_PATH = settings.ES_PATH


#ES 定义index字段  
"""
    analyzed 使用分词器
    analyzer  分词器类型
"""
ES_FIELD_MAPPING = {
    "id" :
        {"index":"no","type":u'integer'},
    "sha1" :
        {"index":"analyzed","type":u'string','store': 'yes'},
    #标题
    "title":
        {"index":"analyzed","type":u'string','store': 'yes',},
    #作者
    "author" :
        {"index":"analyzed","type":u'string','store': 'yes',},
    #创建时间
    "creation_time" :
        {"index":"analyzed","type":u'date'},
    #是否允许主动传播
    "broadcast":
        {"index":"no","type":u'boolean'},
    #参与人数
    "nb_participants" :
        {"index":"analyzed","type":u'integer'},
    #插件类型: 调查问卷，监督举报等
    "plugin" :
        {"index":"analyzed","type":u'string'},
    #功能类别标签：排行榜，求安慰等
    "func_tags":
        {"index":"analyzed","type":u'string',},
    #行业大标签 list 
    "topic_tags" :
        {"index":"analyzed","type":'string','store': 'yes'},
    #兴趣小标签 list
    "interest_tag":
        {"index":"analyzed","type":'string','store': 'yes'},
    #描述
    "description" :
        {"index":"no","type":u'string'},
    #版本
    "_version_":
        {"index":"analyzed","type":u'long'},
    #地理位置,经纬度 [经度,纬度]
    "geo":
        {"index":"analyzed","type":u'geo_point','store': 'yes',},
    #发布活动时的参与者限制条件列表
    "limits" :
        {"index":"analyzed","type":u'string'},
    #参与类型 0 :所有用户 1:联系人
    "participant_type" :
        {"index":"no","type":u'integer'},
    #图片列表
    "image_sha1s":
        {"index":"no","type":u'string'},
    #分享设置 1:可以分享 0:不可以分享
    "can_be_shared" :
        {"index":"no","type":u'integer'},
    #分享次数
    "nb_shares" :
        {"index":"analyzed","type":u'integer'},
    #多少人已经完成任务或已签到
    "nb_completes":
        {"index":"analyzed","type":u'integer'},
    #根据坐标反解析出的地理位置信息，比如海淀区学清路38号
    "loc" :
        {"index":"analyzed","type":u'string'},
    #城市
    "city" :
        {"index":"analyzed","type":u'string'},
    #百度地图对应的城市编码
    "city_code":
        {"index":"analyzed","type":u'integer'},
    #发起人类型：0表示以个人名义发起，1表示以公司名义发起
    "organizer_type" :
        {"index":"analyzed","type":u'integer'},
     #是否有红包, 缺省免费没有
    "has_bonus" :
        {"index":"no","type":u'boolean'},
    #此项投票或是任务的红包总金额
    "total_amount":
        {"index":"analyzed","type":u'float'},
    #红包派发给多少人
    "nb_rewarded_people":
        {"index":"analyzed","type":u'integer'},
    #红包派发类型: 0:最先参与的若干个人；1:根据结果审批的若干个人；
    "bonus_type" :
        {"index":"analyzed","type":u'integer'},
    #红包是否已经派发0 :未派发 1:已派发
    "is_bonus_paid":
        {"index":"analyzed","type":u'integer',},
    #红包发放是否已经结算：0 :未结算 1:已结算
    "is_account" :
        {"index":"analyzed","type":u'integer',},
    "creator_sha1" :
        {"index":"analyzed","type":u'string',},
    "sub_type" :
        {"index":"analyzed","type":u'integer',},
    "status" :
        {"index":"analyzed","type":u'integer',},
}

#分布式comment全局id存储
GLOBAL_COMMENT_FIELD_MAPPING = {
    "user_sha1" :
        {"index":"not_analyzed","type":u'string','store': 'yes'},
    "obj_sha1" :
        {"index":"not_analyzed","type":u'string','store': 'yes'},
    "global_object_id":
        {"index":"not_analyzed","type":u'string','store': 'yes',},
    "sha1":
        {"index":"not_analyzed","type":u'string','store': 'yes',},
}

#分布式paticipation全局id存储
GLOBAL_PARTICIPATION_FIELD_MAPPING = {
    "user_sha1" :
        {"index":"analyzed","type":u'string','store': 'yes'},
    "obj_sha1" :
        {"index":"analyzed","type":u'string','store': 'yes'},
    "global_object_id":
        {"index":"analyzed","type":u'string','store': 'yes',},
}

#分布式usenav全局id存储
GLOBAL_USERNAVIGATION_FIELD_MAPPING = {
    "user_sha1" :
        {"index":"analyzed","type":u'string','store': 'yes'},
    "global_object_id":
        {"index":"analyzed","type":u'string','store': 'yes',},
    "time":
        {"index":"not_analyzed","type":u'date','store': 'yes',"format": "yyyy-MM-dd"},

}
#分布式fileimage全局id存储
GLOBAL_FILEIMAGE_FIELD_MAPPING = {
    "sha1" :
        {"index":"analyzed","type":u'string','store': 'yes'},
    "global_object_id":
        {"index":"analyzed","type":u'string','store': 'yes',},
}

#分布式message全局id存储
GLOBAL_MESSAGE_FIELD_MAPPING = {
    "sha1" :
        {"index":"not_analyzed","type":u'string','store': 'yes'},
    "user_sha1" :
        {"index":"not_analyzed","type":u'string','store': 'yes'},
    "global_object_id":
        {"index":"not_analyzed","type":u'string','store': 'yes',},
    "obj_sha1":
        {"index":"not_analyzed","type":u'string','store': 'yes',},
    "comment_sha1":
        {"index":"not_analyzed","type":u'string','store': 'yes',},
    "type" :
        {"index":"not_analyzed","type":u'integer'},
    "creation_time" :
        {"index":"not_analyzed","type":u'date'},
    "already_read":
        {"index":"not_analyzed","type":u'integer'},
}






