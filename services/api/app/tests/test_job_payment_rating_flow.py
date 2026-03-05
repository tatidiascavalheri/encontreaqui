from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_job_payment_and_rating_flow():
    job = client.post('/jobs', json={
        'client_id': 1,
        'professional_id': 2,
        'category_id': 1,
        'description': 'Trocar chuveiro',
        'scheduled_at': '2026-01-01T10:00:00Z'
    }).json()
    assert job['status'] == 'requested'

    paid = client.post('/payments/intent', json={'amount_cents': 20000}).json()
    assert paid['status'] == 'requires_capture'

    client.patch(f"/jobs/{job['id']}/status", json={'status': 'completed'})
    rating = client.post('/ratings', json={
        'job_id': job['id'], 'rater_id': 1, 'target_id': 2, 'score': 5, 'job_status': 'completed'
    })
    assert rating.status_code == 200
