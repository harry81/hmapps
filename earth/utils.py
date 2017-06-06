# -*- coding: utf-8 -*-
import locale


def flatten_dict(item):
    addrdetail = item.pop('addrdetail', None)

    if addrdetail:
        for k, v in addrdetail.items():
            item[k] = v

    return item


def rename_fields(item):
    ret = {}

    ret['sum_amount'] = locale.atoi(item[u'거래금액'].replace(',', ''))
    ret['bldg_yy'] = item[u'건축년도']
    ret['bldg_nm'] = item[u'아파트']
    ret['dong'] = item[u'법정동']
    ret['deal_yy'] = item[u'년']
    ret['deal_mm'] = item[u'월']
    ret['deal_dd'] = item[u'일']
    ret['bldg_area'] = item[u'전용면적']
    ret['bobn'] = item[u'지번']
    ret['area_cd'] = item[u'지역코드']
    ret['aptfno'] = item[u'층']

    return ret
