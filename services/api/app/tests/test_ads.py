from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_ad_serving_and_tracking():
    served = client.get('/ads/serve', params={
        'placement': 'HOME', 'lat': -23.56, 'lng': -46.65, 'role': 'client'
    })
    assert served.status_code == 200
    ad = served.json()['ad']
    assert ad is not None

    imp = client.post('/ads/track/impression', json={'campaign_id': ad['id']})
    clk = client.post('/ads/track/click', json={'campaign_id': ad['id']})
    assert imp.json()['tracked'] == 'impression'
    assert clk.json()['tracked'] == 'click'
