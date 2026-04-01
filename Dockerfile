FROM node:20-slim
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv && apt-get clean
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
RUN npm run build
RUN pip3 install fastapi uvicorn aiofiles --break-system-packages
EXPOSE 8000
CMD ["python3", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
