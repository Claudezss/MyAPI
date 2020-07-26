import json


def test_home(client):
    rsp = client.get("/")
    assert rsp.status_code == 200
    assert "Claude Zhang's APIs" == json.loads(rsp.data.decode())


def test_doc(client):
    rsp = client.get("/swagger.json")
    assert rsp.status_code == 200
    json_rsp = json.loads(rsp.data.decode())
    assert "swagger" in json_rsp
    assert "basePath" in json_rsp
    assert "paths" in json_rsp
