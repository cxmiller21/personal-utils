from taco import util

def test_get_app_config_data():
    app_data = util.get_json_config("my-apps")
    assert type(app_data) == dict
    
    assert app_data["installed"]["path"] == "/Applications"
    assert app_data["system"]["path"] == "/System/Applications"
    
    assert type(app_data["installed"]["apps"]) == list
    assert type(app_data["system"]["apps"]) == list
