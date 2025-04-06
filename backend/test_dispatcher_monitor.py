from services.dispatcher_monitor import evaluate_dispatcher

# Sample synthetic test data
sample_logs = [
    {"duration": 8, "status": "dropped", "timestamp": "2024-04-05T14:01:00"},
    {"duration": 45, "status": "completed", "timestamp": "2024-04-05T14:10:00"},
    {"duration": 5, "status": "dropped", "timestamp": "2024-04-05T14:20:00"},
    {"duration": 60, "status": "completed", "timestamp": "2024-04-05T14:32:00"},
    {"duration": 6, "status": "dropped", "timestamp": "2024-04-05T14:45:00"},
    {"duration": 7, "status": "dropped", "timestamp": "2024-04-05T14:59:00"},
    {"duration": 40, "status": "completed", "timestamp": "2024-04-05T15:15:00"},
    {"duration": 50, "status": "completed", "timestamp": "2024-04-05T15:30:00"},
    {"duration": 9, "status": "dropped", "timestamp": "2024-04-05T15:45:00"},
    {"duration": 55, "status": "completed", "timestamp": "2024-04-05T16:00:00"}
]

dispatcher_id = "D1234"

print("💡 Starting test script...")

result = evaluate_dispatcher(dispatcher_id, sample_logs)

print("🧠 Dispatcher Behavior Analysis:")
print(result)
