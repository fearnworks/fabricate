cd /code
# npm run dev --port 28101 --host 0.0.0.0
npm run build
http-server dist -p 28101 -a 0.0.0.0 --cors 