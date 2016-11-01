#coding=utf-8

import datetime
import elasticsearch

es = elasticsearch.Elasticsearch()

if __name__ == "__main__":


    # es.index("newbie","link",{"name":"lxy","age":27,"create_date":datetime.datetime.now()})
    # es.indices.refresh(index="newbie")
    # es.bulk({"name":"liuxiaoyan"})
    # es.create(index="newbie",doc_type='link',id=1,body={"name":"liuxiaoyan"})
    # result = es.search(index="newbie", doc_type="link",
    #                 body={"query":{
    #                     "match":{"company.name":"qingdun"}
    #                 }}
    #                 ).get("hits").get("hits")
    # print len(result)
    # print es.search(index="my-index",doc_type="test-type")
    # print es.count("newbie","link",{
    #     "query":{
    #         "bool":{
    #             "must":{"match":{"company.name":"qingdun"}},
    #             # "must_not":{"match":{"name":"niyoufa"}},
    #         }
    #     }
    # })
    # es.delete("newbie","link",1)
    # es.delete_by_query("newbie",)
    # result = es.search("newbie","user",{
    #     "query":{
    #         "term":{
    #             "age":25,
    #         }
    #     }
    # })
    # result = es.search("newbie", "user", {
    #     "query": {
    #         "terms": {
    #             "age": [20,25,30],
    #         }
    #     }
    # })
    # result = es.search("newbie", "user", {
    #     "query": {
    #         "range": {
    #             "age": {
    #                 "gte":25,
    #                 "lte":2
    #             },
    #         }
    #     }
    # })
    # result = es.search("newbie", "user", {
    #     "query": {
    #         "exists": {
    #             "field":"age"
    #         }
    #     }
    # })
    # result = es.search("newbie", "user", {
    #     "query": {
    #         "bool":{
    #             "must":{"term":{"age":25}},
    #             "must_not":{"term":{"name":"niyoufa"}},
    #             "should":[
    #                 {"term":{"name":"lxy1"}},
    #             ]
    #         }
    #     }
    # })
    # result = es.search("newbie", "user", {
    #     "query": {
    #         "match_all":{}
    #     }
    # })
    # result = es.search("newbie", "user", {
    #     "query": {
    #         "match": {"name":"niyoufa"}
    #     }
    # })
    # result = es.search("newbie", "user", {
    #     "query": {
    #         "multi_match": {
    #             "query":"full text search",
    #             "fields":["name","age"]
    #         }
    #     }
    # })

    # filter
    # result = es.search("newbie","link",{
    #     "query":{
    #         "filtered": {
    #             "query": {"match": {"name": "niyoufa"}},
    #             "filter": {"term": {"age": 25}},
    #         },
    #     }
    # })

    # sort
    # result = es.search("newbie", "link", {
    #     "query": {
    #         "exists":{
    #             "field":"age",
    #         }
    #     },
    #     "sort":{"age":{"order":"desc"}}
    # })

    result = es.search("newbie", "link", {
        "query": {
            "match": {"name":"niyoufa"}
        }
    })

    print result.get("hits").get("hits")
    print len(result.get("hits").get("hits"))