document.addEventListener('DOMContentLoaded', function() {
    const addTaskForm = document.getElementById('addTaskForm');
    addTaskForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const taskTitle = document.getElementById('taskTitle').value;
        const taskDescription = document.getElementById('taskDescription').value;
        
        // Fetch API to add a task dynamically (only if using API calls instead of form submission)
        fetch('/add_task', {
            method: 'POST',
            body: JSON.stringify({ title: taskTitle, description: taskDescription }),
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => response.json())
        .then(data => {
            // After adding the task, redirect or update the task list
            window.location.reload();
        })
        .catch(error => console.log(error));
    });
});
