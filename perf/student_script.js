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
        http_req_duration: ['p(95)<500']
    }
};


export default function () {
    let authToke = ''
    let createdStudentID = null;

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

    group('Create student', function () {
        const randomNumber = Math.floor(Math.random() * 10000);
        const payload = JSON.stringify(
            {
                name: 'Test User' + randomNumber,
                email: 'testemail' + randomNumber + '@yahoo.com',
                department: 'CSE',
                registrationId: randomNumber,
                age: Math.floor(Math.random() * (70 - 18 + 1)) + 18
            }
        );

        const response = http.post(`${BASE_URL}/api/student`, payload, {
            headers: {
                ...headers,
                'Authorization': `Bearer ${authToke}`
            }

        })

        createdStudentID = response.json().registrationId
        console.log('Random number: ', randomNumber)
        console.log('Registration id after creation: ', createdStudentID)

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

    group('Get students', function () {
        const response = http.get(`${BASE_URL}/api/student`, {
            headers: {
                ...headers,
                'Authorization': `Bearer ${authToke}`
            }
        })

        check(response, { 'Status code is 200 or 201': (r) => r.status === 200 || r.status === 201, });

        sleep(5)
    });


    group('Get student with ID', function () {
        console.log(createdStudentID)
        const response = http.get(`${BASE_URL}/api/student/${createdStudentID}`, {
            headers: {
                ...headers,
                'Authorization': `Bearer ${authToke}`
            }

        })

        check(response, { 'Status code is 200 or 201': (r) => r.status === 200 || r.status === 201, });

        sleep(5)
    });


    group('Update student', function () {
        const payload = JSON.stringify(
            {
                name: 'Test User Update' + createdStudentID,
                email: 'updatetestemail' + createdStudentID + '@yahoo.com',
            }
        );

        const response = http.put(`${BASE_URL}/api/student/${createdStudentID}`, payload, {
            headers: {
                ...headers,
                'Authorization': `Bearer ${authToke}`
            }

        })

        check(response, { 'Status code is 200 or 201': (r) => r.status === 200 || r.status === 201, });

        sleep(5)
    });

    group('Delete student with ID', function () {
        console.log(createdStudentID)
        const response = http.del(`${BASE_URL}/api/student/${createdStudentID}`, null, {
            headers: {
                ...headers,
                'Authorization': `Bearer ${authToke}`
            }

        })
        console.log(response)
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
