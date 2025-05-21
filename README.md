# Vulnerable Blog

A deliberately vulnerable blog application built with FastAPI for practicing security testing and penetration testing. This application contains intentional security vulnerabilities for educational purposes.

## Features

- User authentication
- Create, read blog posts
- Comment system
- User profiles
- Modern responsive UI with Bootstrap 5
- Mobile-friendly design

## Security Vulnerabilities

This application contains intentional security vulnerabilities for educational purposes, including:
- XSS (Cross-Site Scripting) vulnerabilities
- CSRF (Cross-Site Request Forgery) vulnerabilities
- Insecure direct object references
- Insufficient input validation
- Cookie-based authentication without proper security measures

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/vulnerable-blog.git
cd vulnerable-blog
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the server:
```bash
python blog.py
```

2. Access the application at `http://localhost:9000`

## Test Credentials

Use these credentials to test the application:

```
Username: admin
Password: admin123
```

## Security Testing

This application is designed for practicing security testing. Here are some areas you can explore:

1. XSS Testing:
   - Try injecting JavaScript in post content
   - Test comment sections for XSS vulnerabilities

2. CSRF Testing:
   - Test form submissions
   - Check if tokens are properly implemented

3. Authentication Testing:
   - Test cookie security
   - Try session hijacking
   - Test password reset functionality

4. Input Validation:
   - Test SQL injection
   - Test file upload vulnerabilities
   - Test input sanitization

## Contributing

Feel free to submit issues and enhancement requests!

## Disclaimer

This application is intentionally vulnerable and should only be used in controlled environments for educational purposes. Do not deploy this application in production or expose it to the public internet.
