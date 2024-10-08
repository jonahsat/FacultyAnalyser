# Faculty Performance Evaluation and Review Platform

This is a Django-based platform designed to collect and analyze feedback from students to evaluate faculty performance. The platform allows students to submit feedback on their faculty members through a simple form-based interface. The collected data is processed and analyzed, generating performance insights for faculty members in the form of summaries, strengths, areas for improvement, and an overall rating. The platform also includes dashboards for both students and faculty, displaying relevant data and actions.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Models Overview](#models-overview)
- [Functionality](#functionality)
  - [Student Feedback](#student-feedback)
  - [Teacher Analysis](#teacher-analysis)
- [Contributions](#contributions)
- [License](#license)

---

## Project Overview

This platform helps automate faculty evaluations by collecting student feedback and providing insights into faculty performance. The key feature of the system is that it uses predefined questions with 5-point scale options (Strongly Disagree, Disagree, Neutral, Agree, Strongly Agree) to collect responses. These responses are averaged and passed through AI models to generate performance reviews for faculty members, highlighting their strengths, areas for improvement, and overall performance.

---

## Features

1. **Student Dashboard**:
   - View and update profile information.
   - Give feedback to faculty members.
   - View previous feedback submissions.

2. **Faculty Dashboard**:
   - View personal profile information.
   - Start performance analysis based on collected feedback.
   - Review analysis results (overall score, summary, strengths, areas for improvement).

3. **Feedback Collection**:
   - Students can submit feedback for faculty members based on predefined questions.
   - Feedback is captured as ratings on a 1-5 scale.

4. **Performance Analysis**:
   - AI-based analysis of faculty feedback.
   - Summary of strengths and areas for improvement.
   - Overall rating generation based on student responses.

5. **Admin Panel**:
   - Admin users can manage the student and faculty accounts, and configure questions for feedback.

---

## Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS (TailwindCSS), JavaScript
- **Database**: PostgreSQL (Render)
- **Deployment**: Vercel (Frontend), AWS (Future for Backend)
- **AI Integration**: Gemini AI (for text-based performance analysis)

---

## Installation

### Prerequisites

- Python 3.x
- Virtual Environment (recommended)

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/jonahsat/FacultyAnalyser.git
   ```

2. Navigate to the project directory:

   ```bash
   cd faculty_analyser
   ```

3. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Apply migrations:

   ```bash
   python manage.py migrate
   ```

6. Run the development server:

   ```bash
   python manage.py runserver
   ```

7. Visit `http://127.0.0.1:8000` in your browser to access the platform.

---

## Usage

1. **Student Actions**:
   - Login and navigate to the dashboard.
   - Provide feedback to faculty members.
   - Review previously submitted feedback.

2. **Faculty Actions**:
   - Login to the dashboard.
   - View profile and performance analysis.
   - Start a new performance analysis if there isn’t one already.

3. **Admin Actions**:
   - Manage student and faculty accounts through the Django admin panel.
   - Add or modify questions for feedback collection.

---

## Models Overview

### User Models:
- **UserProfile**: Extends Django’s user model to distinguish between student and faculty roles.
- **Student**: Contains specific fields like major, semester, and registration ID.
- **Teacher**: Contains fields like department and faculty-specific information.

### Feedback Models:
- **Question**: Stores feedback questions.
- **Option**: Stores the answer options for each question (strongly disagree to strongly agree).
- **Feedback**: Links students to teachers through questions and selected options.

### Analysis Model:
- **Analysis**: Stores the AI-generated analysis for each teacher, including overall score, summary, strengths, and areas for improvement.

---

## Functionality

### Student Feedback

- **Feedback Form**: Students fill out a feedback form consisting of multiple-choice questions. Each question has a 5-option scale (Strongly Disagree - Strongly Agree).
  
- **Feedback Submission**: Once submitted, feedback is stored in the database for later analysis.

### Teacher Analysis

- **Analysis Generation**: After collecting feedback, the teacher can initiate performance analysis from their dashboard. The system calculates the average opinion for each question and sends the data to the AI for further processing.
  
- **Generated Report**: The system generates a performance report, including:
  1. **Overall Score**: A number out of 5, based on average feedback ratings.
  2. **Summary**: A brief analysis of the faculty’s performance.
  3. **Strengths**: Positive aspects of the faculty's teaching.
  4. **Areas to Improve**: Constructive feedback for improvement.

---


## Contributions

Contributions to this project are welcome! Feel free to fork the repository and create a pull request. Please follow these guidelines:
1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature-name`).
3. Commit your changes.
4. Push to your fork and submit a pull request.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

Special thanks to the Gemini AI team for providing the API used in this project.

--- 
