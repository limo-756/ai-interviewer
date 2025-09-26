# ai-interviewer
Chat application that can emulate an interview with the candidate

# How to run the application locally
### Backend
1. Create a virtual env
2. Activate virtual env
3. Run `pip install -r ai-interviewer-backend/requirements.txt`
4. Run `cd ai-interviewer-backend/src/python`
5. Run `uvicorn interviewer.main:app --reload`

### Frontend
1. Run `cd ai-interviewer-frontend`
2. Run `npm start`