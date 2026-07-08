import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 5,
  duration: '30s',
  thresholds: {
    http_req_failed: ['rate<0.05'],
    http_req_duration: ['p(95)<1500'],
  },
};

export default function () {
  const base = __ENV.BASE_URL || 'http://localhost/api';
  const res = http.get(`${base}/health`);
  check(res, { 'health ok': (r) => r.status === 200 });
  sleep(1);
}
