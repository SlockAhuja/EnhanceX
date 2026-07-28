"""
EnhanceX REST API Client Example
Created by Slock Ahuja (https://github.com/SlockAhuja/EnhanceX)
"""

from enhancex.sdk import EnhanceXClient

client = EnhanceXClient(endpoint="http://localhost:8000")
task = client.submit_task("sample_input.jpg", "sample_output.jpg", mode="auto")
print(f"Submitted task: {task.task_id}")
client.process_batch_sync()
print(f"Task status: {task.status}")
