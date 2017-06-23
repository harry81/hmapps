# # 동 구하기
# curl 'http://rt.molit.go.kr/srh/getGugunListAjax.do'  -H 'Origin: http://rt.molit.go.kr'   --data 'sidoCode=47'
# 구미 - 47190
def get_gugunlist(sido):
    sidocode = sido['CODE']
    response = requests.get("http://rt.molit.go.kr/srh/getGugunListAjax.do",
                            params={"sidoCode": sidocode})
    return response.json()['jsonList']


# # 구군구하기
# curl 'http://rt.molit.go.kr/srh/getDongListAjax.do'  -H 'Origin: http://rt.molit.go.kr'   --data 'gugunCode=47830'
def get_donglist(dong):
    guguncode = dong['CODE']
    response = requests.get("http://rt.molit.go.kr/srh/getDongListAjax.do",
                            params={"gugunCode": guguncode})
    return response.json()['jsonList']


# # 단지 구하기
# curl 'http://rt.molit.go.kr/srh/getDanjiComboAjax.do' --data 'menuGubun=A&houseType=1&srhYear=2017&srhPeriod=2&gubunCode=LAND&dongCode=1121510900'
def get_danjicombo(**addr):
    params = {
        "dongCode": None,
        "menuGubun": "A",
        "houseType": 1,
        "srhYear": 2017,
        "srhPeriod": 2,
        "gubunCode": "LAND"
    }
    params.update(addr)

    response = requests.get("http://rt.molit.go.kr/srh/getDanjiComboAjax.do",
                            params=params)
    return response.json()['jsonList']
