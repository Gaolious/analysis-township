
def test_call_by_reference_check():
    def check(a:dict):
        a.update({
            'param' : 1
        })

    param = {
        'a' : 1
    }

    assert param.get('a', None) == 1
    assert param.get('param', None) == None

    check(param)

    assert param.get('a', None) == 1
    assert param.get('param', None) == 1
