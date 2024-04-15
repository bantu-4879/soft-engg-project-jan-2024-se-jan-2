import joblib 

#directory_path = "/Users/sahithi/Documents/GitHub/soft-engg-project-jan-2024-se-jan-2/code/backend/application/Ticker_priority_model"

loaded_model = joblib.load('pre-trained-model.pkl')
ticket_description = ["Discrepancy in grades", "Wrong evaluation in graded assignments", "When is the next live session?", "Extention of the deadline"]
predicted_priority = loaded_model.predict(ticket_description)
print("Predicted Priority Rating:", predicted_priority[:])