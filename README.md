# পোর্টফোলিও

## চালানোর নিয়ম
pip install -r requirements.txt
ADMIN_TOKEN=আপনার-গোপন-কোড uvicorn main:app --reload

- সাইট: http://localhost:8000
- অ্যাডমিন: http://localhost:8000/admin (প্রজেক্ট যোগ / এডিট / মুছুন)
- API: GET/POST /api/projects, PUT/DELETE /api/projects/{id} (লেখার জন্য X-Token হেডার লাগে)
- ডেটা থাকে data.json ফাইলে।

## করণীয়
- static/index.html-এ YOUR_GITHUB ও YOUR_LINKEDIN বদলান।
- প্রজেক্টের GitHub/লাইভ লিংক অ্যাডমিন থেকে যোগ করুন।
