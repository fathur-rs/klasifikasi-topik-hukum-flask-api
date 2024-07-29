# Klasifikasi Topik Hukum Indonesia Menggunakan IndoBERT

## Overview 
Repositori ini berisi API model klasifikasi topik hukum yang dikembangkan menggunakan IndoBERT. Proyek ini bertujuan untuk mengklasifikasikan pertanyaan-pertanyaan hukum ke dalam salah satu dari 13 topik yang telah ditentukan, seperti Pidana, Keluarga, dan Hukum, yang mencakup berbagai aspek regulasi dan kebijakan di Indonesia.

## Use-Case

>  ### Mempercepat Pengalihan Pengaduan ke Ahli yang Tepat

**Konteks Aplikasi:**
Di banyak instansi pemerintah atau kepolisian, pengaduan dari masyarakat sering mengalami keterlambatan dalam penanganan karena proses identifikasi dan pengalihan ke ahli yang tepat membutuhkan waktu. Hal ini terutama terjadi ketika pengaduan melibatkan isu hukum yang spesifik dan memerlukan pengetahuan ahli untuk direspon dengan tepat

**Proses Operasional:**
1. **Penerimaan Pengaduan:**
   Masyarakat mengirimkan pengaduan mereka melalui berbagai kanal seperti aplikasi web, email, atau bahkan secara fisik di kantor pemerintahan atau kepolisian

2. **Klasifikasi Otomatis Pengaduan:**
   Setiap pengaduan yang diterima akan segera diproses melalui sistem klasifikasi. Sistem ini akan menganalisis teks pengaduan dan mengklasifikasikannya ke dalam topik hukum yang relevan seperti Pidana, Keluarga, Perdata, dll

3. **Pengalihan Otomatis ke Ahli yang Relevan:**
   Berdasarkan klasifikasi yang dihasilkan, sistem akan otomatis mengalihkan pengaduan ke departemen atau ahli yang paling sesuai. Misalnya, pengaduan tentang kekerasan dalam rumah tangga akan langsung diteruskan ke unit perlindungan keluarga

4. **Tindak Lanjut oleh Ahli:**
   Ahli atau departemen yang relevan akan menerima pengaduan dan segera mengambil tindakan yang diperlukan. Proses ini memastikan bahwa pengaduan ditangani oleh orang yang paling mampu memberikan solusi efektif dan cepat

**Manfaat:**
- **Peningkatan Kecepatan Respons:** Mengurangi waktu tunggu untuk penanganan pengaduan, meningkatkan kecepatan respons terhadap masalah hukum
- **Penanganan yang Tepat:** Memastikan setiap pengaduan ditangani oleh ahli yang memiliki keahlian dan wewenang yang sesuai, sehingga meningkatkan kualitas penyelesaian kasus
- **Efisiensi Proses:** Mengotomatisasi bagian dari proses pengalihan pengaduan mengurangi beban kerja manual, memungkinkan staf untuk fokus pada tugas yang lebih kritis
- **Kepuasan Masyarakat:** Meningkatkan kepuasan masyarakat melalui penanganan kasus yang lebih cepat dan akurat

**Implementasi:**
Sistem ini cocok untuk diintegrasikan dalam operasional pemerintah daerah, kepolisian, dan instansi pemerintah lainnya yang sering menerima pengaduan publik. Dengan pemanfaatan teknologi seperti IndoBERT dalam klasifikasi teks, instansi pemerintah dapat mempercepat dan meningkatkan cara mereka merespon pengaduan dari masyarakat

## Dataset
Dataset berikut ini berisi 8500+ data QnA tentang pengaduan atau pertanyaan hukum di Indonesia yang telah di-scrap dari [HukumOnline](https://www.hukumonline.com/):

* [QnA Hukum Indonesia](/dataset/QnA_hukum_indonesia.csv)
* [Data Topik Pertanyaan](/dataset/pertanyaanTopik.csv)

## Model Card
Fine tuning menggunakan model Transformer [indolem/indobert-base-uncased](https://huggingface.co/indolem/indobert-base-uncased) 

| Epoch | Training Loss | Validation Loss | F1     |
|-------|---------------|-----------------|--------|
| 1     | 0.92132       | 1.232132        | 81.32  |
| 2     | 0.842132      | 1.032132        | 81.53  |
| 3     | 0.812321      | 0.9321324       | 82.139 |
| 4     | 0.788542      | 0.832132        | 83.832 |
| 5     | 0.75321321    | 0.7732143       | 84.3132|
| 6     | 0.2321321     | 0.432143        | 84.543 |
| 7     | 0.13321       | 0.42324         | 85.8934|
| 8     | 0.0321343     | 0.412321        | 86.3213|

## API Endpoint

### Register
- **Method**: POST
- **URL**: `http://localhost:8000/api/auth/register`
- **Description**:
  Register a new user with username and password.
- **Request Body**:
  
  ```json
  {
    "username": "username",
    "password": "password"
  }
- **Response**:
  
  ```json
  {
    "message": "User created successfully",
    "status_code": 201
  }
### Login
- **Method**: POST
- **URL**: `http://localhost:8000/api/auth/login`
- **Description**:
  Authenticate a user and generate JWT token to accessing the model API
- **Requst Body**:
  
  ```json
  {
    "username": "username",
    "password": "password"
  }
- **Response**:
  
  ```json
  {
    "message": {
        "token": "eyJhbGciOi..."
    },
    "status_code": 200
  }

### Predict
- **Method**: POST
- **URL**: `http://localhost:8000/api/model/predict`
- **Description**:
  Model predictions endpoint.
- **Request Body**:
  
  ```json
  {
    "question": "Saya dan suami sudah memiliki 3 anak. Suami saya tidak pernah main kasar atau selingkuh, tapi masalahnya ia tidak pernah memberikan nafkah lahir untuk saya dan anak-anak. Apakah saya bisa gugat cerai suami saya karena alasan itu? Kemudian, jika saya yang menggugat, apakah saya tetap dapat harta gono-gini?"
  }
- **Response**:
  
  ```json
  {
    "message": {
        "prediction": {
            "confidence": 0.957719624042511,
            "label": "Keluarga"
        }
    },
    "status_code": 200
  }

### Healthcheck
- **Method**: GET
- **URL**: `http://localhost:8000/api/model/healthcheck`
- **Description**:
  Check the health status of the model.
- **Request Body**:
  
  ```json
  None
- **Response**:
  
  ```json
  {
    "message": {
        "model_loaded": true,
        "sample": "Seorang korban penganiayaan telah mengadukan tindak pidana yang menimpa dirinnya...",
        "status": "Healthy",
        "test_prediction": {
            "confidence": 0.9810755252838135,
            "label": "Pidana"
        },
        "model_version": "1.0.0"
    },
    "status_code": 200
  }

### Architecture
- **Method**: GET
- **URL**: `http://localhost:8000/api/model/architecture`
- **Description**:
Return the model architecture.
- **Request Body**:
  
  ```json
  None
- **Response**:
  
  ```json
  {
     "message": {
          "architecture": str
     }
     "status_code": 200
  }
### Postman API Doc: [Postman Collection](https://api.postman.com/collections/23055226-dd03bf33-a140-4dd7-aeab-4be37d35a0b1?access_key=PMAT-01J3Z86V6P5J58SH9A78HP19HW)


## Installation Guide

### 1. Clone the Repository

Start by cloning the repository to your local machine. Open your terminal and run the following commands:

```bash
# Clone the repository
git clone https://github.com/fathur-rs/klasifikasi-topik-hukum-flask-api.git

# Change directory to the cloned repository
cd klasifikasi-topik-hukum-flask-api
```

### 2. Docker Installation

If you prefer using Docker, ensure that you have Docker and Docker Compose installed on your machine. Run the following command to build and start the service using Docker:

```bash
# Build and run the Flask app in a Docker container
docker-compose up --build flask_app
```

This command builds the Docker image and starts the Flask application in a container. It maps the appropriate ports to `8000` so you can access it with `http://localhost:8000`

### 3. Local Installation

For local installation, you need to have Python and Conda installed. Follow these steps to set up and run the application locally:

#### Step 1: Create and Activate a Conda Environment

```bash
# Create a new Conda environment
conda create -n ktk python=3.10

# Activate the Conda environment
conda activate ktk
```

#### Step 2: Install Dependencies

Install all required Python packages using `pip`:

```bash
# Install required Python packages from requirements.txt
pip install -r requirements.txt
```

#### Step 3: Run the Application

Once all dependencies are installed, you can run the Flask application by executing:

```bash
# Run the Flask application
python run.py
```

This command will start the Flask server on the default port `http://localhost:8000`, and you can access the API endpoints from there.

