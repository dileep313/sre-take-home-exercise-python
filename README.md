
#  HTTP Endpoint Availability Monitoring Tool
*Fetch SRE Take-Home Exercise Solution*

---

##  Project Overview
A lightweight, Python-based monitoring tool designed to evaluate the availability of HTTP endpoints based on reliability standards provided by **Fetch Rewards**.

The tool performs automated health checks on configured endpoints, ensuring they respond with:
-  HTTP Status Codes between **200-299**
-  Response times within **500 milliseconds**

It calculates **cumulative availability** by domain and logs results every 15 seconds — demonstrating key Site Reliability Engineering (SRE) practices.

---

## Description
This project was developed as part of the **Fetch Rewards Site Reliability Engineering (SRE) Take-Home Exercise**.

### Key Features:
- Reads endpoint configurations from a YAML file.
- Performs scheduled health checks.
- Logs availability percentages (with decimals dropped as per requirements).
- Graceful error handling and detailed logging.
- Ignores port numbers when grouping domains.

This solution highlights reliability, observability, and robust error management — core principles in SRE.

---

##  Getting Started

###  Dependencies
Before running the program, ensure you have:

- Python **3.x**
- `pip` package manager
- Required Python libraries:

```bash
pip install requests pyyaml
```

---

### Installing

1. **Clone the Repository**
   ```bash
   git clone https://github.com/dileep313/sre-take-home-exercise-python.git
   cd sre-take-home-exercise-python
   ```

2. **Install Dependencies**
   ```bash
   pip install requests pyyaml
   ```

### Executing the Program

Run the monitoring script by passing your YAML configuration:

```bash
python main.py sample.yaml
```

-  Health checks run every **15 seconds**
-  Logs cumulative availability per domain
-  Stop execution anytime using `Ctrl + C`

---

## How Each Issue Was Identified and Why Each Change Was Made

During the review of the provided starter code, I systematically compared the implementation against the exercise requirements. Each gap was identified by analyzing expected behaviors versus actual code behavior. Below is a detailed explanation:

1. **Default HTTP Method Handling**
   - *Identified:* The script failed when `method` was missing in the YAML.
   - *Why Changed:* Added a fallback to `GET` for robustness.

2. **Handling of Headers and Body**
   - *Identified:* Missing `headers` or `body` led to request errors.
   - *Why Changed:* Applied safe defaults and parsed JSON correctly.

3. **Response Time Validation**
   - *Identified:* No enforcement of 500ms response limit.
   - *Why Changed:* Integrated response time checks to meet availability criteria.

4. **Request Timeout**
   - *Identified:* Potential hangs due to slow endpoints.
   - *Why Changed:* Implemented `timeout=5` to ensure consistent cycles.

5. **Domain Parsing**
   - *Identified:* Port numbers included in domain grouping.
   - *Why Changed:* Adjusted parsing logic to exclude ports.

6. **Availability Calculation**
   - *Identified:* Used rounding instead of truncating decimals.
   - *Why Changed:* Switched to `int()` for compliance.

7. **Error Logging**
   - *Identified:* Lack of clarity on endpoint failures.
   - *Why Changed:* Added detailed exception handling.

---
