FROM python:3.13-alpine

# Set workdir early
WORKDIR /app

# Copy only requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip setuptools wheel python-dotenv \
 && pip install -r requirements.txt

# Now copy the full app
COPY . .

# Set port and expose
ENV PORT=9090
EXPOSE 9090

# Default command to run your Flask app
CMD ["python", "run.py"]
