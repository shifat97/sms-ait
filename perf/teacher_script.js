import http from 'k6/http'
import { sleep, group, check } from 'k6'
import { htmlReport } from 'https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js';
import { textSummary } from 'https://jslib.k6.io/k6-summary/0.0.1/index.js';


const BASE_URL = 'http://54.255.195.111:5171';
const headers = { 'Content-Type': 'application/json' };

export const options = {
    duration: '10s',
    vus: 1,
    thresholds: {
        http_req_failed: ['rate<0.01'],
        http_req_duration: ['p(95)<1000']
    }
};


export default function () {
    let authToke = ''
    let createdTeacherId = null;

    group('Login', function () {
        const payload = JSON.stringify({
            username: 'admin',
            password: 'password123'
        })

        const response = http.post(`${BASE_URL}/login`, payload, {
            headers: headers
        })

        const responseData = response.json();
        authToke = responseData['authToken'];

        sleep(5)
    })

    group('Create teacher', function () {
        const randomNumber = Math.floor(Math.random() * 10000);
        const payload = JSON.stringify(
            {
                name: 'Test User' + randomNumber,
                email: 'testemail' + randomNumber + '@yahoo.com',
                department: 'CSE',
                teacherId: randomNumber,
                designation: 'Professor'
            }
        );

        const response = http.post(`${BASE_URL}/api/teacher`, payload, {
            headers: {
                ...headers,
                'Authorization': `Bearer ${authToke}`
            }

        })

        createdTeacherId = response.json().teacherId

        check(response, {
            'Status code is 200 or 201': (r) => r.status === 200 || r.status === 201,
            'Data matched with payload': (r) => {
                const responseData = r.json();
                const requestData = JSON.parse(payload);

                return responseData.name === requestData.name;
            }
        });

        sleep(5)
    });

    group('Get teachers', function () {
        const response = http.get(`${BASE_URL}/api/teacher`, {
            headers: {
                ...headers,
                'Authorization': `Bearer ${authToke}`
            }
        })

        check(response, { 'Status code is 200 or 201': (r) => r.status === 200 || r.status === 201, });

        sleep(5)
    });


    group('Get teacher with ID', function () {
        const response = http.get(`${BASE_URL}/api/teacher/${createdTeacherId}`, {
            headers: {
                ...headers,
                'Authorization': `Bearer ${authToke}`
            }

        })

        check(response, { 'Status code is 200 or 201': (r) => r.status === 200 || r.status === 201, });

        sleep(5)
    });


    group('Update teacher', function () {
        const payload = JSON.stringify(
            {
                name: 'Test User Update' + createdTeacherId,
                email: 'updatetestemail' + createdTeacherId + '@yahoo.com',
            }
        );

        const response = http.put(`${BASE_URL}/api/teacher/${createdTeacherId}`, payload, {
            headers: {
                ...headers,
                'Authorization': `Bearer ${authToke}`
            }

        })

        check(response, { 'Status code is 200 or 201': (r) => r.status === 200 || r.status === 201, });

        sleep(5)
    });

    group('Delete teacher with ID', function () {
        const response = http.del(`${BASE_URL}/api/teacher/${createdTeacherId}`, null, {
            headers: {
                ...headers,
                'Authorization': `Bearer ${authToke}`
            }

        })

        check(response, { 'Status code is 200 or 201': (r) => r.status === 200 || r.status === 201, });

        sleep(5)
    });
};


export function handleSummary(data) {
    return {
        'perf-results.html': htmlReport(data),
        stdout: textSummary(data, { indent: ' ', enableColors: true }),
    };
};
